import websockets
import aiohttp
import json
import logging

log = logging.getLogger(__name__)
base_url = "https://raw.githubusercontent.com/mansuf/firefly_iii-treasury.id-update/main/treasury.id-websocket-url.txt"


async def send_subscribe_gold_rate(ws: websockets.WebSocketClientProtocol):
    result = None
    log.debug("Sending gold-rate subscription to websocket")
    try:
        await ws.send(
            json.dumps(
                {
                    "data": {"auth": "", "channel": "gold-rate"},
                    "event": "pusher:subscribe",
                }
            )
        )
        result = json.loads(await ws.recv())
    except websockets.exceptions.ConnectionClosedError:
        return False

    event = result.get("event", "Unknown event")
    if event != "pusher_internal:subscription_succeeded":
        log.error(
            f"Expected event 'pusher_internal:subscription_succeeded', got {event!r}"
        )
        return False

    return True


async def create_websockets_connection(http_session: aiohttp.ClientSession):
    resp = await http_session.get(base_url)
    treasury_id_url = await resp.text()

    return websockets.connect(treasury_id_url)
