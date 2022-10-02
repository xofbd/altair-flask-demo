FROM python:3.9.2-slim
COPY requirements.txt /tmp
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc
RUN pip install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["bin/run", "-o", "0.0.0.0", "dev"]
