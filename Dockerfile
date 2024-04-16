# Use a specific Alpine-based base image
FROM python:3.12.2-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /app

# Install system dependencies required for common Python packages
RUN apk update \
    && apk add --no-cache gcc musl-dev libffi-dev postgresql-dev curl \
    && rm -rf /var/cache/apk/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Copy application code
COPY . .

# Create and switch to a non-root user
RUN addgroup -S appuser && adduser -S appuser -G appuser \
    && chown -R appuser:appuser /app
USER appuser

# Expose port 8080 for the application
EXPOSE 8080

# Command to run the application using Gunicorn
CMD ["waitress-serve", "--port=8080", "app:app"]

# Healthcheck to make sure the container is ready
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1