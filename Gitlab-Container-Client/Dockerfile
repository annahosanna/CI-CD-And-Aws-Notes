FROM amazonlinux:2023

# Install Busybox and development tools
RUN yum update -y && \
    yum install -y busybox curl-devel gcc gcc-c++ make openssl-devel zlib-devel autoconf automake libtool krb5-libs libicu openssl-libs zlib

RUN yum update -y && \
    yum install -y ca-certificates socklog java-17-openjdk-headless wget openssl-devel pam-devel zlib-devel dotnet-sdk-6.0 \
    && yum clean all

# Build and install OpenSSH from source
WORKDIR /tmp
RUN curl -LO https://cdn.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-8.4p1.tar.gz && \
    tar xzf openssh-8.4p1.tar.gz && \
    cd openssh-8.4p1 && \
    ./configure --without-tcl --without-tk && \
    make && \
    make install

# Build and install Git from source
RUN curl -LO https://mirrors.edge.kernel.org/pub/software/scm/git/git-2.32.0.tar.gz && \
    tar xzf git-2.32.0.tar.gz && \
    cd git-2.32.0 && \
    make configure && \
    ./configure --without-tcltk --without-gettext && \
    make && \
    make install

# Enable RSA in sshd_config
RUN echo "RSAAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PubkeyAuthentication yes" >> /etc/ssh/sshd_config

# Install GitLab client
RUN curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.rpm.sh | bash && \
    yum install -y gitlab-ce

# Create gitlab-ce user and directory
RUN useradd -ms /bin/bash gitlab-ce

# Install Tini
RUN curl -Lo /tini https://github.com/krallin/tini/releases/download/v0.19.0/tini-static && chmod +x /tini

# Install proot and tini
RUN yum install -y proot

RUN echo $(dirname $(dirname $(which java | tr -d '[:space:]!')))"/lib"
RUN ldconfig

# Create entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/entrypoint.sh"]
