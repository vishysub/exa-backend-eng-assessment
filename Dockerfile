FROM python:3.9


WORKDIR /code

COPY requirements.txt /code/

RUN pip install -r requirements.txt

COPY . .



EXPOSE 8000

CMD ["uvicorn", "apis.index:app", "--host", "0.0.0.0"]