FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"

CMD [ "python", "./main.py" ]
