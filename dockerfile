from python:3.10
RUN apt-get update -y
WORKDIR /app
RUN python -m pip install --upgrade pip
COPY /olympic-analysis /app
Run pip install -r req.txt
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]



