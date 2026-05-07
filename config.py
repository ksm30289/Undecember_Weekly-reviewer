import os
import json


def required(name):
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"환경변수 누락: {name}")
    return v


SPREADSHEET_ID = required("SPREADSHEET_ID")

GOOGLE_SERVICE_ACCOUNT_JSON = json.loads(
    required("GOOGLE_SERVICE_ACCOUNT_JSON")
)

OPENAI_API_KEY = required("OPENAI_API_KEY")

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-4o-mini"
)

DAILY_REPORT_SHEET = os.getenv(
    "DAILY_REPORT_SHEET",
    "일별 동향 요약"
)

WEEKLY_REPORT_SHEET = os.getenv(
    "WEEKLY_REPORT_SHEET",
    "주간 동향 요약"
)

TIMEZONE = os.getenv(
    "TIMEZONE",
    "Asia/Seoul"
)
