FROM python:3.12.3-slim

WORKDIR /app

COPY requirements.txt /app


RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . /app/

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
