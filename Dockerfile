FROM gitpod/workspace-full


RUN sudo apt-get update
# RUN sudo apt-get -y upgrade
RUN export DEBIAN_FRONTEND=noninteractive \
    && sudo apt -y install --no-install-recommends openscad
RUN  /usr/bin/pip --disable-pip-version-check --no-cache-dir install -U viewscad solidpython
