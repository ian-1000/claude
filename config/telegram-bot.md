# 텔레그램 봇 설정

## 개요
핸드폰에서 출퇴근 시간에 뉴스 브리핑을 들을 수 있는 텔레그램 봇

---

## 🚀 빠른 시작 (5분)

### 1단계: 봇 생성 (텔레그램에서)

1. 텔레그램 앱에서 **@BotFather** 검색
2. `/newbot` 입력
3. 봇 이름 입력 (예: `한솔 뉴스 브리핑`)
4. 봇 username 입력 (예: `hansol_news_bot`)
5. **토큰 복사** (예: `123456789:ABCdefGHIjklMNO...`)

### 2단계: 봇 실행 (PC에서)

```bash
# 프로젝트 폴더로 이동
cd /home/user/claude

# 환경변수 설정
export TELEGRAM_BOT_TOKEN='여기에_토큰_붙여넣기'

# 봇 실행
python scripts/telegram_bot.py
```

### 3단계: 핸드폰에서 사용

1. 텔레그램에서 내 봇 검색 (예: @hansol_news_bot)
2. `/start` 입력
3. `/audio` 입력 → MP3 파일 수신!

---

## 📋 봇 명령어

| 명령어 | 기능 |
|--------|------|
| `/start` | 봇 시작, 환영 메시지 |
| `/news` | 오늘의 뉴스 브리핑 (텍스트) |
| `/audio` | 음성 브리핑 (MP3 파일) |
| `/voice sunhi` | 여성 음성으로 변경 |
| `/voice injoon` | 남성(차분) 음성으로 변경 |
| `/voice hyunsu` | 남성(밝은) 음성으로 변경 |
| `/subscribe` | 매일 아침 자동 브리핑 구독 |
| `/unsubscribe` | 자동 브리핑 취소 |
| `/help` | 도움말 |

---

## 🎤 음성 옵션

| 이름 | 성별 | 특징 | 추천 |
|------|------|------|------|
| sunhi (기본) | 여성 | 차분한 뉴스 앵커 | 아침 브리핑 |
| injoon | 남성 | 차분하고 신뢰감 | 저녁 브리핑 |
| hyunsu | 남성 | 밝고 친근함 | 점심 브리핑 |

---

## ⏰ 자동 브리핑 설정

### 매일 아침 7시 자동 전송

```bash
# crontab 편집
crontab -e

# 아래 줄 추가 (매일 오전 7시)
0 7 * * * cd /home/user/claude && python scripts/telegram_bot.py --send-daily
```

### 또는 systemd 서비스로 등록

```bash
# /etc/systemd/system/news-bot.service
[Unit]
Description=News Briefing Telegram Bot
After=network.target

[Service]
Type=simple
User=user
WorkingDirectory=/home/user/claude
Environment=TELEGRAM_BOT_TOKEN=your-token-here
ExecStart=/usr/bin/python3 scripts/telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable news-bot
sudo systemctl start news-bot
```

---

## 🌐 24시간 실행 (무료 호스팅)

### 옵션 1: Railway (추천)

1. [railway.app](https://railway.app) 가입
2. GitHub 연동
3. 환경변수 설정: `TELEGRAM_BOT_TOKEN`
4. 자동 배포 완료!

**비용**: 월 $5 크레딧 무료 (충분함)

### 옵션 2: Render

1. [render.com](https://render.com) 가입
2. Web Service 생성
3. 환경변수 설정
4. 배포

**비용**: 무료 (15분 후 슬립 → 메시지 오면 깨어남)

### 옵션 3: 본인 PC

```bash
# 백그라운드 실행
nohup python scripts/telegram_bot.py > bot.log 2>&1 &
```

**비용**: 무료 (PC 켜져 있어야 함)

---

## 🔧 환경변수

| 변수명 | 필수 | 설명 |
|--------|------|------|
| `TELEGRAM_BOT_TOKEN` | ✅ | BotFather에서 받은 토큰 |
| `TELEGRAM_ALLOWED_USERS` | ❌ | 허용할 사용자 ID (쉼표 구분) |

### 환경변수 설정 방법

```bash
# 일시적 (현재 세션만)
export TELEGRAM_BOT_TOKEN='your-token'

# 영구적 (~/.bashrc에 추가)
echo "export TELEGRAM_BOT_TOKEN='your-token'" >> ~/.bashrc
source ~/.bashrc
```

---

## 📁 관련 파일

| 파일 | 설명 |
|------|------|
| `scripts/telegram_bot.py` | 봇 메인 스크립트 |
| `scripts/tts_generator.py` | TTS 변환기 |
| `config/telegram-bot.md` | 이 문서 |
| `briefings/audio/` | 생성된 MP3 저장 |

---

## 🐛 문제 해결

### "TELEGRAM_BOT_TOKEN 환경변수를 설정해주세요"
```bash
export TELEGRAM_BOT_TOKEN='your-token-here'
```

### "네트워크 오류" (TTS 생성 시)
- 인터넷 연결 확인
- edge-tts는 Microsoft 서버 연결 필요

### 봇이 응답하지 않음
- 토큰이 올바른지 확인
- 봇이 실행 중인지 확인 (`ps aux | grep telegram_bot`)

---

## 메타데이터
- 생성일: 2026-02-02
- 라이브러리: python-telegram-bot, edge-tts
