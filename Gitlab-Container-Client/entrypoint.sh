#!/bin/sh

# Import SSH key
eval $(cat /dev/1/environ/SSH_KEY | awk -F "=" '{print "export "$1"="$2}')

# Run proot and execute kaniko
proot -b /etc/mtab -b /etc/resolv.conf -b /etc/hosts -b /etc -b /sys -b /proc -- /kaniko/executor "$@"

# Keep the container running
sleep infinity
