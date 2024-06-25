# firefly_iii-treasury.id-update

Update gold price from https://treasury.id (via websocket) to firefly-iii (https://firefly-iii.org) based how much grams you have

## Installation

Via PyPI

```sh
pip install firefly_iii-treasury.id-update
```

Via Docker

```sh
docker pull mansuf/firefly_iii-treasury.id-update
```

## Usage

**NOTE:** While this app provide CLI arguments that you can use, it's highly recommended to use environments instead

### Docker usage

```sh
# With environments
docker run --env-file .env mansuf/firefly_iii-treasury.id-update

# With CLI arguments
docker run mansuf/firefly_iii-treasury.id-update --api-key "firefly-iii api key" --transaction-id "firefly-iii transaction id" --url "firefly-iii base url" --grams-gold "3"
```

### PyPI usage

```sh
# With environments 
firefly-iii-treasury-update --load-dotenv

# With CLI arguments
firefly-iii-treasury-update --api-key "firefly-iii api key" --transaction-id "firefly-iii transaction id" --url "firefly-iii base url" --grams-gold "3"

# If you having encountering error "firefly-iii-treasury-update" command not found
# you can do this instead

# For Windows
py -3 -m firefly_iii_treasury_id_update --load-dotenv .env

# For Linux / Mac OS
python3 -m firefly_iii_treasury_id_update --load-dotenv
```
