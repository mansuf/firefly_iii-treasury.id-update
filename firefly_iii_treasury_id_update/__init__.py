"""
Update gold price from https://treasury.id (via websocket) to firefly-iii (https://firefly-iii.org) based how much grams you have
"""

# fmt: off
__version__ = "0.0.1"
__description__ = "Update gold price from https://treasury.id (via websocket) to firefly-iii (https://firefly-iii.org) based how much grams you have"
__author__ = "Rahman Yusuf"
__author_email__ = "danipart4@gmail.com"
__license__ = "MIT"
__repository__ = "mansuf/firefly_iii-treasury.id-update"
__url_repository__ = "https://github.com"
# fmt: on

import logging

logging.getLogger(__name__).addHandler(logging.NullHandler())
