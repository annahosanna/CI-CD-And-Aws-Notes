# Use Amazon Linux 2023 as the base image
FROM amazonlinux:2023
# FROM busybox:latest

# Install root CA
RUN yum install -y ca-certificates && \
    update-ca-trust force-enable
# RUN mkdir -p /etc/ssl/certs && \
#    wget -O /etc/ssl/certs/ca-certificates.crt https://curl.se/ca/cacert.pem

# Install necessary packages
RUN yum update -y && \
<<<<<<< HEAD
    yum install -y busybox curl-devel gcc gcc-c++ make openssl-devel zlib-devel autoconf automake libtool krb5-libs libicu openssl-libs zlib

RUN yum update -y && \
    yum install -y ca-certificates socklog java-17-openjdk-headless wget openssl-devel pam-devel zlib-devel dotnet-sdk-6.0 \
    && yum clean all

# Build and install OpenSSH from source
WORKDIR /tmp
RUN curl -LO https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-8.4p1.tar.gz && \
    tar xzf openssh-8.4p1.tar.gz && \
    cd openssh-8.4p1 && \
=======
    yum install -y busybox ansible powershell proot python3 dotnet curl-devel gcc gcc-c++ make openssl-devel zlib-devel autoconf automake libtool socklog awscli wget && \
    yum install -y java-17-openjdk-headless && \
    yum clean all

# Build and install OpenSSH from source without tcl/tk and GetText
RUN curl -LO https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-9.7p1.tar.gz && \
    tar -xzf openssh-9.7p1.tar.gz && \
    cd openssh-9.7p1 && \
>>>>>>> 0f251fa (Make changes to Dockerfile)
    ./configure --without-tcl --without-tk && \
    make && make install
# Also need to make clean, and clean upbuid direcctory

# Also need to make clean, and clean upbuid direcctory
RUN ssh-keygen -A
RUN \
    echo "RSAAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config

# Enable RSA in sshd_config
RUN sed -i 's/#HostKey \/etc\/ssh\/ssh_host_rsa_key/HostKey \/etc\/ssh\/ssh_host_rsa_key/' /etc/ssh/sshd_config

# Create home directory for GitLab CE user
# Shouldn't useradd create dir and set perm?
RUN useradd -m gitlab-ce && \
    mkdir -p /home/gitlab-ce && \
    chown gitlab-ce:gitlab-ce /home/gitlab-ce

# Build and install Git from source without Tcl/Tk and GetText
RUN \
    wget https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.33.0.tar.gz && \
    tar -xzvf git-2.33.0.tar.gz && \
    cd git-2.33.0 && \
    make configure && \
    ./configure --without-tcltk --without-gettext && \
    make all && \
    make install


# RUN wget https://busybox.net/downloads/binaries/1.35.0-x86_64/busybox && \
#     mv busybox /bin/busybox && chmod +x /bin/busybox && \
#     ln -s /bin/busybox /bin/sh && \
#     ln -s /bin/busybox /bin/ash
# RUN yum install -y busybox

# This isn't quite right as kaniko is the name of the program
RUN \
    wget https://github.com/GoogleContainerTools/kaniko/releases/download/v1.6.0/kaniko-executor -O /kaniko && \
    chmod +x /kaniko

# Create a directory for Kaniko to run within proot
RUN mkdir -p /kaniko/.docker
# Set environment variables
# Set up Kaniko configuration

RUN echo '{"auths":{"your-registry":{"username":"your-username","password":"your-password"}}}' > /kaniko/.docker/config.json

# Install various interpreters like Python, Java, Ruby whatever
# For Java you will also need to add the library search path:
RUN echo $(dirname $(dirname $(which java | tr -d '[:space:]!')))"/lib" > /etc/ld.so.conf.d/file.conf && \
    ldconfig

# Install GitLab client
RUN curl -LO https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh && \
    bash script.rpm.sh && \
    yum install -y gitlab-ce

<<<<<<< HEAD
# Create gitlab-ce user and directory
RUN useradd -ms /bin/bash gitlab-ce

# Install Tini
RUN curl -Lo /tini https://github.com/krallin/tini/releases/download/v0.19.0/tini-static && chmod +x /tini

# Install proot and tini
RUN yum install -y proot

RUN echo $(dirname $(dirname $(which java | tr -d '[:space:]!')))"/lib"
RUN ldconfig
=======
# Install Tini
RUN curl -Lo /usr/bin/tini https://github.com/krallin/tini/releases/download/v0.19.0/tini && \
    chmod +x /usr/bin/tini
>>>>>>> 0f251fa (Make changes to Dockerfile)

# Install proot
RUN \
    wget https://github.com/proot-me/proot-static-build/releases/download/v5.1.0/proot-x86_64 -O /bin/proot && \
    chmod +x /bin/proot

# Probably need a syslog like program listening on /dev/log like logrotate

ENV HOME /root
ENV PATH /bin:/sbin:/usr/bin:/usr/sbin

# Entry point script
ADD entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
# Use Tini as the entry point to manage the process
ENTRYPOINT ["/sbin/tini", "--", "/entrypoint.sh"]
