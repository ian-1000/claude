# 개인화 뉴스 브리핑 시스템

## 시스템 개요
이한솔 사용자를 위한 **올인원 개인화 뉴스 브리핑 AI** 시스템입니다.
28개 기능을 통합하여 지식 누적, 목표 관리, 업무/창작 지원을 제공합니다.

---

## 핵심 원칙

1. **개인화 매칭**: 모든 뉴스는 이한솔님의 프로필 기반으로 관련성 평가
2. **지식 누적**: 배운 용어, 수정 사항, 인사이트를 `/knowledge/`에 기록
3. **목표 연결**: 뉴스와 OKR(대학원, 웹소설)을 연결하여 시사점 제공
4. **음슴체 해석**: 모든 해석은 ~임, ~함, ~인 듯함 스타일로 작성

---

## 사용자 프로필 참조

| 파일 | 용도 |
|------|------|
| `/user/profile.md` | HR 정보, 개인정보, 핵심 키워드 |
| `/user/interests.md` | 관심 분야 상세 (AI, 건설, 웹소설) |
| `/user/portfolio.md` | 투자 정보 |

---

## 명령어 목록

### 뉴스 브리핑
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `뉴스 검색해줘` | 오늘의 개인화 브리핑 | `/config/briefing-template.md` |
| `주간 리포트` | 주간 트렌드 요약 | `/briefings/weekly/` |
| `월간 리포트` | 월간 트렌드 분석 | `/briefings/monthly/` |
| `한일 뉴스` | 한일 관계 특별 브리핑 | `/special/korea-japan.md` |
| `HRD 트렌드` | 기업교육 동향 | `/work/trends/` |
| `경쟁사 동향` | 건설사/HRD 경쟁사 | `/trackers/competitors.md` |
| `웹소설 시장 분석` | 플랫폼 동향 | `/creative/market-analysis.md` |
| `대학원 정보 업데이트` | 고려대/연세대 정보 | `/education/grad-school.md` |

### 지식 관리
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `용어 추가: [용어]` | 새 용어 학습 기록 | `/knowledge/terms/` |
| `수정 기록: [주제]` | 틀린 내용 수정 기록 | `/knowledge/corrections/` |
| `학습 현황` | 진행 상황 확인 | `/knowledge/progress.md` |
| `오늘의 복습` | 복습할 용어 확인 | `/knowledge/review-schedule.md` |
| `복습 완료: [용어]` | 복습 완료 표시 | `/knowledge/review-schedule.md` |
| `퀴즈 시작` | 자가 테스트 | `/knowledge/quizzes/` |
| `전문성 현황` | 분야별 레벨 확인 | `/knowledge/expertise.md` |

### 목표/액션 관리
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `OKR 현황` | 목표 달성률 확인 | `/goals/okr.md` |
| `액션 목록` | 미완료 할일 | `/actions/pending.md` |
| `액션 완료: [항목]` | 완료 처리 | `/actions/completed.md` |
| `액션 추가: [항목]` | 새 할일 추가 | `/actions/pending.md` |

### 분석
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `시장 현황` | 시장 지표 스냅샷 | `/dashboard/market.md` |
| `분석해줘: [질문]` | 대화형 분석 | - |
| `시나리오 분석: [주제]` | 예측 시뮬레이션 | `/analysis/scenarios/` |
| `연결 그래프: [주제]` | 뉴스 간 연결성 | `/knowledge/connections.md` |

### 창작 (웹소설)
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `아이디어 저장: [내용]` | 웹소설 소재 저장 | `/creative/ideas/` |
| `출간 현황` | 로드맵 확인 | `/creative/publishing-roadmap.md` |

### 업무 (HRD)
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `업무 아이디어 저장: [내용]` | 나누쌤/교육 아이디어 | `/work/insights/` |

### 일일 루틴
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `아침 루틴` | 뉴스 브리핑 + 액션 확인 | `/routines/daily.md` |
| `저녁 루틴` | 학습 정리 + 복습 체크 | `/routines/daily.md` |

