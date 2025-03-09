FROM python:3

RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean

COPY . /yt_com_bot/
WORKDIR /yt_com_bot/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python3 -m nltk.downloader stopwords

CMD python3 bot.py

## docker run --rm -d --publish 8000:8000 85d5821d784d