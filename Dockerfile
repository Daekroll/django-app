FROM python:3.11

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --upgrade pip "poetry==1.8.4"
RUN poetry config virtualenvs.create false --local
COPY pyproject.tomal poetry.log ./
RUN poetry install

COPY ./misite .

CMD ["gunicorn", "misite.wsgi:application", "--bind", "0.0.0.0:8000"]