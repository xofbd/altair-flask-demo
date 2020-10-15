FROM python:3.8.6-slim
COPY requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt
COPY . /app
WORKDIR /app
EXPOSE 5000
CMD ["bin/run_app", "0.0.0.0"]
