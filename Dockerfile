FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy content of current directory in working directory
COPY . /app

# Install requirements
RUN pip install -r requirements.txt

# Copy custom index
COPY streamlit_app/index.html /usr/local/lib/python3.11/site-packages/streamlit/static/index.html

# Expose port 8080 to world outside of the container
EXPOSE 8080

# Run streamlit app
ENTRYPOINT ["streamlit", "run", "App.py", "--server.port=8080", "--server.address=0.0.0.0"]