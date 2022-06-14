FROM python:3.7.10
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ADD . /app/
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5001"]