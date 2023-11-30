FROM python:3.8 as compile
LABEL authors="vsobolev"

RUN pip install -U pip && pip install poetry==1.2.2
RUN python -m venv "/venv"
ENV VIRTUAL_ENV "/venv"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry install --no-root

COPY . /app/

FROM python:3.8 as runtime

WORKDIR /app

EXPOSE 8000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV "/venv"
ENV PATH $PATH:/venv/bin

COPY --from=compile /venv /venv

RUN echo ". /venv/bin/activate" >> "$HOME/.bashrc"

COPY --from=compile /app /app

RUN chmod 777 run.sh

ENTRYPOINT ["./run.sh"]

CMD ["runserver"]