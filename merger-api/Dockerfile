# This Dockerfile uses Python Docker Official image.
ARG PYTHON_VERSION=3.14
FROM python:${PYTHON_VERSION}-alpine AS builder
WORKDIR /app

# Copy requirements and install the dependencies for the environment (defaults to prod)
COPY requirements/ requirements/
ARG REQUIRE_ENV=prod
RUN pip install --no-cache-dir --prefix=/install -r requirements/${REQUIRE_ENV}.txt

# Production stage
FROM python:${PYTHON_VERSION}-alpine
WORKDIR /app

# Prevent Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
# Keeps Python from buffering stdout and stderr.
# To avoid situations where the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

# Copy the built dependencies from the builder stage
COPY --from=builder /install /usr/local

# Copy the application code into the container.
COPY . .

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistant" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on and run the application.
EXPOSE 8000
CMD ["python3", "-m", "uvicorn", "app.main:app", "--host=0.0.0.0", "--port=8000"]
