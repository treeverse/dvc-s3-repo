ARG PYTHON_VERSION=3.14
ARG RUBY_VERSION=3.4.7

FROM ubuntu:20.04 AS pyenv
ARG PYTHON_VERSION

# Setup python (pyenv) build dependencies (https://github.com/pyenv/pyenv/wiki#suggested-build-environment)
RUN apt-get update && \
   DEBIAN_FRONTEND=noninteractive  apt-get install -y \
        build-essential \
        git \
        curl \
        libbz2-dev \
        libffi-dev \
        liblzma-dev \
        libncursesw5-dev \
        libreadline-dev \
        libsqlite3-dev \
        libssl-dev \
        libxml2-dev \
        libxmlsec1-dev \
        llvm \
        tk-dev \
        wget \
        xz-utils \
        zlib1g-dev && \
    # ruby dependencies
    apt-get install -y libyaml-dev && \

    rm -rf /var/lib/apt/lists/*

RUN curl https://pyenv.run | bash

ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# make sure we're using the correct python version
RUN PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    python --version | grep ${PYTHON_VERSION}

FROM pyenv AS rbenv
ARG RUBY_VERSION

RUN curl -fsSL https://github.com/rbenv/rbenv-installer/raw/HEAD/bin/rbenv-installer | bash
ENV RBENV_ROOT="/root/.rbenv"
ENV PATH="$RBENV_ROOT/shims:$RBENV_ROOT/bin:$PATH"
RUN rbenv install ${RUBY_VERSION} && \
    rbenv global ${RUBY_VERSION} && \
    ruby --version | grep ${RUBY_VERSION}

FROM rbenv

# https://github.com/deb-s3/deb-s3
RUN gem install fpm deb-s3

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /bin/

RUN uv pip install --system boto awscli
