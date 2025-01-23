FROM python:3.13

EXPOSE 5000

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]

# docker build -t  flask-rest-api .

# docker run -dp 5005:5000 flask-rest-api