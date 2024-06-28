from datetime import datetime


def get_selling_price(data: dict) -> int:
    selling_rate = data["selling_rate"]
    selling_rate = selling_rate.replace(".", "")
    return int(selling_rate)


def get_datetime_utc_string():
    dt = datetime.now()
    return dt.isoformat()


def validate_bool(val):
    if isinstance(val, str):
        value = val.strip().lower()

        # Is it 1 or 0 ?
        try:
            return bool(int(value))
        except ValueError:
            pass

        # This is dumb
        if value == "true":
            return True
        elif value == "false":
            return False
        else:
            raise ValueError(f"'{val}' is not valid boolean value")
    else:
        return bool(val)
