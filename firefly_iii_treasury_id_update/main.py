import aiohttp
import os
import logging
import websockets
import json
import time

from . import __version__, __repository__, __url_repository__
from .treasury import create_websockets_connection, send_subscribe_gold_rate
from .exceptions import (
    WebsocketConnectionError,
    ConnectionClosedError,
    MissingArguments,
)
from .firefly_iii import update_transaction
from .utils import get_selling_price

log = logging.getLogger(__name__)


def get_http_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(
        headers={
            "User-Agent": f"firefly_iii-treasury.id-update v{__version__} ({__url_repository__}/{__repository__})"
        }
    )


async def _run_main(http_session, grams_gold, api_key, transaction_id, firefly_iii_url):
    log.info("Establishing websocket connection")
    websocket_conn = await create_websockets_connection(http_session)
    async with websocket_conn as ws:
        data = json.loads(await ws.recv())

        event = data.get("event", "Unknown event")
        if event != "pusher:connection_established":
            log.error(f"Expected event 'pusher:connection_established', got {event!r}")
            raise WebsocketConnectionError(
                "Failed to establish websocket connection to treasury.id"
            )

        success = await send_subscribe_gold_rate(ws)
        if not success:
            raise WebsocketConnectionError(
                "Failed to send subscription to websocket connection"
            )

        log.info("Connected to websocket, waiting for gold-rate event from websocket")
        while True:
            try:
                data = json.loads(await ws.recv())
            except websockets.exceptions.ConnectionClosedError:
                raise ConnectionClosedError(
                    "Failed to retrive data from websocket connection"
                )

            event = data.get("event", "Unknown event")

            if event != "gold-rate-event":
                log.debug(
                    f"Expected event 'gold-rate-data', got {event!r} (data: {data}), ignoring..."
                )
                continue

            data = json.loads(data["data"])
            selling_price = get_selling_price(data)
            amount = int(selling_price * grams_gold)

            # TODO: Create update request to REST API firefly-iii
            log.info(
                f"Got gold-rate event from websocket, selling price = {selling_price}, updating to firefly-iii"
            )
            await update_transaction(
                http_session=http_session,
                url=firefly_iii_url,
                api_key=api_key,
                transaction_id=transaction_id,
                amount=amount,
            )
            log.info(
                f"Successfully update transaction id = {transaction_id} with amount {amount}"
            )


async def run_main():
    http_session = get_http_session()

    api_key = os.environ.get("FIREFLY_III_API_KEY")
    transaction_id = os.environ.get("FIREFLY_III_TRANSACTION_ID")
    firefly_iii_url = os.environ.get("FIREFLY_III_URL")
    grams_gold = os.environ.get("GRAMS_GOLD")

    if api_key is None:
        raise MissingArguments("there is no FIREFLY_III_API_KEY in environment")
    elif transaction_id is None:
        raise MissingArguments("there is no FIREFLY_III_TRANSACTION_ID in environment")
    elif firefly_iii_url is None:
        raise MissingArguments("there is no FIREFLY_III_URL in environment")
    elif grams_gold is None:
        raise MissingArguments("there is no GRAMS_GOLD in environment")

    # Determine if grams_gold is a url location, a file, or just hardcoded numbers
    if grams_gold.startswith("http"):
        res = await http_session.get(grams_gold)
        grams_gold = float(await res.text())
    elif os.path.exists(grams_gold):
        with open(grams_gold, "r") as o:
            grams_gold = float(o.read())
    else:
        grams_gold = float(grams_gold)

    while True:
        try:
            await _run_main(
                http_session, grams_gold, api_key, transaction_id, firefly_iii_url
            )
        except Exception as e:
            log.error(
                f"Connection error from websocket (exception raised: {e}), retrying in 3 seconds..."
            )
            time.sleep(3)
