FROM python:3.12-slim

RUN mkdir hospital_service
WORKDIR /hospital_service

COPY ./requirements.txt /hospital_service

RUN pip3 install -r requirements.txt
    
COPY . .

CMD ["sh", "-c", "sleep 12; alembic upgrade head && python3 main.py"]
