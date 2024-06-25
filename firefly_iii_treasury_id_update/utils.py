from datetime import datetime


def get_selling_price(data: dict) -> int:
    selling_rate = data["selling_rate"]
    selling_rate = selling_rate.replace(".", "")
    return int(selling_rate)


def get_datetime_utc_string():
    dt = datetime.now()
    return dt.isoformat()
