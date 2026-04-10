ARG PYTHON_VERSION=3.14
ARG RUBY_VERSION=3.4.7

FROM fedora:41 as pyenv
ARG PYTHON_VERSION

# https://github.com/pyenv/pyenv/wiki#suggested-build-environment
# https://github.com/pyenv/pyenv/issues/2416
RUN yum install -y \
        curl \
        wget \
        git \
        make \
        bzip2 \
        bzip2-devel \
        gcc \
        libffi-devel \
        openssl-devel \
        readline-devel \
        sqlite \
        sqlite-devel \
        tk-devel \
        xz-devel \
        zlib-devel \
        findutils

RUN curl https://pyenv.run | bash

ENV PYENV_ROOT="/root/.pyenv"
ENV PATH="$PYENV_ROOT/shims:$PYENV_ROOT/bin:$PATH"

# make sure we're using the correct python version
RUN PYTHON_CONFIGURE_OPTS="--enable-shared" pyenv install ${PYTHON_VERSION} && \
    pyenv global ${PYTHON_VERSION} && \
    python --version | grep ${PYTHON_VERSION}

FROM pyenv as rbenv
ARG RUBY_VERSION

RUN yum install -y rbenv

ENV RBENV_ROOT="/root/.rbenv"
ENV PATH="$RBENV_ROOT/shims:$RBENV_ROOT/bin:$PATH"
RUN rbenv install ${RUBY_VERSION} && \
    rbenv global ${RUBY_VERSION} && \
    ruby --version | grep ${RUBY_VERSION}

FROM rbenv

# TODO: check if all of these dependencies are required
RUN yum install -y wget jq yum-utils gnupg patch gdbm-devel ncurses-devel rpm-build && \
    gem install fpm

COPY --from=ghcr.io/astral-sh/uv:0.11.6 /uv /bin/
