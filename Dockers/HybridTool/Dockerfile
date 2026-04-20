# Dockerfile for HybridTool PyMC Fargate Task
# conda environment for PyMC/JAX/numpyro dependency compatibility

FROM condaforge/miniforge3:latest

WORKDIR /app

# Copy conda environment file and create environment
# Uses mamba (faster conda solver) bundled with miniforge3
COPY Dockers/HybridTool/environment-docker.yml /tmp/environment.yml
RUN mamba env create -f /tmp/environment.yml && \
    mamba clean -afy && \
    find /opt/conda/envs/hybridtool -name "*.pyc" -delete

# Use conda environment by default
ENV PATH=/opt/conda/envs/hybridtool/bin:$PATH

# Copy project files
COPY server_min/ /app/server/
COPY Dockers/HybridTool/run_*.py /app/
COPY Dockers/HybridTool/task_common.py /app/
COPY Dockers/HybridTool/bbn_input_loader.py /app/

# Make scripts executable
RUN chmod +x /app/run_*.py

# Default command (script selected via TASK_TYPE environment variable)
# TASK_TYPE: bbn_inference, sensitivity_analysis, update_pfd, full_analysis
CMD ["sh", "-c", "python /app/run_${TASK_TYPE:-full_analysis}.py"]

