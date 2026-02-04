#!/usr/bin/env python3
"""
뉴스 브리핑 LINE 봇
LINE Messaging API를 사용하여 핸드폰으로 뉴스 브리핑 전송
"""

import os
import sys
import asyncio
import json
import threading
from datetime import datetime, time
from pathlib import Path
from flask import Flask, request, abort, send_from_directory
from linebot.v3 import WebhookHandler
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,
    TextMessage,
    AudioMessage,
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.v3.exceptions import InvalidSignatureError

# 프로젝트 경로 설정
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from tts_generator import (
    generate_briefing_audio_m4a,
    VOICES,
    OUTPUT_DIR,
)

# 뉴스 브리핑 엔진 import
from news_briefing import generate_news_briefing

# Flask 앱 설정
app = Flask(__name__)

# LINE 설정 (환경변수에서 로드)
CHANNEL_ACCESS_TOKEN = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN", "")
CHANNEL_SECRET = os.environ.get("LINE_CHANNEL_SECRET", "")

# Webhook URL (ngrok 또는 서버 URL)
WEBHOOK_BASE_URL = os.environ.get("LINE_WEBHOOK_BASE_URL", "http://localhost:5000")

# 설정 검증
if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
    print("경고: LINE_CHANNEL_ACCESS_TOKEN 또는 LINE_CHANNEL_SECRET가 설정되지 않았습니다.")
    print("환경변수를 설정하세요:")
    print("  export LINE_CHANNEL_ACCESS_TOKEN='your_token'")
    print("  export LINE_CHANNEL_SECRET='your_secret'")

# LINE API 클라이언트
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# 사용자 설정 저장 (메모리)
user_settings = {}
subscribed_users = set()

# 기본 설정
DEFAULT_VOICE = "sunhi"
DEFAULT_USER_NAME = "이한솔"

# LINE 메시지 최대 길이
LINE_MAX_MESSAGE_LENGTH = 4500


def split_message(text: str, max_length: int = LINE_MAX_MESSAGE_LENGTH) -> list:
    """긴 메시지를 여러 개로 분할 (LINE 5000자 제한 대응)"""
    if len(text) <= max_length:
        return [text]

    messages = []
    # 섹션 구분자로 분할
    separator = "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    sections = text.split(separator)

    current_msg = ""
    for i, section in enumerate(sections):
        test_addition = separator + section if i > 0 else section

        if len(current_msg) + len(test_addition) > max_length:
            if current_msg.strip():
                messages.append(current_msg.strip())
            current_msg = section.strip()
        else:
            if i > 0 and current_msg:
                current_msg += separator
            current_msg += section

    if current_msg.strip():
        messages.append(current_msg.strip())

    return messages if messages else [text]


def get_user_setting(user_id: str, key: str, default=None):
    """사용자 설정 조회"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    return user_settings[user_id].get(key, default)


def set_user_setting(user_id: str, key: str, value):
    """사용자 설정 저장"""
    if user_id not in user_settings:
        user_settings[user_id] = {}
    user_settings[user_id][key] = value


def generate_sample_briefing() -> str:
    """샘플 뉴스 브리핑 생성 (실제로는 Claude가 생성)"""
    today = datetime.now()
    weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weekday = weekdays[today.weekday()]

    return f"""
# 오늘의 뉴스 브리핑
📅 {today.year}년 {today.month}월 {today.day}일 {weekday}

## 3줄 요약
1. AI 기술 발전이 교육 분야에 큰 변화를 가져오고 있음
2. 건설업계 디지털 전환 가속화 중
3. 한일 관계 개선 움직임 지속

## 시사점
- 업무: 나누쌤 플랫폼에 AI 기능 추가 검토 필요
- 학업: 대학원 AI 융합 과정과 연계 가능
- 창작: 웹소설 소재로 AI 관련 스토리 고려

