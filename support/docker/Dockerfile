# SPDX-License-Identifier: GPL-2.0-or-later
# copied from Buildroot 2021.08-1081-g76c7fed85f
# and then updated:
# - to not point to Buildroot mailing list or docker hub
# - to allow multiple layers on docker to improve regeneration of image
# - to use sed to select snapshot mirror instead of copying a file
# - to add pytest

# This Dockerfile generates the docker image that gets used by Gitlab CI
# To build it (YYYYMMDD.HHMM is the current date and time in UTC):
#   sudo docker build -t ricardomartincoski/checkpackage:YYYYMMDD.HHMM support/docker
#   sudo docker push ricardomartincoski/checkpackage:YYYYMMDD.HHMM

# We use a specific tag for the base image *and* the corresponding date
# for the repository.
FROM debian:bullseye-20210902

LABEL maintainer="Ricardo Martincoski <ricardo.martincoski@gmail.com>" \
      description="Container with everything needed to unit test check-package used in buildroot"

# Setup environment
ENV DEBIAN_FRONTEND noninteractive

# This repository can be a bit slow at times. Don't panic...
RUN sed -e 's,^deb.*,,g' -e 's,^# deb,deb [check-valid-until=no],g' -i /etc/apt/sources.list

# The container has no package lists, so need to update first
RUN dpkg --add-architecture i386 && \
    apt-get update -y
RUN apt-get install -y --no-install-recommends \
        bc \
        build-essential \
        bzr \
        ca-certificates \
        cmake \
        cpio \
        cvs \
        file \
        g++-multilib \
        git \
        libc6:i386 \
        libncurses5-dev \
        locales \
        mercurial \
        python3 \
        python3-flake8 \
        python3-nose2 \
        python3-pexpect \
        qemu-system-arm \
        qemu-system-x86 \
        rsync \
        subversion \
        unzip \
        wget \
        && echo done

RUN apt-get install -y --no-install-recommends \
        python3-pytest \
        && echo done

RUN apt-get -y autoremove && \
    apt-get -y clean

# To be able to generate a toolchain with locales, enable one UTF-8 locale
RUN sed -i 's/# \(en_US.UTF-8\)/\1/' /etc/locale.gen && \
    /usr/sbin/locale-gen

RUN useradd -ms /bin/bash br-user && \
    chown -R br-user:br-user /home/br-user

USER br-user
WORKDIR /home/br-user
ENV HOME /home/br-user
ENV LC_ALL en_US.UTF-8
