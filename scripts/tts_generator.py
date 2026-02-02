#!/usr/bin/env python3
"""
뉴스 브리핑 TTS 변환기
edge-tts를 사용하여 뉴스 브리핑을 자연스러운 음성으로 변환
"""

import asyncio
import edge_tts
import re
import os
import sys
from datetime import datetime
from pathlib import Path

# 기본 설정
DEFAULT_VOICE = "ko-KR-SunHiNeural"  # 여성 뉴스 앵커 스타일
DEFAULT_RATE = "+0%"  # 속도 조절 (-50% ~ +100%)
DEFAULT_VOLUME = "+0%"  # 볼륨 조절
DEFAULT_PITCH = "+0Hz"  # 음높이 조절

# 사용 가능한 한국어 음성
VOICES = {
    "sunhi": "ko-KR-SunHiNeural",      # 여성, 차분한 뉴스 앵커
    "injoon": "ko-KR-InJoonNeural",    # 남성, 차분한 뉴스 앵커
    "hyunsu": "ko-KR-HyunsuNeural",    # 남성, 밝은 톤
}

# 출력 디렉토리
OUTPUT_DIR = Path(__file__).parent.parent / "briefings" / "audio"


def clean_text_for_tts(text: str) -> str:
    """
    마크다운/이모지를 제거하고 TTS에 적합한 텍스트로 변환
    """
    # 이모지 제거
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"
        u"\u3030"
        u"\u2022"  # bullet point
        "]+", flags=re.UNICODE)
    text = emoji_pattern.sub('', text)

    # 마크다운 기호 제거
    text = re.sub(r'#{1,6}\s*', '', text)  # 헤더
    text = re.sub(r'\*{1,2}([^*]+)\*{1,2}', r'\1', text)  # 볼드/이탤릭
    text = re.sub(r'`{1,3}[^`]*`{1,3}', '', text)  # 코드 블록
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # 링크
    text = re.sub(r'━+', '', text)  # 구분선
    text = re.sub(r'╔[═╗]+', '', text)  # 박스 상단
    text = re.sub(r'╚[═╝]+', '', text)  # 박스 하단
    text = re.sub(r'║', '', text)  # 박스 측면
    text = re.sub(r'\|[^|]+\|', '', text)  # 테이블
    text = re.sub(r'^\s*[-*+]\s*\[\s*[xX]?\s*\]', '', text, flags=re.MULTILINE)  # 체크박스
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)  # 리스트
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)  # 숫자 리스트
    text = re.sub(r'>\s*', '', text)  # 인용문

    # URL 제거
    text = re.sub(r'https?://\S+', '', text)
    text = re.sub(r'기사 보기\s*→?', '', text)

    # 특수 기호 변환
    text = text.replace('→', '')
    text = text.replace('←', '')
    text = text.replace('↓', '')
    text = text.replace('↑', '')

    # 연속 공백/줄바꿈 정리
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r' {2,}', ' ', text)
    text = text.strip()

    return text


def convert_to_news_script(briefing_text: str, user_name: str = "이한솔") -> str:
    """
    브리핑 텍스트를 뉴스 앵커 스타일의 읽기 스크립트로 변환
    """
    # 텍스트 정리
    text = clean_text_for_tts(briefing_text)

    # 뉴스 스크립트 구조화
    script_parts = []

    # 인트로
    today = datetime.now()
    weekdays = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']
    weekday = weekdays[today.weekday()]

    intro = f"""
안녕하세요, {user_name}님.
{today.year}년 {today.month}월 {today.day}일 {weekday}, 오늘의 뉴스 브리핑입니다.
"""
    script_parts.append(intro)

    # 본문 처리
    lines = text.split('\n')
    current_section = ""

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 섹션 헤더 감지 및 변환
        if '오늘의 핵심' in line or '3줄 요약' in line:
            script_parts.append("\n먼저 오늘의 핵심 뉴스 세 가지입니다.\n")
            current_section = "핵심"
        elif '세계 주요 이슈' in line or '세계' in line and '이슈' in line:
            script_parts.append("\n\n세계 주요 이슈입니다.\n")
            current_section = "세계"
        elif '대한민국 뉴스' in line or '국내' in line:
            script_parts.append("\n\n대한민국 뉴스입니다.\n")
            current_section = "국내"
        elif '해석' in line and '배경' in line:
            script_parts.append("\n해석 및 배경지식입니다.\n")
        elif '시사점' in line:
            script_parts.append(f"\n{user_name}님께 드리는 시사점입니다.\n")
        elif '용어 설명' in line:
            script_parts.append("\n용어 설명입니다.\n")
        elif '액션 아이템' in line:
            script_parts.append("\n\n오늘의 액션 아이템입니다.\n")
        elif '다음 뉴스' in line or '업데이트' in line:
            continue  # 메타 정보 스킵
        else:
            # 일반 텍스트
            # 음슴체를 존댓말로 변환
            line = re.sub(r'임$', '입니다', line)
            line = re.sub(r'함$', '합니다', line)
            line = re.sub(r'됨$', '됩니다', line)
            line = re.sub(r'였음$', '였습니다', line)
            line = re.sub(r'됐음$', '됐습니다', line)
            line = re.sub(r'인 듯함$', '인 것으로 보입니다', line)
            line = re.sub(r'일 듯함$', '일 것으로 보입니다', line)
            line = re.sub(r'로 보임$', '로 보입니다', line)
            line = re.sub(r'예상됨$', '예상됩니다', line)

            # 괄호 안 내용 자연스럽게
            line = re.sub(r'\(([^)]+)\)', r', \1,', line)

            if line:
                script_parts.append(line + "\n")

    # 아웃트로
    outro = f"""

이상으로 오늘의 뉴스 브리핑을 마칩니다.
{user_name}님, 좋은 하루 보내세요.
"""
    script_parts.append(outro)

    return ''.join(script_parts)


