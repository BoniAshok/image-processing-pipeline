FROM python:3.11-slim

WORKDIR /app

# Install project dependencies
COPY requirements.txt pyproject.toml ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and install package
COPY src/ ./src/
COPY image-pipeline.py README.md ./
RUN pip install --no-cache-dir .

ENTRYPOINT ["image-pipeline"]
CMD ["--help"]