---
이 브리핑은 LINE 봇 테스트용 샘플입니다.
실제 브리핑은 Claude가 생성합니다.
"""


@app.route("/callback", methods=["POST"])
def callback():
    """LINE Webhook 콜백"""
    signature = request.headers.get("X-Line-Signature", "")
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


@app.route("/audio/<filename>")
def serve_audio(filename):
    """오디오 파일 제공 (LINE에서 접근)"""
    return send_from_directory(OUTPUT_DIR, filename)


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    """텍스트 메시지 처리"""
    user_id = event.source.user_id
    text = event.message.text.strip().lower()

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        # 명령어 처리
        if text in ["뉴스", "브리핑", "news"]:
            # 상세 브리핑 생성 후 분할 전송
            briefing = handle_news_command(user_id)
            messages = split_message(briefing)

            # 여러 메시지로 분할 전송
            text_messages = [TextMessage(text=msg) for msg in messages[:5]]  # LINE 최대 5개
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=text_messages
                )
            )
            return  # 직접 응답 처리 완료
        elif text in ["음성", "오디오", "audio", "voice"]:
            handle_audio_command(user_id, line_bot_api, event.reply_token)
            return  # 오디오는 별도 처리
        elif text.startswith("음성변경") or text.startswith("voice"):
            parts = text.split()
            if len(parts) >= 2:
                voice = parts[1]
                reply = handle_voice_change(user_id, voice)
            else:
                reply = "사용법: 음성변경 sunhi/injoon/hyunsu"
        elif text in ["구독", "subscribe"]:
            reply = handle_subscribe(user_id)
        elif text in ["구독취소", "unsubscribe"]:
            reply = handle_unsubscribe(user_id)
        elif text in ["도움말", "help", "?"]:
            reply = get_help_message()
        elif text in ["상태", "status"]:
            reply = get_status_message(user_id)
        else:
            reply = f"알 수 없는 명령어입니다.\n\n{get_help_message()}"

        # 텍스트 응답
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=reply)]
            )
        )


def handle_news_command(user_id: str) -> str:
    """뉴스 브리핑 텍스트 반환 - 상세 개인화 브리핑"""
    # 상세 뉴스 브리핑 생성
    briefing = generate_news_briefing()
    return briefing


def handle_audio_command(user_id: str, line_bot_api: MessagingApi, reply_token: str):
    """음성 브리핑 생성 및 전송 - 뉴스 앵커 스타일"""
    try:
        # 먼저 "생성 중" 메시지는 보내지 않음 (LINE은 reply_token을 한 번만 사용 가능)

        # 사용자 설정
        voice_name = get_user_setting(user_id, "voice", DEFAULT_VOICE)
        voice = VOICES.get(voice_name, VOICES[DEFAULT_VOICE])

        # 상세 뉴스 브리핑 생성
        briefing = generate_news_briefing()

        # 오디오 생성 (m4a)
        today = datetime.now().strftime("%Y-%m-%d")
        filename = f"briefing_{today}_{user_id[-6:]}.m4a"

        # 비동기 실행
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            output_path = loop.run_until_complete(
                generate_briefing_audio_m4a(
                    briefing,
                    output_filename=filename,
                    voice=voice,
                    user_name=DEFAULT_USER_NAME
                )
            )
        finally:
            loop.close()

        # 오디오 URL 생성
        audio_url = f"{WEBHOOK_BASE_URL}/audio/{filename}"

        # 오디오 메시지 전송
        # 뉴스 브리핑은 길 수 있으므로 5분으로 설정
        duration = 300000

        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[
                    TextMessage(text="🎧 음성 브리핑을 생성했습니다.\n뉴스 앵커 스타일로 읽어드립니다."),
                    AudioMessage(
                        original_content_url=audio_url,
                        duration=duration
                    )
                ]
            )
        )

    except ImportError as e:
        # pydub 미설치
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=f"❌ 음성 기능에 필요한 패키지가 없습니다.\n\n오류: {str(e)}\n\n해결: pip install pydub 실행 필요")]
            )
        )
    except ConnectionError as e:
        # 네트워크 오류
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=f"❌ 음성 생성 서버에 연결할 수 없습니다.\n\n회사 네트워크에서 Microsoft TTS 서버가 차단되어 있을 수 있습니다.\n\n집에서 다시 시도해주세요.")]
            )
        )
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                reply_token=reply_token,
                messages=[TextMessage(text=f"❌ 오디오 생성 중 오류가 발생했습니다.\n\n오류 유형: {error_type}\n오류 내용: {error_msg[:200]}")]
            )
        )


def handle_voice_change(user_id: str, voice: str) -> str:
    """음성 변경"""
    voice = voice.lower()
    if voice in VOICES:
        set_user_setting(user_id, "voice", voice)
        voice_names = {
            "sunhi": "선희 (여성, 밝고 친근한 톤) ⭐추천",
            "injoon": "인준 (남성, 차분한 앵커)",
            "hyunsu": "현수 (남성, 밝은 톤)"
        }
        return f"✅ 음성이 {voice_names.get(voice, voice)}(으)로 변경되었습니다.\n\n💡 선희 음성이 가장 자연스럽습니다."
    else:
        return f"❌ 알 수 없는 음성입니다.\n\n사용 가능:\n• sunhi - 선희 (여성, 추천)\n• injoon - 인준 (남성)\n• hyunsu - 현수 (남성)"


def handle_subscribe(user_id: str) -> str:
    """구독 설정"""
    subscribed_users.add(user_id)
    return """✅ 매일 아침 7시 브리핑 구독이 설정되었습니다.

