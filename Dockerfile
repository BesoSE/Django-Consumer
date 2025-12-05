FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
RUN python -m venv /opt/venv
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . .
CMD . venv/bin/activate