from datetime import datetime
from zoneinfo import ZoneInfo

from config import (
    TIMEZONE,
    DAILY_REPORT_SHEET,
    WEEKLY_REPORT_SHEET,
)

from sheets import (
    get_records,
    append_row,
)

from weekly_summary import (
    get_last_week_range,
    filter_reports,
    summarize_weekly,
)


def main():
    print("주간 리포트 생성 시작")

    start_date, end_date = (
        get_last_week_range()
    )

    print(
        f"대상 기간: "
        f"{start_date} ~ {end_date}"
    )

    daily_records = get_records(
        DAILY_REPORT_SHEET
    )

    review_records = get_records(
        "구글플레이 리뷰"
    )

    weekly_reports = filter_reports(
        daily_records,
        start_date,
        end_date,
    )

    review_texts = []

    for row in review_records:
        date = str(
            row.get("작성일", "")
        ).strip()

        review = str(
            row.get("번역문", "")
        ).strip()

        score = str(
            row.get("평점", "")
        ).strip()

        if (
            start_date <= date <= end_date
            and review
        ):
            review_texts.append(
                f"[{score}점] {review}"
            )

    report_text = summarize_weekly(
        start_date=start_date,
        end_date=end_date,
        daily_reports=weekly_reports,
        review_reports=review_texts[:200],
    )

    created_at = datetime.now(
        ZoneInfo(TIMEZONE)
    ).strftime("%Y-%m-%d %H:%M:%S")

    append_row(
        WEEKLY_REPORT_SHEET,
        [
            f"{start_date} ~ {end_date}",
            report_text,
            created_at,
        ]
    )

    print("주간 리포트 저장 완료")


if __name__ == "__main__":
    main()
