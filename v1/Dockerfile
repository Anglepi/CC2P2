FROM python:3-buster

WORKDIR /ApiV1

COPY . .

RUN pip3 install -r dependencies.txt

CMD ["gunicorn", "-b", "0.0.0.0:8082", "api:app", "--reload"]