#!/bin/bash
# Claude Code 컨텍스트 윈도우 상태 표시줄

input=$(cat)

# JSON 파싱
CONTEXT_SIZE=$(echo "$input" | jq -r '.context_window.context_window_size // 200000')
USAGE=$(echo "$input" | jq '.context_window.current_usage // null')

# ANSI 색상 코드
GREEN="\033[32m"
YELLOW="\033[33m"
RED="\033[31m"
RESET="\033[0m"
BOLD="\033[1m"

# 진행률 바 문자
FILLED="█"
EMPTY="░"
BAR_WIDTH=15

if [ "$USAGE" != "null" ] && [ -n "$USAGE" ]; then
    # 현재 사용량 계산
    INPUT_TOKENS=$(echo "$USAGE" | jq '.input_tokens // 0')
    CACHE_CREATE=$(echo "$USAGE" | jq '.cache_creation_input_tokens // 0')
    CACHE_READ=$(echo "$USAGE" | jq '.cache_read_input_tokens // 0')
    OUTPUT_TOKENS=$(echo "$USAGE" | jq '.output_tokens // 0')

    CURRENT_TOKENS=$((INPUT_TOKENS + OUTPUT_TOKENS))
    PERCENT=$((CURRENT_TOKENS * 100 / CONTEXT_SIZE))

    # K 단위로 변환
    CURRENT_K=$(awk "BEGIN {printf \"%.1f\", $CURRENT_TOKENS / 1000}")
    TOTAL_K=$(awk "BEGIN {printf \"%.0f\", $CONTEXT_SIZE / 1000}")

    # 색상 결정
    if [ "$PERCENT" -ge 100 ]; then
        COLOR=$RED
        STATUS="압축됨"
    elif [ "$PERCENT" -ge 80 ]; then
        COLOR=$RED
        STATUS="${PERCENT}%"
    elif [ "$PERCENT" -ge 50 ]; then
        COLOR=$YELLOW
        STATUS="${PERCENT}%"
    else
        COLOR=$GREEN
        STATUS="${PERCENT}%"
    fi

    # 진행률 바 생성
    if [ "$PERCENT" -gt 100 ]; then
        FILLED_COUNT=$BAR_WIDTH
    else
        FILLED_COUNT=$((PERCENT * BAR_WIDTH / 100))
    fi
    EMPTY_COUNT=$((BAR_WIDTH - FILLED_COUNT))

    BAR=""
    for ((i=0; i<FILLED_COUNT; i++)); do
        BAR+="$FILLED"
    done
    for ((i=0; i<EMPTY_COUNT; i++)); do
        BAR+="$EMPTY"
    done

    # 남은 토큰 계산
    REMAINING=$((CONTEXT_SIZE - CURRENT_TOKENS))
    if [ "$REMAINING" -lt 0 ]; then
        REMAINING=0
    fi
    REMAINING_K=$(awk "BEGIN {printf \"%.1f\", $REMAINING / 1000}")

    # 출력
    echo -e "${BOLD}컨텍스트${RESET} ${COLOR}${BAR}${RESET} ${COLOR}${STATUS}${RESET} (${CURRENT_K}K/${TOTAL_K}K) 남음:${REMAINING_K}K"
else
    # 초기 상태
    BAR=""
    for ((i=0; i<BAR_WIDTH; i++)); do
        BAR+="$EMPTY"
    done
    TOTAL_K=$(awk "BEGIN {printf \"%.0f\", $CONTEXT_SIZE / 1000}")

    echo -e "${BOLD}컨텍스트${RESET} ${GREEN}${BAR}${RESET} ${GREEN}0%${RESET} (0K/${TOTAL_K}K) 남음:${TOTAL_K}K"
fi
