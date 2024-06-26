import aiohttp
import logging
from .utils import get_datetime_utc_string

log = logging.getLogger(__name__)


def prepare_data_for_request(amount, update_date):
    request_data = {
        "apply_rules": True,
        "fire_webhooks": True,
        "transactions": [
            {
                "amount": amount,
            }
        ],
    }

    if update_date:
        request_data["transactions"][0]["date"] = get_datetime_utc_string()

    return request_data


async def update_transaction(
    http_session: aiohttp.ClientSession,
    url: str,
    api_key: str,
    transaction_id: int,
    amount: int,
    update_date: bool,
):
    parsed_url = f"{url}/api/v1/transactions/{transaction_id}"
    data = prepare_data_for_request(amount, update_date)
    headers = {"Authorization": f"Bearer {api_key}"}

    try:
        resp = await http_session.put(parsed_url, json=data, headers=headers)
    except Exception as e:
        # Log it for debugging and then re-raise the exception
        log.debug(f"Failed to send request to firefly-iii, exception raised: {e}")
        raise e

    if not resp.ok:
        log.debug(f"Request failed, server sending {resp.status} code")
        raise RuntimeError(f"Server sending {resp.status} code")
