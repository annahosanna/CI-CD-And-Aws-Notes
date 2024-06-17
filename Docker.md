## This is mostly dedicated to the creation and execution of Dockerfiles/Images in a rootless environment

```
* A rootless Docker image builder with a fair number of restrictions for Kubernetes. The OS on this will need to be reconstructed.
- https://github.com/GoogleContainerTools/kaniko
* Upload tools for your favorite image repositlory
- https://github.com/google/go-containerregistry
* Chroot like tool under which the new Docker image will be built.
- https://gitlab.com/proot/proot/-/pipelines
* Provide replacements for the Linux tools whos installers do not work without Systemd 
- https://www.busybox.net/

Other notes:
Some application like perl and maybe OpenSSH will need to be recompiled so that they do not rely on Systemd 
```

### Random Dockerfile notes ###

#### My program thinks it needs Systemd :(
* Some programs think they need Systemd, and then you will have to install it :(
 1. yum install procps-ng mlocate dbus dbus-libs util-linux
 2. Many tools like rsync and OpenSSH (distro), have for no good reason, been forced to use Systemd as a dependancy by the distro vendor.
* Systemd was not made to use containers and relies on the abilty to see cgroups, in the same way Docker does. This allows Systemd Units to correct manage process group resources for which a parent has exited.
 1. While systemd is useless - systemctl, and journalctl are still necessary (and maybe udev too), so they should be replaced with:
 2. docker-systemctl-replacement, and docker-journalctl-replacement files in /usr/bin and symlinked as necessary
 3. Further process management can also be done with s6, s6-overlay, Runit, and GNU Shepherd
 4. [Integrating Runit with Systemd Example](https://busybox.net/kill_it_with_fire.txt)
#### Replacing Systemd
 1. Systemd monitors processes and cleans up zombie processes. 
* A new PID 1
 1. Having a PID 1 is probably a good idea because of the way environment variable injection happens in containers. 
 2. Zombie cleanup can, but does not need to a be, a child process of PID 1.
 3. Tini is an easy choice.
* A new process supervisor 
 1. This is not a graphical system: 
 2. `systemctl mask graphical.targget runlevel5.target`
 3. `systemctl set-default multi-user.target`
* Journald is still needed: systemctl start systemd-journald.service
* Make sure the syslog socket is pointing to the correct place: `rm -f /dev/log && ln -s /run/systemd/journal/dev-log /dev/log`
* `mkdir -p /var/log/journal && chown root:systemd-journal /var/log/journal && chmod 755 /var/log/journal && chmod g+s /var/log/journal`
* Adjust /etc/systemd/journald.conf to ensure it does not write to kmsg. The Syslog RFC also states that syslog lines should not exeed 1K. 
#### DBus setup
 1. Some programs rely on DBus for signaling; however, this will have to occur without Systemd. The steps are as follows
 2. One time setup of dbus uuid: `dbus-uuidgen > /var/lib/dbus/machine-id` 
 3. Start DBus: `dbus-daemon --config-file=/usr/share/dbus-1/system.conf --print-address`
 4. `ENV DBUS_SESSION_BUS_ADDRESS="unix:path=/run/dbus/system_bus_socket"`
 5. If this was done as a part of building the container then `rm -f /run/dbus/messagebus.pid && rm -rf /run/dbus`
 6. Create a script in /etc/profile.d with something like: `export $(strings /proc/1/environ | grep DBUS_SESSION_BUS_ADDRESS)`
#### Maybe you don't need Systemd
 1. Can you build the generic version yourself, so that Systemd is not tied in?
 2. OpenSSH and git are good examples (You don't need tcl/tk, or GetText normally) - and just follow the instructions for installing dependancies like curl-devel
 3. As mentioned above, procps requires Systemd - why not just use the ps from busybox which does not.
 4. Busybox provides a huge number of programs, including Runit.
 5. If your creating a container, then you do not even need to build it yourself. You can use COPY --from ... to get the correct files from the Busybox docker distribution.
 #### Docker in Docker (DID) and Rootless containers for CI/CD and Fargate
 1. Use proot to create a false root (it uses the only available Fargate capability `SYS_PTRACE`) - Then remap the same files and directories which Docker does: `/etc/mtab`, `/etc/resolv.conf` and `/etc/hosts` (and a few directories like `/dev` `/sys` `/proc`)
 2. Add `SYS_PTRACE` capability (the only capability which you can add in Fargate) to the Task Definition
 3. Use Kaniko to perform the build (to a tar)
 4. As a part of the Dockerfile add any non standard library paths (such as Java may create) to ld.so.conf.d to the resulting image
 5. Using From the Go Container Registry project use the crane tool to upload to Docker repositories.
* Great source of info about al2 dockerfiles: `https://github.com/aws/aws-codebuild-docker-images/blob/master/al2/x86_64/standard/3.0/Dockerfile`
#### SSM/CloudWatch
* When fargate injects environment variables it does so to PID 1, so you may need to copy the variable name and value from PID 1 into the PID of Cloudwatch and SSM, in order to assume a role. `export ($strings /proc/1/environ | grep AWS_CONTAINER_CREDENTIALS_RELATIVE_URI )` and similar.
* `ENV RUN_IN_CONTAINER=True`
* If there are health chech ipc errors: `rm -rf /var/lib/amazon/ssm/ipc`
* Worst case, you might need to treat the container like foriegn hybid infrastructure, and configure ssm accordingly.
#### Java library note
* In a Dockerfile, any non standard library path might need something like:
```
echo "/path/to/libs" > /etc/ld.so.conf.d/file.conf
ldconfig
```
* For Java it might be similar to:
```
echo $(dirname $(dirname $(which java | tr -d '[:space:]!')))"/lib"
```
#### AWS Corretto and OpenJDK do not have the same systemd requirement.
* AWS Corretto Headless via yum depends on systemd - and is not meant for containers. If you want to roll your own AL2 Java then refer to the Dockerfile provided by AWS for the correct yum repo. (Unlike OpenDK)
#### Save layers
* Create the image and then only copy the needed parts - for instance if a whole bunch of tools were installed to build a binary, but only the resulting binary is needed, or if the certificate store was manipulated using several commands, but only the final result is needed.
```
FROM mybase as firstthing
...
...
FROM myotherbase as secondthing
...
...
FROM scratch
COPY --from=firstthing / /first/
COPY --from=secondthing / /second/
```
* Caveat: Check that suid bit is still set correctly after copy.


#### Container stuff
* Process supervisors which do not use cgroups and are meant to run as pid 1: S6, Runit
  1. Seems like AWS ECS Fargate injects some metadata environment variables into `/proc/1/environ` so it might be important to retain pid 1 environ. 
* (S6 Overlay)[https://github.com/just-containers/s6-overlay]
* What about tini -> bash -> Start programs -> 'wait'
* Minimalistic init's to prevent zombies and resource leaks: tini/dumb-init/minit (Originally at `https://github.com/chazomaticus/minit`)/(or any other simple init)
* Example project of a Docker container with a Process Supervisor, which start multiple processes such as (S6 Overlay)[https://github.com/just-containers/s6-overlay]
* socklog (deal with missing /dev/log)
* https://github.com/aws/aws-codebuild-docker-images/tree/master/al2/x86_64/standard/3.0 (this also does dind)
* Systemd does not work in containers without extra capabilities for a number of reasons such as cgroups, and dbus - but it seems to be the standard most applications use.
* Need to add a link here to the explanation of why dind is so hard, and which solutions are truely rootless.
* S6 examples with comments. Execlineb and the way it uses a stack is neat and logical, but some examples are needed for when to use one thing rather than another.
* S6 sometimes uses some fd stuff that is confusing and needs better comments.
* S6 also needs to document its limits - such as when it needs a helper program, like socklog.
* Although I may not like it some software requires systemd
  1. systemd (systemctl) (docker-systemctl-replacement)
  2. rsyslog
  3. logrotate
  4. binutils
  5. coreutils
  6. python3
  7. iptables
  8. util-linux
  9. iproute
  10. net-tools
  11. maybe ethtool
  12. dbus
  13. maybe java 

#### Add ECS/ECR/Fargate notes
  * Add notes
  * Find out how to do sidecars
    1. https://linkedin.com/pulse/architecting-sidecar-securely-aws-fargate-anuj-gupta?trk=public_profile_article_view
    2. https://blog.aquasec.com/securing-aws-fargate-with-sidecards
    3. https://aws.amazon.com/blogs/compute/nginx-reverse-sidecar-container-on-amazon-ecs/
    4. https://blog.aquasec.com/revisiting-aws-fargate-with-aqua-3.0
  * Add another entry to the array of images in the Task Definition. These can then share resources, but run as two seperate containers.
    1. Good for being able to upgrade one container image without affecting the other.
  * An ECS Fargate Metadata to EC2 Metadata mock. Some software assumes EC2, doesn't understand where to get ECS metadata. A mock that combines iptables, the ECS Metadata and some API calls to produce something that looks like EC2 Metadata would be useful for software compatibility.

## ------------------------------------------
