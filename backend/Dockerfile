FROM python:3.12-slim

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/user/app/
ENV PYTHONPATH=/home/user/app/

COPY pyproject.toml poetry.lock /home/user/app/
RUN pip install 'uvicorn[standard]'
RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false
RUN poetry install --with dev --no-root --no-interaction --no-ansi


RUN mkdir -p /home/user/app/uploaded_files/ && chown -R user:user /home/user/app/uploaded_files/

USER user

COPY --chown=user:user . /home/user/app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
