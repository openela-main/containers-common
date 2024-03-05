#!/bin/bash
# This script assures we always deliver the current documentation/configs
# for the c/storage, c/image and c/common vendored in podman, skopeo, buildah
# For questions reach to Jindrich Novy <jnovy@redhat.com>
rm -f /tmp/ver_image /tmp/ver_common /tmp/ver_storage
CENTOS=""
pwd | grep /tmp/centos > /dev/null
if [ $? == 0 ]; then
  CENTOS=1
  PKG=centpkg
else
  PKG=rhpkg
fi
set -e
for P in podman skopeo buildah; do
  BRN=`pwd | sed 's,^.*/,,'`
  rm -rf $P
  $PKG clone $P
  cd $P
  $PKG switch-branch $BRN
  cache_deploy
  if [ $BRN != stream-container-tools-rhel8 ]; then
    $PKG prep
  else
    $PKG --release rhel-8 prep
  fi
  DIR=`ls -d -- */ | grep "$P"`
  grep github.com/containers/image $DIR/go.mod | cut -d\  -f2 | sed 's,-.*,,'>> /tmp/ver_image
  grep github.com/containers/common $DIR/go.mod | cut -d\  -f2 | sed 's,-.*,,' >> /tmp/ver_common
  grep github.com/containers/storage $DIR/go.mod | cut -d\  -f2 | sed 's,-.*,,' >> /tmp/ver_storage
  cd -
done
IMAGE_VER=`sort -n /tmp/ver_image | head -n1`
COMMON_VER=`sort -n /tmp/ver_common | head -n1`
STORAGE_VER=`sort -n /tmp/ver_storage | head -n1`
sed -i "s,^%global.*image_branch.*,%global image_branch $IMAGE_VER," containers-common.spec
sed -i "s,^%global.*common_branch.*,%global common_branch $COMMON_VER," containers-common.spec
sed -i "s,^%global.*storage_branch.*,%global storage_branch $STORAGE_VER," containers-common.spec
rm -f /tmp/ver_image /tmp/ver_common /tmp/ver_storage
rm -rf podman skopeo buildah
