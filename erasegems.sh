#!/bin/bash

if [ "$(id -u)" != "0" ]; then
  echo "This script must be run as root"
  exit
fi

yum list installed 'rubygem-*' > /dev/null 2>&1
out=$?
if [ $out -eq 1 ]; then
  echo 'No rubygems found.'
  exit 1
else
  echo 'Removing locally installed gems...'

  yum list installed | awk '{print $1}'  | grep 'rubygem' |sed -e 's/.noarch//g;s/.x86_64//g;/-doc/d;/-devel/d;/-debuginfo/d;/fedora/d;/fc19/d' | xargs -L1 yum erase -y
fi
