from python:3.10
RUN apt-get update -y
WORKDIR /app
RUN python -m pip install --upgrade pip
COPY . /app
Run pip install -r req.txt
ENTRYPOINT["python"]
CMD["app.py"]



