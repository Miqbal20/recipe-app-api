# Use the specified base image
FROM python:3.10.13-alpine

# Set a default value for the build-time argument
ARG DEV=false

# Set the environment variable based on the build-time argument
ENV DEV=${DEV}

# Copy files to the image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# Set working directory
WORKDIR /app

# Install dependencies based on the DEV environment variable
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt \
    && if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Set the PATH
ENV PATH="/py/bin:$PATH"

# Switch to the django-user user
USER django-user

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:8000"]