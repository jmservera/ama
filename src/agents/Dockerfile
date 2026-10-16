# Build context is the src/ folder: docker build -f src/agents/Dockerfile src
# The agents identity has no database or blob access (ADR 0001): the core is installed without the sql or blob extras.
# python:3.12-slim-bookworm, pinned by digest (resolved 2026-10-08). Bump deliberately and re-run the tests.
FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258 AS build
WORKDIR /build
COPY build-requirements.txt .
RUN pip install --no-cache-dir --require-hashes -r build-requirements.txt
COPY core/pyproject.toml ./core/pyproject.toml
COPY core/src ./core/src
COPY agents/pyproject.toml ./agents/pyproject.toml
COPY agents/src ./agents/src
RUN pip wheel --no-cache-dir --no-deps --no-build-isolation --wheel-dir /wheels ./core ./agents

FROM python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258
RUN apt-get update && apt-get upgrade -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --uid 10001 --no-create-home --shell /usr/sbin/nologin app \
    && mkdir -p /app /data /state && chown 10001:10001 /state
WORKDIR /app
RUN --mount=type=bind,from=build,source=/wheels,target=/wheels \
    pip install --no-cache-dir --no-index --no-deps /wheels/*.whl
COPY container-entrypoint.py /usr/local/bin/container-entrypoint.py
USER 10001:10001
# No working data is baked into the image. Mount the dataset at /data and a writable volume at /state.
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 ZF_DATA=/data/zavaforward.json ZF_STATE=/state
ENTRYPOINT ["python", "/usr/local/bin/container-entrypoint.py"]
CMD ["python", "-m", "zava_forward.agents"]
