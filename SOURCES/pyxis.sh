#!/bin/bash
#set -e
rm -f /tmp/pyxis*.json
TOTAL=`curl -s --negotiate -u: -H 'Content-Type: application/json' -H 'Accept: application/json' -X GET "https://pyxis.engineering.redhat.com/v1/repositories?page_size=1" | jq .total`
if [ "$TOTAL" == "null" ]; then
  echo "Error comunicating with Pyxis API."
  exit 1
fi
PAGES=$(($TOTAL/500))
for P in `seq 0 $PAGES`; do
  curl -s --negotiate -u: -H 'Content-Type: application/json' -H 'Accept: application/json' -X GET "https://pyxis.engineering.redhat.com/v1/repositories?page_size=500&page=$P" > /tmp/pyxis$P.json
done
cat /tmp/pyxis*.json > /tmp/pyx.json
rm -f /tmp/rhel-shortnames.conf
while read -r LINE; do
  if [[ "$LINE" == *\"_id\":* ]] || [[ "$LINE" == *\"total\":* ]]; then
    if [ -z $REGISTRY ] ||
       [ -z $PUBLISHED ] ||
       [ -z $REPOSITORY ] ||
       [  $REPOSITORY == \"\" ] ||
       [ "$AVAILABLE" != "Generally Available" ] ||
       [[ $REPOSITORY == *[@:]* ]] ||
       [[ $REPOSITORY == *[* ]] ||
       [[ "$REGISTRY" == *non_registry* ]] ||
       [[ $REGISTRY != *.* ]]
     then
      continue
    fi
    if [[ $REGISTRY == *quay.io* ]] ||
       [[ $REGISTRY == *redhat.com* ]]; then
      if [ "$REQUIRES_TERMS" == "1" ]; then
        REGISTRY=registry.redhat.io
      fi
      echo "\"$REPOSITORY\" = \"$REGISTRY/$REPOSITORY\""
      echo "\"$REPOSITORY\" = \"$REGISTRY/$REPOSITORY\"" >> /tmp/rhel-shortnames.conf
    fi
    REGISTRY=""
    PUBLISHED=""
    AVAILABLE=""
    REPOSITORY=""
    REQUIRES_TERMS=""
    continue
  fi
  if [[ "$LINE" == *\"published\":\ true,* ]]; then
    PUBLISHED=1
  fi
  if [[ "$LINE" == *\"requires_terms\":\ true,* ]]; then
    REQUIRES_TERMS=1
  fi
  if [[ "$LINE" == *\"repository\":\ * ]]; then
    REPOSITORY=`echo $LINE | sed 's,^.* ",,' | sed 's;",$;;'`
  fi
  if [[ "$LINE" == *\"registry\":\ * ]]; then
    REGISTRY=`echo $LINE | sed -e 's,^.*:\ ",,' -e 's,".*,,'`
  fi
  if [[ "$LINE" == *\"release_categories\":\ * ]]; then
    read -r LINE
    AVAILABLE=`echo $LINE | sed 's,",,g'`
  fi
done < /tmp/pyx.json

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
