FROM python:3.11.5-slim

COPY requirements.txt .

COPY ./main/ServerMQTT.py .

COPY ./main/model.joblib .

RUN python3 -m pip install -r requirements.txt --no-cache-dir

COPY ./main/start.sh .
RUN chmod +x /start.sh

COPY . .

EXPOSE 5001

ENV FLASK_APP=./main/App_flask.py
ENV FLASK_ENV=development

CMD ["/start.sh"]
