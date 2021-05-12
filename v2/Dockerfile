FROM python:3-buster

WORKDIR /ApiV2

COPY . .

RUN pip3 install -r requeriments.txt

CMD ["gunicorn", "-b", "0.0.0.0:8083", "api:app", "--reload"]