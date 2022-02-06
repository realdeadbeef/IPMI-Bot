FROM python:3.10.2-slim-buster

RUN apt update -y
RUN apt upgrade -y
RUN apt install ipmitool -y

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot
COPY ipmicommands.py /usr/src/bot
COPY main.py /usr/src/bot

RUN pip install --no-cache-dir python-telegram-bot

CMD ["python", "main.py"]