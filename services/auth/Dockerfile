FROM python:3.12-alpine

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirement.txt,target=requirement.txt \
    pip install -r requirement.txt

EXPOSE 8001

CMD ["fastapi", "dev", "--host", "0.0.0.0", "--port", "8001"]