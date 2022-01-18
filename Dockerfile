FROM gitpod/workspace-full


RUN sudo apt-get update
# RUN sudo apt-get -y upgrade
RUN export DEBIAN_FRONTEND=noninteractive \
    && sudo apt -y install --no-install-recommends openscad xvfb
RUN pip3 --disable-pip-version-check --no-cache-dir install viewscad solidpython
