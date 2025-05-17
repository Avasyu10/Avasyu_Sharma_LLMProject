FROM python:3.10.17-bookworm

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app
EXPOSE 5000
CMD ["flask", "--app", "app.main", "run", "--host=0.0.0.0", "--port=5000"]
ENV FLASK_APP=app.main