FROM python:3.12-slim

RUN mkdir account_service
WORKDIR /account_service

COPY ./requirements.txt /account_service

RUN pip3 install -r requirements.txt
    
# RUN mkdir -p certificates \
#     && openssl genpkey -algorithm RSA -out certificates/private_key.pem -pkeyopt rsa_keygen_bits:2048  \
#     && openssl rsa -pubout -in certificates/private_key.pem -out certificates/public_key.pem

COPY . .

CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --reload"]
