FROM python:3.12-slim

RUN mkdir account_service
WORKDIR /account_service

COPY ./requirements.txt /account_service

RUN pip3 install -r requirements.txt
    

COPY . .

CMD ["sh", "-c", "sleep 10; alembic upgrade head && python3 main.py"]
