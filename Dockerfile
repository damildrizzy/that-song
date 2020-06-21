FROM python:3.7-alpine

COPY app/config.py /app/
COPY app/video.py /app/
COPY app/utils.py /app/
COPY app/app.py /app/
COPY requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app
CMD ["python3", "app.py"]