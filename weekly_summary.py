from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from openai import OpenAI

from config import (
    OPENAI_API_KEY,
    OPENAI_MODEL,
    TIMEZONE,
)


client = OpenAI(
    api_key=OPENAI_API_KEY
)


def get_last_week_range():
    now = datetime.now(
        ZoneInfo(TIMEZONE)
    )

    monday = now - timedelta(
        days=now.weekday() + 7
    )

    sunday = monday + timedelta(days=6)

    return (
        monday.strftime("%Y-%m-%d"),
        sunday.strftime("%Y-%m-%d"),
    )


def filter_reports(records, start_date, end_date):
    results = []

    for row in records:
        date = str(
            row.get("요약일자", "")
        ).strip()

        report = str(
            row.get("일별 리포트", "")
        ).strip()

        if not date or not report:
            continue

        if start_date <= date <= end_date:
            results.append({
                "date": date,
                "report": report,
            })

    return results


def build_prompt(
    start_date,
    end_date,
    daily_reports,
    review_reports,
):
    return f"""
너는 게임 운영 PM 리포트를 작성하는 AI다.

아래는 언디셈버의
주간 운영 데이터다.

기간:
{start_date} ~ {end_date}

목표:
- 주간 흐름 분석
- 반복 VOC 정리
- 운영 리스크 파악
- 다음 주 액션 제안

반드시 아래 형식을 지켜라.

📊 언디셈버 주간 운영 리포트
({start_date} ~ {end_date})

[1. 주간 전체 요약]

[2. 주요 이슈 TOP 5]

[3. 채널별 분석]
- 디스코드:
- 언디셈버_KR_부정 동향:
- 언디셈버_KR_플로어 동향:
- 구글플레이 리뷰:

채널별 분석에서는 반드시 아래 채널만 사용한다.
- 디스코드
- 언디셈버_KR_부정 동향
- 언디셈버_KR_플로어 동향
- 구글플레이 리뷰

데이터에 없는 채널명, 수치, 전주 대비 증감률은 생성하지 않는다.

[4. 구글 리뷰 분석]

[5. 유저 니즈 분석]

====================

[일별 운영 리포트]

{daily_reports}

====================

[구글 리뷰 데이터]

{review_reports}
"""


def summarize_weekly(
    start_date,
    end_date,
    daily_reports,
    review_reports,
):
    prompt = build_prompt(
        start_date,
        end_date,
        daily_reports,
        review_reports,
    )

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": "게임 운영 분석 전문가"
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()
