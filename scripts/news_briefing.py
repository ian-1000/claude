#!/usr/bin/env python3
"""
개인화 뉴스 브리핑 생성 엔진
이한솔 사용자 맞춤형 뉴스 브리핑 생성
"""

from datetime import datetime
from typing import List, Dict

# ============================================
# 1. 사용자 프로필
# ============================================

USER_PROFILE = {
    "name": "이한솔",
    "company": "자이씨앤에이(ZyC&A)",
    "parent_company": "GS건설",
    "role": "OD 전문가",
    "platform": "나누쌤",
    "career": "6년차 (교사 2년 → HRD 4년)",
    "family": "일본인 배우자",
    "hobby": "웹소설 집필 (조아라 69화 연재)",
    "education_goal": "고려대 데이터사이언스 / 연세대 AI융합",
}

# ============================================
# 2. 카테고리 아이콘
# ============================================

CATEGORY_ICONS = {
    "AI/기술": "🤖",
    "건설": "🏗️",
    "웹소설/콘텐츠": "✍️",
    "교육/HRD": "📚",
    "한일관계": "🎌",
    "대학원": "🎓",
    "경제/금융": "💰",
    "정책/규제": "📋",
    "세계": "🌐",
    "국내": "🇰🇷",
    "일반": "📰",
}

# ============================================
# 3. 개별 뉴스 포맷
# ============================================

def format_news_item(news: Dict) -> str:
    """개별 뉴스 항목 포맷"""
    return f"""
📌 {news['title']}
🔗 기사 보기 → {news.get('source', '뉴스')}
📍 {news.get('source', '')} | {news.get('date', '')}

💭 해석 및 배경지식
{news.get('analysis', '')}

📚 용어 설명
{news.get('terms', '- 해당 없음')}

🔍 시사점 (이한솔님 맞춤)
{news.get('implications', '')}
"""

# ============================================
# 4. 전체 브리핑 포맷
# ============================================

def format_full_briefing(world_news: List[Dict], korea_news: List[Dict], actions: List[str]) -> str:
    """전체 브리핑 생성"""
    today = datetime.now()
    weekdays = ['월', '화', '수', '목', '금', '토', '일']
    weekday = weekdays[today.weekday()]

    # 상위 3개 뉴스로 핵심 요약
    all_news = world_news + korea_news
    all_news.sort(key=lambda x: x.get('score', 0), reverse=True)
    top3 = all_news[:3]

    briefing = f"""╔══════════════════════════════════════════════╗
║  📰 오늘의 뉴스 브리핑                         ║
║  {today.year}년 {today.month}월 {today.day}일 ({weekday})                          ║
╚══════════════════════════════════════════════╝

> **이한솔**님을 위한 개인화 브리핑

## 오늘의 핵심 (3줄 요약)
"""

    # 핵심 3줄
    for news in top3:
        icon = CATEGORY_ICONS.get(news.get('category', '일반'), '📰')
        briefing += f"{icon} {news['title']} - {news.get('brief_implication', '')}\n"

    # 세계 뉴스
    briefing += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 세계 주요 이슈
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for news in world_news[:3]:
        briefing += format_news_item(news)
        briefing += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    # 국내 뉴스
    briefing += """
🇰🇷 대한민국 뉴스
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    for news in korea_news[:4]:
        briefing += format_news_item(news)
        briefing += "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"

    # 액션 아이템
    briefing += """
💡 오늘의 액션 아이템
"""
    for action in actions[:4]:
        briefing += f"☐ {action}\n"
    briefing += """→ "액션 추가: [항목]"으로 저장하세요

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
    briefing += f"⏰ 업데이트: {today.strftime('%Y-%m-%d')} ({weekday})\n"
    briefing += '💡 다음 뉴스: "뉴스 검색해줘" 입력\n'
    briefing += "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

    return briefing

# ============================================
# 5. 메인 함수 - 뉴스 브리핑 생성
# ============================================

