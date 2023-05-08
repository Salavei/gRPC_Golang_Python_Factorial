FROM python:3.9-alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install -r requirements.txt
RUN pip install uvicorn

COPY . .

CMD ["uvicorn", "main.main:app", "--reload", "--host", "0.0.0.0", "--port", "6000"]