### TTS (음성 브리핑)
| 명령어 | 기능 | 참조 파일 |
|--------|------|-----------|
| `뉴스 읽어줘` | 브리핑을 음성 MP3로 변환 | `/config/tts.md` |
| `브리핑 재생` | 생성된 MP3 파일 경로 안내 | `/briefings/audio/` |
| `음성 변경: [sunhi/injoon/hyunsu]` | TTS 음성 변경 | `/config/tts.md` |

### LINE 봇 (핸드폰 청취)
| 메시지 | 기능 | 참조 파일 |
|--------|------|-----------|
| `뉴스` | 텍스트 브리핑 | `/config/line-bot.md` |
| `음성` | m4a 음성 브리핑 전송 | - |
| `음성변경 [sunhi/injoon/hyunsu]` | 음성 변경 | - |
| `구독` | 매일 아침 자동 브리핑 | - |
| `구독취소` | 구독 해제 | - |
| `도움말` | 명령어 안내 | - |

---

## 뉴스 브리핑 생성 규칙

### 1. 뉴스 수집
- WebSearch 도구로 최신 뉴스 검색
- `/config/matching-rules.md` 기준으로 관련성 평가

### 2. 개인화 매칭
```
키워드 매칭 → 맥락 매칭 → 시의성 매칭 → 최종 점수
```

### 3. 시사점 생성
- **업무 관점**: 자이씨앤에이, HRD, 나누쌤 플랫폼 연결
- **학업 관점**: 대학원 진학, AI/데이터사이언스 연결
- **창작 관점**: 웹소설 출간, 콘텐츠 시장 연결
- **가정 관점**: 한일 관계, 일본어 학습 연결

### 4. 출력 형식
- `/config/briefing-template.md` 형식 준수
- 음슴체 사용 (~임, ~함, ~인 듯함)

---

## 지식 관리 규칙

### 용어 추가 시
1. `/knowledge/terms/{term-name}.md` 생성
2. `/knowledge/progress.md` 통계 업데이트
3. `/knowledge/review-schedule.md` 복습 일정 추가
4. `/knowledge/expertise.md` 해당 분야 경험치 추가

### 수정 기록 시
1. `/knowledge/corrections/YYYY-MM-DD-{topic}.md` 생성
2. `/knowledge/misconceptions.md` 패턴 분석 업데이트
3. `/knowledge/progress.md` 통계 업데이트

### 복습 시스템 (스페이스드 리피티션)
- 1일 후 → 3일 후 → 7일 후 → 14일 후 → 30일 후
- 복습 성공 시 다음 단계로, 실패 시 1일 후로 리셋

---

## 전문성 레벨 시스템

| 레벨 | 이름 | 조건 |
|------|------|------|
| Lv.1 | 입문자 | 용어 0-5개 |
| Lv.2 | 학습자 | 용어 6-15개 |
| Lv.3 | 숙련자 | 용어 16-30개 |
| Lv.4 | 전문가 | 용어 31-50개 |
| Lv.5 | 마스터 | 용어 51개+ |

분야: 경제/금융, 기술/AI, HRD/조직개발, 건설/부동산, 콘텐츠/출판, 정치/정책

---

## 알림 규칙

### 긴급 알림
- AI 규제 정책 변경
- 건설업 주요 정책
- 대학원 입시 일정

### 중요 알림
- 웹소설 공모전 공고
- LLM/AI 신기술 발표
- 한일 정상회담

---

## 파일 구조 참조

```
/home/user/claude/
├── CLAUDE.md                 # 이 파일
├── scripts/                  # Python 스크립트
│   ├── tts_generator.py      # TTS 변환기 (MP3/m4a)
│   └── line_bot.py           # LINE 봇
├── user/                     # 사용자 정보
├── knowledge/                # 지식 관리
├── briefings/                # 브리핑 저장
│   └── audio/                # TTS MP3 파일
├── config/                   # 설정
├── goals/                    # 목표 관리
├── actions/                  # 액션 아이템
├── analysis/                 # 분석
├── dashboard/                # 대시보드
├── alerts/                   # 알림
├── trackers/                 # 추적
├── work/                     # 업무
├── creative/                 # 웹소설
├── special/                  # 특별 섹션
├── learning/                 # 학습
├── education/                # 대학원
├── visualizations/           # 시각화
└── routines/                 # 루틴
```

---

## 메타데이터
- 버전: 1.0
- 생성일: 2026-02-02
- 기능 수: 28개
