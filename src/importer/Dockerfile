# Build context is the src/ folder: docker build -f src/importer/Dockerfile src
# python:3.12-slim-bookworm, pinned by digest (resolved 2026-10-08). Bump deliberately and re-run the tests.
FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS build
WORKDIR /build
COPY build-requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r build-requirements.txt
COPY core/pyproject.toml ./core/pyproject.toml
COPY core/src ./core/src
COPY importer/pyproject.toml ./importer/pyproject.toml
COPY importer/src ./importer/src
RUN pip wheel --no-cache-dir --no-deps --no-build-isolation --wheel-dir /wheels ./core ./importer

FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app /data /state && chown 10001:10001 /state
WORKDIR /app
COPY importer/requirements.txt .
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels \
    pip install --no-cache-dir --require-hashes -r requirements.txt \
    && pip install --no-cache-dir --no-index --no-deps /wheels/*.whl \
    && rm requirements.txt
USER 10001
# No working data is baked into the image. Mount the dataset at /data and a writable volume at /state.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ZF_DATA=/data/zavaforward.json ZF_STATE=/state
CMD ["python", "-m", "zava_forward.importer"]
