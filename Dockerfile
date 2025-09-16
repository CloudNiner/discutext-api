FROM python:3.12-slim

WORKDIR /app

# Install uv in a separate step to leverage Docker's layer caching.
RUN pip install uv

COPY pyproject.toml ./
RUN uv pip install --system .

# Copy application code into the container
COPY app.py ./app.py
COPY ./discutext_api ./discutext_api

EXPOSE 5050

CMD ["python", "app.py"]
