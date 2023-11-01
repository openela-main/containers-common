#!/bin/bash
# This script delivers current documentation/configs and assures it has the intended
# settings for a particular branch/release.
# For questions reach to Jindrich Novy <jnovy@redhat.com>

ensure() {
  if grep ^$2[[:blank:]].*= $1 > /dev/null
  then
    sed -i "s;^$2[[:blank:]]=.*;$2 = $3;" $1
  else
    if grep ^\#.*$2[[:blank:]].*= $1 > /dev/null
    then
      sed -i "/^#.*$2[[:blank:]].*=/a \
$2 = $3" $1
    else
      echo "$2 = $3" >> $1
    fi
  fi
}

#./pyxis.sh
#./update-vendored.sh
spectool -f -g containers-common.spec
for FILE in *; do
  [ -s "$FILE" ]
  if [ $? == 1 ] && [ "$FILE" != "sources" ]; then
    echo "empty file: $FILE"
    exit 1
  fi
done
ensure storage.conf    driver                        \"overlay\"
ensure storage.conf    mountopt                      \"nodev,metacopy=on\"
if pwd | grep rhel-8 > /dev/null
then
awk -i inplace '/#default_capabilities/,/#\]/{gsub("#","",$0)}1' containers.conf
ensure registries.conf unqualified-search-registries [\"registry.access.redhat.com\",\ \"registry.redhat.io\",\ \"docker.io\"]
ensure registries.conf short-name-mode               \"permissive\"
ensure containers.conf runtime                       \"runc\"
ensure containers.conf events_logger                 \"file\"
ensure containers.conf log_driver                    \"k8s-file\"
ensure containers.conf network_backend               \"cni\"
if ! grep \"NET_RAW\" containers.conf > /dev/null
then
  sed -i '/^default_capabilities/a \
  "NET_RAW",' containers.conf
fi
if ! grep \"SYS_CHROOT\" containers.conf > /dev/null
then
  sed -i '/^default_capabilities/a \
  "SYS_CHROOT",' containers.conf
fi
else
ensure registries.conf unqualified-search-registries [\"registry.access.redhat.com\",\ \"registry.redhat.io\",\ \"docker.io\"]
ensure registries.conf short-name-mode               \"enforcing\"
ensure containers.conf runtime                       \"crun\"
fi
[ `grep \"keyctl\", seccomp.json | wc -l` == 0 ] && sed -i '/\"kill\",/i \
				"keyctl",' seccomp.json
[ `grep \"socket\", seccomp.json | wc -l` == 0 ] && sed -i '/\"socketcall\",/i \
				"socket",' seccomp.json
