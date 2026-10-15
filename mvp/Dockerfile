# Build context is the repository root, because the image also installs src/core and src/agents (ADR 0006, M1 and M4):
#   docker build -f mvp/Dockerfile -t zavaforward-mvp:ci .
# python:3.12-slim-bookworm, pinned by digest (resolved 2026-10-08). Bump deliberately and re-run the tests.
FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS build
WORKDIR /build
COPY src/build-requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r build-requirements.txt
COPY src/core/pyproject.toml ./core/pyproject.toml
COPY src/core/src ./core/src
COPY src/agents/pyproject.toml ./agents/pyproject.toml
COPY src/agents/src ./agents/src
RUN pip wheel --no-cache-dir --no-deps --no-build-isolation --wheel-dir /wheels ./core ./agents

FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
# libltdl7 and libkrb5-3 are the runtime libraries the Azure SQL driver (mssql-python, bundled ODBC Driver 18) loads.
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends libltdl7 libkrb5-3 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app /data /state && chown 10001:10001 /state
WORKDIR /app
COPY mvp/requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r requirements.txt && rm requirements.txt
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels \
    pip install --no-cache-dir --no-index --no-deps /wheels/*.whl
COPY mvp/zavaforward_mvp ./zavaforward_mvp
COPY mvp/law ./law
COPY src/agents/evals/ai_priority_golden.json ./evals/ai_priority_golden.json
COPY mvp/web ./web
RUN chmod -R a+rX ./web
USER 10001
# No working data is baked into the image. Mount the dataset at /data and a writable volume at /state.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PORT=8088 ZF_BIND=0.0.0.0 ZF_DATA=/data/zavaforward.json ZF_STATE=/state ZF_AI_GOLDEN=/app/evals/ai_priority_golden.json
EXPOSE 8088
HEALTHCHECK --interval=30s --timeout=3s CMD ["python", "-c", "import os,urllib.request;urllib.request.urlopen('http://127.0.0.1:'+os.environ['PORT']+'/healthz',timeout=2)"]
CMD ["python", "-m", "zavaforward_mvp.server"]
