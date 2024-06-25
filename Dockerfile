FROM python:3.11

COPY . /app
WORKDIR /app

# Install firefly_iii_treasury_id_update
RUN pip install --upgrade pip
RUN pip install .

WORKDIR /downloads

ENTRYPOINT [ "firefly-iii-treasury-update" ]

CMD [ "--help" ]