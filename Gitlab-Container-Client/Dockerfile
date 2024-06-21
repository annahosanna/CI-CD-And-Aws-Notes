FROM amazonlinux:2023

# Install Busybox and development tools
RUN yum update -y && \
    yum install -y busybox curl-devel gcc gcc-c++ make openssl-devel zlib-devel autoconf automake libtool

# Install CA certificates
RUN yum install -y ca-certificates

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

# Install proot and tini
RUN yum install -y proot tini

# Create entrypoint script
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/sbin/tini", "--", "/usr/local/bin/entrypoint.sh"]
