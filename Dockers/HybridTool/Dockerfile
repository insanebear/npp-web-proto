# Dockerfile for HybridTool PyMC Fargate Task
# Python environment with PyMC and JAX for Bayesian inference

FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY server/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY server/ /app/server/
COPY Dockers/HybridTool/run_*.py /app/
COPY Dockers/HybridTool/bbn_input_loader.py /app/

# Make scripts executable
RUN chmod +x /app/run_*.py

# Default command (script selected via TASK_TYPE environment variable)
# TASK_TYPE: sensitivity_analysis, update_pfd, full_analysis
CMD ["sh", "-c", "python /app/run_${TASK_TYPE:-full_analysis}.py"]

