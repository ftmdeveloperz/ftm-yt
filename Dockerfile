FROM python:3.10

WORKDIR /app

COPY . .

RUN apt update && apt install -y ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install -U yt-dlp
RUN pip install -r requirements.txt

CMD ["python", "bot.py"]