구독 해제: "구독취소" 입력

참고: 자동 브리핑은 서버가 계속 실행 중일 때만 작동합니다."""


def handle_unsubscribe(user_id: str) -> str:
    """구독 해제"""
    subscribed_users.discard(user_id)
    return "✅ 브리핑 구독이 해제되었습니다."


def get_help_message() -> str:
    """도움말 메시지"""
    return """📱 뉴스 브리핑 봇 도움말

[명령어]
• 뉴스 - 텍스트 브리핑
• 음성 - 음성 브리핑 (m4a)
• 음성변경 [이름] - 음성 변경
  └ sunhi (여성), injoon (남성), hyunsu (남성)
• 구독 - 매일 아침 자동 브리핑
• 구독취소 - 구독 해제
• 상태 - 현재 설정 확인
• 도움말 - 이 메시지

[사용 예시]
"뉴스" → 오늘의 뉴스 브리핑
"음성" → MP3 음성으로 듣기
"음성변경 injoon" → 남성 음성으로 변경"""


def get_status_message(user_id: str) -> str:
    """상태 메시지"""
    voice = get_user_setting(user_id, "voice", DEFAULT_VOICE)
    subscribed = "구독 중" if user_id in subscribed_users else "미구독"

    voice_names = {
        "sunhi": "선희 (여성)",
        "injoon": "인준 (남성)",
        "hyunsu": "현수 (남성)"
    }

    return f"""📊 현재 설정

• 음성: {voice_names.get(voice, voice)}
• 구독: {subscribed}
• 사용자 ID: ...{user_id[-6:]}"""


def send_scheduled_briefing():
    """예약 브리핑 전송 (구독자용)"""
    if not subscribed_users:
        return

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        briefing = generate_sample_briefing()

        for user_id in subscribed_users:
            try:
                line_bot_api.push_message(
                    PushMessageRequest(
                        to=user_id,
                        messages=[
                            TextMessage(text="🌅 좋은 아침입니다! 오늘의 뉴스 브리핑입니다."),
                            TextMessage(text=briefing)
                        ]
                    )
                )
            except Exception as e:
                print(f"브리핑 전송 실패 ({user_id}): {e}")


def run_scheduler():
    """스케줄러 실행 (별도 스레드)"""
    import schedule
    import time as time_module

    schedule.every().day.at("07:00").do(send_scheduled_briefing)

    while True:
        schedule.run_pending()
        time_module.sleep(60)


def main():
    """메인 실행"""
    print("=" * 50)
    print("📱 뉴스 브리핑 LINE 봇")
    print("=" * 50)

    if not CHANNEL_ACCESS_TOKEN or not CHANNEL_SECRET:
        print("\n⚠️  LINE 설정이 필요합니다!")
        print("\n1. LINE Developers Console 접속:")
        print("   https://developers.line.biz/console/")
        print("\n2. 환경변수 설정:")
        print("   export LINE_CHANNEL_ACCESS_TOKEN='your_token'")
        print("   export LINE_CHANNEL_SECRET='your_secret'")
        print("   export LINE_WEBHOOK_BASE_URL='https://your-ngrok-url'")
        print("\n3. 봇 다시 실행")
        return

    print(f"\n✅ LINE 설정 완료")
    print(f"🔗 Webhook URL: {WEBHOOK_BASE_URL}/callback")
    print(f"📁 오디오 디렉토리: {OUTPUT_DIR}")

    # 스케줄러 스레드 시작
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    print("⏰ 스케줄러 시작됨 (매일 07:00 브리핑)")

    print("\n서버 시작 중... (Ctrl+C로 종료)")
    print("-" * 50)

    # Flask 서버 실행
    app.run(host="0.0.0.0", port=5000, debug=False)


if __name__ == "__main__":
    main()
