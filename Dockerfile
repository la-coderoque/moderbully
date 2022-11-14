FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1
WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
