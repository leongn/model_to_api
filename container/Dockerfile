# Build an image that can do training and inference in SageMaker
# This is a Python 3 image that uses the nginx, gunicorn, flask stack
# for serving inferences in a stable way.

FROM ubuntu:16.04

MAINTAINER Leongn

# 1. Define the packages required in our environment. 
RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         python3 \
         nginx \
         ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 2. Here we define all python packages we want to include in our environment.
# Pip leaves the install caches populated which uses a significant amount of space. 
# These optimizations save a fair amount of space in the image, which reduces start up time.
RUN wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py && \
    pip install numpy scipy==1.1.0 scikit-learn==0.19.1 pandas nltk xlrd flask gevent gunicorn && \
        rm -rf /root/.cache

# 3. Set some environment variables. PYTHONUNBUFFERED keeps Python from buffering our standard
# output stream, which means that logs can be delivered to the user quickly. PYTHONDONTWRITEBYTECODE
# keeps Python from writing the .pyc files which are unnecessary in this case. We also update
# PATH so that the train and serve programs are found when the container is invoked.

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"

# 4. Define the folder (sentiment_analysis) where our inference code is located
COPY sentiment_analysis /opt/program
WORKDIR /opt/program

