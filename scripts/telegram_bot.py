#!/usr/bin/env python3
"""
뉴스 브리핑 텔레그램 봇
매일 아침 개인화된 뉴스 브리핑을 TTS MP3로 전송
"""

import os
import asyncio
import logging
from datetime import datetime, time
from pathlib import Path

from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# TTS 생성기 import
import sys
sys.path.insert(0, str(Path(__file__).parent))
from tts_generator import generate_briefing_audio, VOICES

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 설정
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', '')
ALLOWED_USERS = os.environ.get('TELEGRAM_ALLOWED_USERS', '').split(',')
DEFAULT_VOICE = 'sunhi'

# 브리핑 저장 경로
AUDIO_DIR = Path(__file__).parent.parent / 'briefings' / 'audio'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)


# 샘플 브리핑 (실제로는 뉴스 검색 결과를 사용)
def get_sample_briefing() -> str:
    """샘플 브리핑 텍스트 반환 (테스트용)"""
    today = datetime.now()
    return f"""
오늘의 핵심 (3줄 요약)
1. 2026년 기업교육 AX 시대 본격화 - PBL 형태 AI 실무 교육 확대
2. 건설업계 핵심 화두: 안전과 AI - SK에코플랜트 AI 솔루션 기업 선언
3. 한일 셔틀외교 완전 정착 - 경제안보·과학기술 협력 확대

대한민국 뉴스

2026년 건설업계 핵심 화두: 안전과 AI

해석 및 배경지식
주요 건설사 신년사의 공통분모는 안전임.
이재명 정부 출범 이후 중대재해 대응 기조가 한층 엄격해졌음.
AI를 잘 쓰는 기업과 못 쓰는 기업 간 격차가 실적과 생존을 가르는 기준이 될 듯함.

시사점 (이한솔님 맞춤)
자이씨앤에이도 안전교육과 AI 역량 강화가 핵심 과제가 될 것임.
나누쌤 플랫폼에 안전교육 AI 콘텐츠 추가 검토 필요함.

2026년 HRD 기업교육 트렌드: AI 전환 시대

해석 및 배경지식
2026년은 AI를 실무에 직접 적용하는 PBL 형태 교육이 확대됨.
전사 임직원 50%가 생성AI 변화를 이해하고, 15%가 AI로 스스로 문제 해결 가능해야 함.
이 수준 도달 시 조직 전체가 움직이기 시작함.

시사점 (이한솔님 맞춤)
나누쌤 플랫폼을 PBL 형태로 업그레이드하면 차별화 가능함.
교육 후 USE-CASE 창출을 KPI로 설정 검토 필요함.
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """시작 명령어"""
    user = update.effective_user
    await update.message.reply_text(
        f"안녕하세요, {user.first_name}님! 🎙️\n\n"
        "개인화 뉴스 브리핑 봇입니다.\n\n"
        "📋 명령어:\n"
        "/news - 오늘의 뉴스 브리핑 (텍스트)\n"
        "/audio - 음성 브리핑 (MP3)\n"
        "/voice [sunhi/injoon/hyunsu] - 음성 변경\n"
        "/help - 도움말"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """도움말"""
    await update.message.reply_text(
        "🎙️ 뉴스 브리핑 봇 사용법\n\n"
        "📰 /news\n"
        "오늘의 개인화 뉴스 브리핑을 텍스트로 받습니다.\n\n"
        "🔊 /audio\n"
        "뉴스 브리핑을 음성 MP3 파일로 받습니다.\n"
        "출퇴근 시간에 듣기 좋습니다!\n\n"
        "🎤 /voice [음성]\n"
        "TTS 음성을 변경합니다.\n"
        "- sunhi: 여성 (기본, 뉴스 앵커 스타일)\n"
        "- injoon: 남성 (차분한 스타일)\n"
        "- hyunsu: 남성 (밝은 스타일)\n\n"
        "⏰ 자동 브리핑\n"
        "매일 아침 7시에 자동으로 브리핑을 보내드립니다.\n"
        "(설정: /subscribe, /unsubscribe)"
    )


async def news_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """뉴스 브리핑 (텍스트)"""
    await update.message.reply_text("📰 뉴스를 검색하고 있습니다...")

    # 브리핑 생성 (실제로는 뉴스 검색 API 연동)
    briefing = get_sample_briefing()

    # 텔레그램 메시지 길이 제한 (4096자)
    if len(briefing) > 4000:
        # 여러 메시지로 분할
        for i in range(0, len(briefing), 4000):
            await update.message.reply_text(briefing[i:i+4000])
    else:
        await update.message.reply_text(briefing)


async def audio_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """음성 브리핑 (MP3)"""
    await update.message.reply_text("🎙️ 음성 브리핑을 생성하고 있습니다...\n잠시만 기다려주세요.")

    try:
        # 브리핑 생성
        briefing = get_sample_briefing()

        # 사용자별 음성 설정 가져오기
        voice_name = context.user_data.get('voice', DEFAULT_VOICE)
        voice = VOICES.get(voice_name, VOICES[DEFAULT_VOICE])

        # MP3 생성
        today = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        filename = f"briefing_{update.effective_user.id}_{today}.mp3"
        output_path = await generate_briefing_audio(
            briefing,
            filename,
            voice=voice,
            user_name="이한솔"
        )

        # MP3 전송
        with open(output_path, 'rb') as audio_file:
            await update.message.reply_audio(
                audio=audio_file,
                title=f"뉴스 브리핑 {datetime.now().strftime('%Y-%m-%d')}",
                performer="뉴스 브리핑 AI",
                caption=f"🎙️ 오늘의 뉴스 브리핑\n음성: {voice_name}"
            )

        # 임시 파일 삭제 (선택)
        # os.remove(output_path)

    except Exception as e:
        logger.error(f"음성 생성 오류: {e}")
        await update.message.reply_text(
            f"❌ 음성 생성 중 오류가 발생했습니다.\n{str(e)}"
        )


async def voice_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """음성 변경"""
    if context.args and context.args[0] in VOICES:
        voice_name = context.args[0]
        context.user_data['voice'] = voice_name

        voice_info = {
            'sunhi': '여성, 뉴스 앵커 스타일',
            'injoon': '남성, 차분한 스타일',
            'hyunsu': '남성, 밝은 스타일'
        }

        await update.message.reply_text(
            f"✅ 음성이 변경되었습니다.\n\n"
            f"🎤 {voice_name}: {voice_info[voice_name]}"
        )
    else:
        current = context.user_data.get('voice', DEFAULT_VOICE)
        await update.message.reply_text(
            f"현재 음성: {current}\n\n"
            "사용법: /voice [음성이름]\n\n"
            "사용 가능한 음성:\n"
            "- sunhi: 여성, 뉴스 앵커 스타일\n"
            "- injoon: 남성, 차분한 스타일\n"
            "- hyunsu: 남성, 밝은 스타일"
        )


async def subscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """자동 브리핑 구독"""
    context.user_data['subscribed'] = True
    await update.message.reply_text(
        "✅ 자동 브리핑을 구독했습니다.\n"
        "매일 아침 7시에 음성 브리핑을 보내드립니다.\n\n"
        "구독 취소: /unsubscribe"
    )


async def unsubscribe_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """자동 브리핑 구독 취소"""
    context.user_data['subscribed'] = False
    await update.message.reply_text(
        "❌ 자동 브리핑 구독이 취소되었습니다."
    )


async def send_daily_briefing(context: ContextTypes.DEFAULT_TYPE) -> None:
    """매일 아침 자동 브리핑 전송 (스케줄러용)"""
    # 구독자 목록에서 브리핑 전송
    # 실제 구현 시 데이터베이스에서 구독자 목록 조회
    pass


def main() -> None:
    """봇 실행"""
    if not BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN 환경변수를 설정해주세요.")
        print("\n설정 방법:")
        print("export TELEGRAM_BOT_TOKEN='your-bot-token-here'")
        print("\n봇 토큰 발급:")
        print("1. 텔레그램에서 @BotFather 검색")
        print("2. /newbot 명령어로 봇 생성")
        print("3. 받은 토큰을 환경변수에 설정")
        return

    # 봇 생성
    application = Application.builder().token(BOT_TOKEN).build()

    # 명령어 핸들러 등록
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("news", news_command))
    application.add_handler(CommandHandler("audio", audio_command))
    application.add_handler(CommandHandler("voice", voice_command))
    application.add_handler(CommandHandler("subscribe", subscribe_command))
    application.add_handler(CommandHandler("unsubscribe", unsubscribe_command))

    # 매일 아침 7시 자동 브리핑 (KST)
    # job_queue = application.job_queue
    # job_queue.run_daily(
    #     send_daily_briefing,
    #     time=time(hour=7, minute=0, tzinfo=pytz.timezone('Asia/Seoul'))
    # )

    print("🤖 뉴스 브리핑 봇이 시작되었습니다.")
    print("Ctrl+C로 종료합니다.")

    # 봇 실행
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
