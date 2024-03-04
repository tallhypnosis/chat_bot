FROM python:3.9

RUN pip install -r requirements.txt

COPY . /app

CMD ["python", "app.py"]