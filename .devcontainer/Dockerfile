FROM mcr.microsoft.com/vscode/devcontainers/base:buster

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update -y \
    && apt -y install --no-install-recommends openscad python3 python3-pip

COPY ./requirements.txt /tmp/pip-tmp/requirements.txt

RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt