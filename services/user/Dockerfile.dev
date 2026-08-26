FROM python:3.12-alpine

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    pip install -r requirements.txt

EXPOSE 8001

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8001"]