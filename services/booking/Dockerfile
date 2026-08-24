FROM python:3.12-alpine

WORKDIR /code

COPY requirements.txt requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt

COPY . .

EXPOSE 8003

CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8003"]