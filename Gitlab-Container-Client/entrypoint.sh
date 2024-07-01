#!/bin/bash

# Import SSH key from /dev/1/environ
SSH_KEY=$(strings /dev/1/environ | grep SSH_KEY | cut -d'=' -f2)
if [ -n "$SSH_KEY" ]; then
    echo "$SSH_KEY" > /home/gitlab-ce/.ssh/id_rsa
    chmod 600 /home/gitlab-ce/.ssh/id_rsa
    chown gitlab-ce:gitlab-ce /home/gitlab-ce/.ssh/id_rsa
fi

# Execute proot with exclusions and run Kaniko
exec proot \
    -b /kaniko:/kaniko \
    -b /home/gitlab-ce:/home/gitlab-ce \
    -b /etc/mtab -b /etc/resolv.conf -b /etc/hosts \
    /kaniko/executor --context /kaniko --dockerfile /kaniko/Dockerfile --destination $IMAGE_NAME

# Keep the container running
exec sleep infinity
