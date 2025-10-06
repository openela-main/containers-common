#!/bin/bash
set -e
rm -f /tmp/pyxis*.json
TOTAL=`curl -s --negotiate -u: -H 'Content-Type: application/json' -H 'Accept: application/json' -X GET "https://pyxis.engineering.redhat.com/v1/repositories?page_size=1" | jq .total`
if [ "$TOTAL" == "null" ]; then
  echo "Error comunicating with Pyxis API."
  exit 1
fi
PAGES=$(($TOTAL/250))
for P in `seq 0 $PAGES`; do
  curl -s --negotiate -u: -H 'Content-Type: application/json' -H 'Accept: application/json' -X GET "https://pyxis.engineering.redhat.com/v1/repositories?page_size=500&page=$P" > /tmp/pyxis$P.json
done
cat /tmp/pyxis*.json > /tmp/pyx.json
rm -f /tmp/pyx_debug
rm -f /tmp/rhel-shortnames.conf
jq '.data[]|.published,.requires_terms,.repository,.registry,.release_categories[0]' < /tmp/pyx.json >/tmp/pyx
readarray -t lines < /tmp/pyx
IDX=0
while [ $IDX -lt ${#lines[@]} ]; do
  PUBLISHED=${lines[$IDX]}
  REQ_TERMS=${lines[$IDX+1]}
  REPOSITORY=`echo ${lines[$IDX+2]} | tr -d '"'`
  REGISTRY=`echo ${lines[$IDX+3]} | tr -d '"'`
  RELEASE=`echo ${lines[$IDX+4]} | tr -d '"'`
  if [ "$PUBLISHED" == "true" ] &&
     [ "$RELEASE" == "Generally Available" ] &&
     [ ! -z "$REPOSITORY" ] &&
     [ "$REPOSITORY" != \"\" ] &&
     [[ $REPOSITORY != *[@:]* ]] &&
     [[ $REPOSITORY != *[* ]] &&
     [[ $REGISTRY == *.* ]] &&
     [ "$REGISTRY" != "non_registry" ]; then
    if [[ $REGISTRY == *quay.io* ]] ||
       [[ $REGISTRY == *redhat.com* ]]; then
      if [ "$REQ_TERMS" == "true" ]; then
        REGISTRY=registry.redhat.io
      fi
    fi
    echo "\"$REPOSITORY\" = \"$REGISTRY/$REPOSITORY\""
    echo $PUBLISHED,$REQ_TERMS,$REPOSITORY,$REGISTRY,$RELEASE >> /tmp/pyx_debug
    echo "\"$REPOSITORY\" = \"$REGISTRY/$REPOSITORY\"" >> /tmp/rhel-shortnames.conf
  fi
  IDX=$(($IDX+5))
done

cp /tmp/rhel-shortnames.conf /tmp/r.conf
for D in `cut -d\  -f1 /tmp/r.conf | sort | uniq -d`; do
  echo $D
  M=`grep ^$D /tmp/r.conf | grep 'redhat.com' | tail -n1`
  [ -z "$M" ] && M=`grep ^$D /tmp/r.conf | tail -n1`
  echo $M
  if [ ! -z "$M" ]; then
    echo "replacing $D with $M"
    grep -v "^$D.*" /tmp/r.conf > /tmp/r2.conf
    echo "$M" >> /tmp/r2.conf
    mv /tmp/r2.conf /tmp/r.conf
  fi
done

sed -i '/.*rhel.*-els\/.*$/d' /tmp/r.conf
echo "[aliases]" > 001-rhel-shortnames-pyxis.conf
sort /tmp/r.conf >> 001-rhel-shortnames-pyxis.conf
