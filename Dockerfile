FROM python:3.11-slim

WORKDIR /app

# ffmpeg 설치
RUN apt-get update && \
    apt-get install -y ffmpeg libopus-dev libffi-dev libnacl-dev && \
    rm -rf /var/lib/apt/lists/*

# poetry 설치
RUN pip install poetry
# 가상환경 미 생성
RUN poetry config virtualenvs.create false

# 의존 라이브러리 설치
COPY pyproject.toml poetry.lock ./

RUN poetry install --only main --no-root

# 소스코드 가져오기
COPY . .

CMD ["python", "-m","src"]