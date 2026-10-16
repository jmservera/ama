# Build context is the src/ folder: docker build -f src/orchestrator/Dockerfile src
# python:3.12-slim-bookworm, latest digest verified 2026-10-16. Bump deliberately and re-run the tests.
FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS build
WORKDIR /build
COPY build-requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r build-requirements.txt
COPY core/pyproject.toml ./core/pyproject.toml
COPY core/src ./core/src
COPY orchestrator/pyproject.toml ./orchestrator/pyproject.toml
COPY orchestrator/src ./orchestrator/src
RUN pip wheel --no-cache-dir --no-deps --no-build-isolation --wheel-dir /wheels ./core ./orchestrator

FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
# libltdl7 and libkrb5-3 are the runtime libraries the Azure SQL driver (mssql-python, bundled ODBC Driver 18) loads.
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && apt-get install -y --no-install-recommends libltdl7 libkrb5-3 \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app /data /state && chown 10001:10001 /state
WORKDIR /app
COPY orchestrator/requirements.txt .
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels \
    pip install --no-cache-dir --require-hashes -r requirements.txt \
    && pip install --no-cache-dir --no-index --no-deps /wheels/*.whl \
    && rm requirements.txt
USER 10001:10001
# No working data is baked into the image. Mount the dataset at /data and a writable volume at /state.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ZF_DATA=/data/zavaforward.json ZF_STATE=/state
CMD ["python", "-m", "zava_forward.orchestrator"]
