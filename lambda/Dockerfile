# Dockerfile for Lambda container image
# Uses AWS Lambda Python 3.11 base image

FROM public.ecr.aws/lambda/python:3.11

# System packages required for building scientific computing libraries
RUN yum install -y \
    gcc \
    gcc-c++ \
    make \
    blas-devel \
    lapack-devel \
    && yum clean all

WORKDIR ${LAMBDA_TASK_ROOT}

# Install NumPy and h5py first (use binary wheels to avoid build dependency issues)
RUN pip install --no-cache-dir numpy==1.26.4 h5py==3.11.0

# Install remaining packages
COPY lambda/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code (bbn_inference, etc.)
COPY server/bbn_inference ./bbn_inference

# Copy Lambda handler
COPY lambda/hybrid_tool_handler.py ./

CMD [ "hybrid_tool_handler.lambda_handler" ]

