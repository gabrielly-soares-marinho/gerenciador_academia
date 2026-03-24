FROM python:3.10

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

WORKDIR /app/backend

CMD ["python", "app.py"]