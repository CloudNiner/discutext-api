FROM python:3.14-slim

WORKDIR /app

# Install uv in a separate step to leverage Docker's layer caching.
RUN pip install uv

COPY pyproject.toml ./
RUN uv pip install --system .
RUN uv pip install --system . --group deploy

# Copy application code into the container
COPY app.py ./app.py
COPY ./discutext_api ./discutext_api

EXPOSE 5050

CMD ["gunicorn", "-w", "2", "-t", "10", "-b", "0.0.0.0:5050", "--access-logfile", "-", "app:app"]
