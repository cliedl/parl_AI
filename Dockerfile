FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:0.5.26 /uv /uvx /bin/

# Set working directory
WORKDIR /app

# Download and unzip chroma db
RUN apt-get update && apt-get install -y wget unzip && \
    mkdir -p /app/data/manifestos/chroma && \
    wget -O openai.zip "https://huggingface.co/datasets/cliedl/electify/resolve/main/openai.zip?download=true" && \
    unzip openai.zip -d /app/data/manifestos/chroma/ && rm openai.zip

# Copy content of current directory in working directory
COPY . /app

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy custom index
COPY streamlit_app/index.html /usr/local/lib/python3.11/site-packages/streamlit/static/index.html

# Expose port 8080 to world outside of the container
EXPOSE 8080

# Add non-root user
RUN useradd -m appuser && chmod -R 755 /app && chown -R appuser:appuser /app

# Switch to newly-created user account with read-only rights
USER appuser

# Run streamlit app
ENTRYPOINT ["uv", "run", "streamlit", "run", "App.py", "--server.port=8080", "--server.address=0.0.0.0"]