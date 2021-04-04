FROM python:3.7

RUN pip install pytelegrambotapi emojis flask
# cryptography==3.1.1

RUN mkdir /app
COPY TeleTeller.py /app
WORKDIR /app

CMD python TeleTeller.py
