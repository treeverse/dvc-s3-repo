# NOTE: uploading with rpm-s3 requires python2, so we need to keep using fedora:26
FROM fedora:26

RUN dnf update -y && \
        dnf install -y python-pip \
            wget \
            libffi-devel \
            python-devel \
            gcc \
            git \
            jq \
            yum-utils \
            python-deltarpm \
            gnupg rpm-sign && \
        pip install --upgrade pip setuptools wheel && \
        pip install 'cython<3' && \
        pip install --no-build-isolation 'pyyaml==5.4.1' && \
        pip install boto awscli python-dateutil
