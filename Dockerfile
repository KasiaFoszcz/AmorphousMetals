# syntax=docker/dockerfile:1
FROM python:3.11-slim

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
        python3-poetry \
    && poetry install --no-root \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Add Python sources.
COPY --link metale_amorficzne/ /app/metale_amorficzne/

# Set the default environment.
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=False

# Run the Streamlit app.
EXPOSE ${STREAMLIT_SERVER_PORT}
HEALTHCHECK CMD curl --fail http://localhost:${STREAMLIT_SERVER_PORT}/_stcore/health
ENTRYPOINT ["poetry", "run", "streamlit", "run", "metale_amorficzne/Home.py"]
