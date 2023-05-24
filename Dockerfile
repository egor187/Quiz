FROM python:3.11

WORKDIR /usr/src/app
COPY ./requirements ./requirements

RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r ./requirements/dev.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]