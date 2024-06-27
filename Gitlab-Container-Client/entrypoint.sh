<<<<<<< HEAD
#!/bin/bash

# Import SSH key from /dev/1/environ
SSH_KEY=$(strings /dev/1/environ | grep SSH_KEY | cut -d'=' -f2)
if [ -n "$SSH_KEY" ]; then
    echo "$SSH_KEY" > /home/gitlab-ce/.ssh/id_rsa
    chmod 600 /home/gitlab-ce/.ssh/id_rsa
    chown gitlab-ce:gitlab-ce /home/gitlab-ce/.ssh/id_rsa
fi

# Also need to configure /dev/log for socklog /var/log/messages etc.

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
=======
#!/bin/sh
###################################
# Import SSH key from injected environment variable
# eval $(cat /dev/1/environ/SSH_KEY | awk -F "=" '{print "export "$1"="$2}')
export $(strings /proc/1/environ | grep SSH_KEY)

# Import the GitLab client SSH key at runtime
# if [ -f /dev/1/environ/SSH_KEY ]; then
#     SSH_KEY=$(cat /dev/1/environ/SSH_KEY)
#     SSH_KEY_VALUE=${SSH_KEY#*=}
#     mkdir -p /root/.ssh
#     echo "$SSH_KEY_VALUE" > /root/.ssh/id_rsa
#     chmod 600 /root/.ssh/id_rsa
# else
#     echo "SSH key not found at /dev/1/environ/SSH_KEY"
#     exit 1
# fi

# SSH_KEY=$(echo $SSH_KEY | cut -d '=' -f 2)

# Need to check if env var is defined

# Setup the SSH key
mkdir -p /home/gitlab-ce/.ssh
echo "$SSH_KEY" > /home/gitlab-ce/.ssh/id_rsa
chmod 600 /gitlab-ce/.ssh/id_rsa
chown gitlab-ce:gitlab-ce /home/gitlab-ce/.ssh/id_rsa
# need to set up correct home directory ownership

# Run proot and execute kaniko
# proot will need to be run in the pipeline
# EXCLUDES="-b /etc/mtab:/etc/mtab -b /etc/resolv.conf:/etc/resolv.conf -b /etc/hosts:/etc/hosts -b /etc -b /sys -b /proc"
# cd /kaniko
#proot -b /etc/mtab -b /etc/resolv.conf -b /etc/hosts -b /etc -b /sys -b /proc -- /kaniko/executor "$@"

# Keep the container running
# This is the lowest overhead infinite loop
# sleep infinity
/usr/bin/sshd
# Execute gitlab-ce
>>>>>>> 0f251fa (Make changes to Dockerfile)
