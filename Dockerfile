FROM python:3.10.2-slim-buster

RUN apt -y update
RUN apt -y upgrade
RUN apt -y install --no-install-recommends ipmitool

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot
COPY ipmicommands.py /usr/src/bot
COPY main.py /usr/src/bot

RUN pip install --no-cache-dir python-telegram-bot

CMD ["python", "main.py"]
