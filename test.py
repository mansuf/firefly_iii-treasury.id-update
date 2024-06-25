import asyncio
import logging
import dotenv
from firefly_iii_treasury_id_update.main import run_main

dotenv.load_dotenv()


def setup_logging(name_module, verbose=False):
    log = logging.getLogger(name_module)
    handler = logging.StreamHandler()
    fmt = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(fmt)
    log.addHandler(handler)
    if verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)
    return log


setup_logging("firefly_iii_treasury_id_update", verbose=True)

asyncio.run(run_main())
