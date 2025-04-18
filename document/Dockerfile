FROM python:3.12-slim

RUN mkdir document_service
WORKDIR /document_service

COPY ./requirements.txt /document_service

RUN pip3 install -r requirements.txt
   
COPY . .

CMD ["sh", "-c", "sleep 16; alembic upgrade head && python3 main.py"]
