FROM python:3.8.13

WORKDIR /app

COPY requirementes.txt requirementes.txt

RUN pip install -r requirementes.txt

COPY . .

EXPOSE 8000


CMD [ "gunicorn", "core.wsgi:application" , "--bind", "0.0.0.0:8000" ]
