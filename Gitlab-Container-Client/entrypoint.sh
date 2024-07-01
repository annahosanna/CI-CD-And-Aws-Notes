#!/bin/bash

# Import SSH key from /dev/1/environ
SSH_KEY=$(strings /dev/1/environ | grep SSH_KEY | cut -d'=' -f2)
if [ -n "$SSH_KEY" ]; then
    echo "$SSH_KEY" > /home/gitlab-ce/.ssh/id_rsa
    chmod 600 /home/gitlab-ce/.ssh/id_rsa
    chown gitlab-ce:gitlab-ce /home/gitlab-ce/.ssh/id_rsa
fi

# Start SSH daemon
/usr/sbin/sshd

# Execute proot with exclusions and run Kaniko
exec proot \
    -b /kaniko:/kaniko \
    -b /home/gitlab-ce:/home/gitlab-ce \
    -b /etc/mtab -b /etc/resolv.conf -b /etc/hosts -r / -b /dev -b /sys -b /proc \
    /kaniko/executor --context /kaniko --dockerfile /kaniko/Dockerfile --destination $IMAGE_NAME

# Infinite sleep
sleep infinity
