FROM python:3.9

WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=10000

EXPOSE 10000

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "10000"] 