def generate_news_briefing() -> str:
    """뉴스 브리핑 생성 메인 함수"""

    # 샘플 뉴스 데이터 (실제로는 웹 검색 결과 사용)
    world_news = [
        {
            "title": "트럼프, 유럽 8개국 관세 전격 철회 - NATO 합의 도출",
            "source": "서울경제",
            "date": "2026-02-04",
            "category": "세계",
            "score": 85,
            "analysis": "트럼프가 유럽 관세를 전격 철회했음. NATO 사무총장과 그린란드 및 북극 지역 미래에 관한 합의 틀을 마련한 게 이유임. 대서양 동맹이 최악의 충돌을 피하게 됐음.",
            "terms": "- 골든돔(Golden Dome): 미국의 미사일 방어 시스템 프로젝트\n- 상호관세: 상대국이 부과하는 관세율만큼 똑같이 부과하는 관세",
            "implications": "[업무] 미국-유럽 관계 안정은 글로벌 건설 프로젝트 발주 환경에 긍정적임\n[학업] 지정학적 리스크와 AI 기술 주권 경쟁이 대학원 연구 주제로 적합함",
            "brief_implication": "글로벌 건설 발주 환경 긍정적",
        },
        {
            "title": "2026년 AI 트렌드: 에이전틱 AI + 소버린 AI 시대 도래",
            "source": "SK텔레콤 뉴스룸",
            "date": "2026-02",
            "category": "AI/기술",
            "score": 95,
            "analysis": "2026년 AI는 스스로 판단하고 업무 수행하는 '에이전틱 AI'로 진화 중임. 각국이 AI 주권(소버린 AI) 확보 경쟁에 돌입했음. SKT는 500B 파라미터 규모의 'A.X K1' 공개했음.",
            "terms": "- 에이전틱 AI: 사람 개입 없이 스스로 판단하고 행동하는 자율형 AI\n- 소버린 AI: 국가 차원의 AI 기술 주권 확보 움직임\n- 500B 파라미터: 5천억 개 학습 매개변수, GPT-4 수준",
            "implications": "[업무] 에이전틱 AI가 HRD 분야에도 적용될 것임. 나누쌤 플랫폼에 자율 학습 추천 기능 검토 가능\n[학업] 고려대/연세대 대학원에서 에이전틱 AI 연구 동향 파악 필요",
            "brief_implication": "나누쌤 플랫폼 AI 기능 업그레이드 기회",
        },
    ]

    korea_news = [
        {
            "title": "2026년 건설업계 핵심 화두: '안전과 AI'",
            "source": "스타트업투데이",
            "date": "2026-02",
            "category": "건설",
            "score": 90,
            "analysis": "주요 건설사 신년사의 공통분모는 '안전'임. SK에코플랜트는 'AI 솔루션 공급 기업'으로 체질 전환 선언했음. AI를 잘 쓰는 기업과 못 쓰는 기업 간 격차가 생존을 가를 듯함.",
            "terms": "- 중대재해처벌법: 사업장 사망사고 발생 시 경영책임자를 처벌하는 법률",
            "implications": "[업무] 자이씨앤에이도 안전교육과 AI 역량 강화가 핵심 과제가 될 것임. 나누쌤 플랫폼에 안전교육 AI 콘텐츠 추가 검토\n[업무] 건설업 AI 전환 사례를 HRD 프로그램에 반영하면 차별화 가능",
            "brief_implication": "나누쌤 안전교육 AI 콘텐츠 기회",
        },
        {
            "title": "2026년 HRD 기업교육 트렌드: AX 시대, USE-CASE 창출이 핵심",
            "source": "에이블런/코멘토",
            "date": "2026-02",
            "category": "교육/HRD",
            "score": 95,
            "analysis": "2026년은 AI를 실무에 직접 적용하는 PBL 형태 교육이 확대됨. 전사 임직원 50%가 생성AI 변화를 이해하고 15%가 AI로 문제 해결 가능하면 조직 전체가 움직이기 시작함.",
            "terms": "- AX(AI Transformation): AI 전환, DX를 넘어 AI 기반 비즈니스 전환\n- PBL: 문제해결 중심 학습, 실제 업무 과제를 AI로 해결\n- LXP: AI 기반 학습경험 플랫폼",
            "implications": "[업무] 🔥 핵심! 나누쌤 플랫폼을 PBL 형태로 업그레이드하면 차별화 가능. USE-CASE 창출을 KPI로 설정 검토\n[학업] 이 트렌드를 대학원 포트폴리오에 반영하면 경쟁력 있음",
            "brief_implication": "나누쌤 PBL 업그레이드 기회",
        },
        {
            "title": "한일 정상회담 성공적 개최 - 셔틀외교 완전 정착",
            "source": "외교부",
            "date": "2026-01",
            "category": "한일관계",
            "score": 80,
            "analysis": "이재명 대통령과 다카이치 총리가 호류지에서 만났음. 경제안보·과학기술·사회문제 대응 협력 합의, 인도주의 협력도 강화됐음.",
            "terms": "- 호류지: 일본 나라현 세계 최고 목조 건축물, 한반도 기술 전파의 상징\n- 셔틀외교: 양국 정상이 번갈아 방문하는 정상외교 형태",
            "implications": "[가정] 🎌 한일관계 개선은 배우자와 공유할 만한 좋은 뉴스임\n[업무] 한일 경제협력 확대 시 GS건설/자이씨앤에이의 일본 관련 사업 기회 모니터링",
            "brief_implication": "배우자와 공유, 일본 사업 기회",
        },
        {
            "title": "웹소설 시장: 네이버 시리즈 vs 카카오페이지 경쟁 심화",
            "source": "업계 분석",
            "date": "2026-02",
            "category": "웹소설/콘텐츠",
            "score": 85,
            "analysis": "네이버는 웹툰-웹소설 미디어믹스 시너지를 극대화 중임. 무협지는 네이버에서 강세이며, 대작 무협 작가들이 네이버 독점으로 이동 추세임.",
            "terms": "- 미디어믹스: 웹소설→웹툰→드라마 등 다양한 매체로 확장",
            "implications": "[창작] 🔥 핵심! 네이버/카카오 동시 출간 전략이 유효함. 네이버는 무협 강세, 카카오는 로판/로맨스 강세 파악 필요\n[창작] 조아라 연재 작품의 장르가 어느 플랫폼에 적합한지 분석 필요",
            "brief_implication": "네이버/카카오 출간 전략 수립",
        },
    ]

    actions = [
        "나누쌤 플랫폼에 PBL 형태 AI 교육 콘텐츠 기획안 작성",
        "건설업 AI 전환 사례 벤치마킹 자료 수집",
        "웹소설 네이버/카카오 출간 전략 검토 (장르별 플랫폼 적합성)",
        "한일 정상회담 결과 배우자와 공유",
    ]

    return format_full_briefing(world_news, korea_news, actions)


if __name__ == "__main__":
    print(generate_news_briefing())
