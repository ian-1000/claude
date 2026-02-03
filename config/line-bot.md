# LINE 봇 설정 가이드

## 개요
LINE Messaging API를 사용하여 핸드폰으로 뉴스 브리핑을 받는 봇입니다.

---

## 1단계: LINE Official Account 생성

### 1.1 LINE Developers Console 접속
1. https://developers.line.biz/console/ 접속
2. LINE 계정으로 로그인
3. "Create a new provider" 클릭 (처음인 경우)
4. Provider 이름 입력 (예: "뉴스브리핑")

### 1.2 Messaging API 채널 생성
1. Provider 선택 → "Create a new channel"
2. "Messaging API" 선택
3. 정보 입력:
   - Channel name: `뉴스브리핑봇`
   - Channel description: `개인화 뉴스 브리핑 봇`
   - Category: `미디어, 엔터테인먼트`
   - Subcategory: `뉴스, 신문`
4. "Create" 클릭

---

## 2단계: 토큰 발급

### 2.1 Channel Access Token
1. 생성된 채널 → "Messaging API" 탭
2. 아래로 스크롤 → "Channel access token"
3. "Issue" 클릭 → 토큰 복사

### 2.2 Channel Secret
1. "Basic settings" 탭
2. "Channel secret" 복사

---

## 3단계: Webhook 설정

### 3.1 ngrok 설치 (로컬 테스트용)
```bash
# macOS
brew install ngrok

# 또는 https://ngrok.com/download 에서 다운로드
```

### 3.2 ngrok 실행
```bash
ngrok http 5000
```
출력된 HTTPS URL 복사 (예: `https://abc123.ngrok.io`)

### 3.3 LINE에 Webhook URL 설정
1. LINE Developers Console → 채널 → "Messaging API" 탭
2. "Webhook URL" 에 입력: `https://abc123.ngrok.io/callback`
3. "Use webhook" 활성화
4. "Verify" 클릭하여 테스트

---

## 4단계: 봇 실행

### 4.1 환경변수 설정
```bash
export LINE_CHANNEL_ACCESS_TOKEN='여기에_채널_액세스_토큰'
export LINE_CHANNEL_SECRET='여기에_채널_시크릿'
export LINE_WEBHOOK_BASE_URL='https://abc123.ngrok.io'
```

### 4.2 봇 실행
```bash
cd /home/user/claude
python scripts/line_bot.py
```

### 4.3 LINE 앱에서 테스트
1. LINE Developers Console → "Messaging API" 탭
2. QR 코드 스캔하여 봇 친구 추가
3. "뉴스" 또는 "음성" 입력하여 테스트

---

## 봇 명령어

| 메시지 | 기능 |
|--------|------|
| `뉴스` | 텍스트 브리핑 |
| `음성` | m4a 음성 브리핑 |
| `음성변경 sunhi` | 여성 음성 (기본) |
| `음성변경 injoon` | 남성 음성 (차분) |
| `음성변경 hyunsu` | 남성 음성 (밝음) |
| `구독` | 매일 아침 7시 자동 브리핑 |
| `구독취소` | 구독 해제 |
| `상태` | 현재 설정 확인 |
| `도움말` | 도움말 표시 |

---

## 무료 호스팅 옵션 (24시간 운영)

### Railway (추천)
1. https://railway.app 접속
2. GitHub 연결 → 프로젝트 배포
3. 환경변수 설정
4. 자동 HTTPS URL 제공

### Render
1. https://render.com 접속
2. "New Web Service" → GitHub 연결
3. 환경변수 설정
4. 무료 티어: 월 750시간

### Fly.io
1. https://fly.io 접속
2. CLI 설치 → `flyctl launch`
3. 무료 티어: 3개 VM

---

## 문제 해결

### "Invalid signature" 오류
- Channel Secret이 정확한지 확인
- 환경변수가 제대로 설정되었는지 확인

### 오디오가 재생되지 않음
- Webhook URL이 HTTPS인지 확인
- ngrok이 실행 중인지 확인
- m4a 파일이 생성되었는지 확인

### 봇이 응답하지 않음
- Webhook URL이 LINE에 설정되었는지 확인
- "Use webhook"이 활성화되었는지 확인
- Flask 서버가 실행 중인지 확인

---

## 비용

| 항목 | 비용 |
|------|------|
| LINE Official Account | 무료 |
| Messaging API | 무료 (500메시지/월) |
| ngrok (로컬) | 무료 |
| Railway/Render | 무료 티어 |

**일반적인 사용 시 완전 무료**

---

## 참고 링크

- [LINE Developers Console](https://developers.line.biz/console/)
- [Messaging API 문서](https://developers.line.biz/en/docs/messaging-api/)
- [line-bot-sdk-python](https://github.com/line/line-bot-sdk-python)
