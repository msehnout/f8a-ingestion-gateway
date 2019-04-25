FROM registry.centos.org/centos/centos:7
MAINTAINER Martin Sehnoutka <msehnout@redhat.com>

ENV LANG=en_US.UTF-8

RUN yum --setopt=tsflags=nodocs install -y epel-release && \
    yum --setopt=tsflags=nodocs install -y python36-pip git && \
    yum clean all

# Cache dependencies
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && \
    pip3 install --upgrade wheel && \
    pip3 install -r /tmp/requirements.txt

ENV APP_DIR=/ingestion_gateway
RUN mkdir -p ${APP_DIR}
WORKDIR ${APP_DIR}

COPY . .

CMD ["python3", "run.py"]