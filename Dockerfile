# syntax=docker/dockerfile:1
FROM python:3.12-slim

LABEL org.opencontainers.image.title="Amorphous Metals Streamlit app" \
      org.opencontainers.image.authors="Marek Pikuła <marek@serenitycode.dev>, Katarzyna Foszcz <kasia@foszcz.co>" \
      org.opencontainers.image.licenses="GPL-3.0-or-later"

# Add Poetry project.
WORKDIR /app
COPY poetry.lock poetry.toml pyproject.toml /app/

# Install Python project dependencies.
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
    && pip install poetry poetry-dynamic-versioning \
    # Needed for dynamic versioning to initialize correctly on install.
    && git init \
    && poetry install --no-root --only main,streamlit \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Set the default environment.
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=False \
    STREAMLIT_SERVER_ENABLE_STATIC_SERVING=True \
    METAL_DATA_PATH=/app/data/ \
    STREAMLIT_ANALYTICS_STORE=/app/persist/analytics.json \
    STREAMLIT_ANALYTICS_PASSWORD=

# Add example data and Python sources.
COPY --link data/ ${METAL_DATA_PATH}
COPY --link amorphous_metals/ /app/amorphous_metals/

# Install with a proper package version.
RUN --mount=type=bind,source=.git,target=/app/.git \
    poetry install --only main,streamlit

# Add non-root user, ensure proper ownership, and add data/cache directory as a volume.
RUN useradd -MU -d /app streamlit \
    && mkdir -p ${METAL_DATA_PATH} /app/.streamlit/cache /app/persist \
    && chown -R streamlit:streamlit /app
VOLUME ${METAL_DATA_PATH} /app/.streamlit/cache

# Run the Streamlit app.
USER streamlit
EXPOSE ${STREAMLIT_SERVER_PORT}
HEALTHCHECK CMD curl --fail http://localhost:${STREAMLIT_SERVER_PORT}/_stcore/health
ENTRYPOINT ["poetry", "run", "python3", "-m", "streamlit", "run", "amorphous_metals/streamlit/Home.py"]