async def generate_tts(
    text: str,
    output_path: str,
    voice: str = DEFAULT_VOICE,
    rate: str = DEFAULT_RATE,
    volume: str = DEFAULT_VOLUME,
    pitch: str = DEFAULT_PITCH
) -> str:
    """
    텍스트를 MP3 음성 파일로 변환
    """
    communicate = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume,
        pitch=pitch
    )

    await communicate.save(output_path)
    return output_path


async def generate_briefing_audio(
    briefing_text: str,
    output_filename: str = None,
    voice: str = DEFAULT_VOICE,
    user_name: str = "이한솔"
) -> str:
    """
    브리핑 텍스트를 음성 파일로 변환하는 메인 함수
    """
    # 출력 디렉토리 생성
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 파일명 생성
    if output_filename is None:
        today = datetime.now().strftime("%Y-%m-%d")
        output_filename = f"briefing_{today}.mp3"

    output_path = OUTPUT_DIR / output_filename

    # 뉴스 스크립트로 변환
    script = convert_to_news_script(briefing_text, user_name)

    # TTS 생성
    await generate_tts(str(script), str(output_path), voice=voice)

    return str(output_path)


def list_voices():
    """사용 가능한 음성 목록 출력"""
    print("사용 가능한 한국어 음성:")
    for name, voice_id in VOICES.items():
        print(f"  - {name}: {voice_id}")


async def main():
    """CLI 인터페이스"""
    import argparse

    parser = argparse.ArgumentParser(description='뉴스 브리핑 TTS 변환기')
    parser.add_argument('--input', '-i', help='입력 텍스트 파일 경로')
    parser.add_argument('--output', '-o', help='출력 MP3 파일 경로')
    parser.add_argument('--voice', '-v', default='sunhi',
                        choices=list(VOICES.keys()),
                        help='음성 선택 (기본: sunhi)')
    parser.add_argument('--text', '-t', help='직접 텍스트 입력')
    parser.add_argument('--list-voices', action='store_true',
                        help='사용 가능한 음성 목록')
    parser.add_argument('--user', '-u', default='이한솔',
                        help='사용자 이름 (기본: 이한솔)')

    args = parser.parse_args()

    if args.list_voices:
        list_voices()
        return

    # 입력 텍스트 결정
    if args.text:
        text = args.text
    elif args.input:
        with open(args.input, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        print("텍스트를 입력하세요 (Ctrl+D로 종료):")
        text = sys.stdin.read()

    if not text.strip():
        print("오류: 텍스트가 비어있습니다.")
        sys.exit(1)

    # 음성 선택
    voice = VOICES.get(args.voice, DEFAULT_VOICE)

    # 출력 경로
    output_path = args.output
    if output_path is None:
        today = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        output_path = f"briefing_{today}.mp3"

    print(f"TTS 생성 중... (음성: {args.voice})")

    # 스크립트 변환 및 TTS 생성
    script = convert_to_news_script(text, args.user)
    await generate_tts(script, output_path, voice=voice)

    print(f"완료: {output_path}")


if __name__ == "__main__":
    asyncio.run(main())
