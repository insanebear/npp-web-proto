# ===================================================================
# Dockerfile for Fargate Batch Job
# ===================================================================

FROM rocker/r-ver:4.4.1

# 1. Install system dependencies and update certificate store
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    jags \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    ca-certificates \
    libfontconfig1-dev \
    libfreetype6-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
 && update-ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# 2. Install CRAN packages (including remotes and jsonlite)
RUN R -e "install.packages(c('rjags', 'remotes', 'jsonlite'), repos='https://cloud.r-project.org', Ncpus = 4)"

# 3. Install paws from CRAN
RUN R -e "install.packages('paws', repos='https://cloud.r-project.org', Ncpus = 4)"

# 4. Verify paws is installed
RUN R -e "if (!requireNamespace('paws.common', quietly = TRUE)) quit(status = 1)"

# 5. Set working directory
WORKDIR /app

# 6. Copy project files
COPY . /app/

# 7. Default command
CMD ["Rscript", "/app/run_simulation.R"]