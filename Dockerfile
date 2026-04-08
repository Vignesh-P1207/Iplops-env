FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables (required by OpenEnv spec)
# These can be overridden at runtime via -e flags or HF Space secrets
ENV API_BASE_URL="https://api.openai.com/v1"
ENV MODEL_NAME="gpt-4o-mini"
ENV HF_TOKEN=""
ENV ENV_BASE_URL="http://localhost:8000"

EXPOSE 8000

# Bind to 0.0.0.0 required for HF Spaces and Docker networking
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
