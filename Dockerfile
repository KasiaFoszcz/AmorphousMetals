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
    && pip install poetry \
    && poetry install --no-root --only main,streamlit \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Add example data and Python sources.
COPY --link data/ /app/data/
COPY --link metale_amorficzne/ /app/metale_amorficzne/

# Set the default environment.
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=False \
    STREAMLIT_SERVER_ENABLE_STATIC_SERVING=True \
    METAL_DATA_PATH=/app/data/

# Run the Streamlit app.
EXPOSE ${STREAMLIT_SERVER_PORT}
HEALTHCHECK CMD curl --fail http://localhost:${STREAMLIT_SERVER_PORT}/_stcore/health
ENTRYPOINT ["poetry", "run", "python3", "-m", "streamlit", "run", "metale_amorficzne/streamlit/Home.py"]
