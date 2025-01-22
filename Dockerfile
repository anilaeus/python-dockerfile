FROM python:3.13

EXPOSE 5000

WORKDIR /app

RUN pip install flask

COPY . .

CMD ["flask", "run", "--host", "0.0.0.0"]

# docker build -t  flask-rest-api .

# docker run -p 5003:5002 flask-rest-api