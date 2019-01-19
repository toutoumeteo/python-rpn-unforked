FROM ubuntu:16.04

LABEL upstream-source="https://github.com/mfvalin/rmnlib-install"
LABEL source="https://github.com/neishm/rmnlib-install-docker"

# Some dependencies needed for the server.
RUN apt-get update && apt-get install -y git make libssl-dev ksh gfortran libopenmpi-dev python liburi-perl wget libncurses5-dev libc6-dev-i386 openmpi-bin

# Create non-privileged account for compiling and installing ssm packages.
# Use the same userid and groupid as the host user to make it easier to
# mount volumes and do file I/O with the host system.
RUN groupadd -g 1000 ssm
RUN useradd -g ssm -u 1000 -m ssm

USER ssm

# Use rmnlib-install to build the core packages.
WORKDIR /home/ssm
RUN git clone https://github.com/jeixav/rmnlib-install.git 
WORKDIR /home/ssm/rmnlib-install
RUN git fetch && git checkout 92f256dae42c27ba37ea1f91dbbac97b079728d9

# Add gem-data as a package to install.
# Copy and adapt the lines in the Makefile from the 'afsisio' package.
RUN sed -i '/afsisio.* \\$/{p;s/afsisio_1.0u/gem-data_4.2.0/}' Makefile
RUN sed -i '/afsisio.*:/,/^$/H;${p;s/.*//;x;s/afsisio_1.0u/gem-data_4.2.0/g}' Makefile

RUN make auto-install VGRID_RELEASE=6.4

# Auto-load profile for interactive sessions.
RUN echo . $HOME/.profile_armnlib >> $HOME/.bashrc
RUN echo . r.load.dot dev/gfortran >> $HOME/.bashrc
WORKDIR /home/ssm

# Extra packages needed for python-rpn tests
USER root
RUN apt-get update
RUN apt-get install -y python-pytest python-numpy python-tz python-scipy

# Copy the python-rpn source into the docker image
COPY . /home/ssm/python-rpn
RUN chown ssm.ssm -R /home/ssm/python-rpn

USER ssm
