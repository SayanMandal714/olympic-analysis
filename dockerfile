FROM python:3.10
WORKDIR /app
COPY /olympic-analysis /app
Run pip install -r requirement.txt
ENTRYPOINT ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]



