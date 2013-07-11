#!/bin/bash

fedora_gems_raw='/home/axil/fedora/gitlab-deps/rubygems_fedora_raw'
fedora_gems='/home/axil/fedora/gitlab-deps/rubygems_fedora'
bugzilla_gems_raw='/home/axil/fedora/gitlab-deps/rubygems_bugzilla_raw'
bugzilla_gems='/home/axil/fedora/gitlab-deps/rubygems_bugzilla'

# Remove files if already exist
ls -l | grep rubygem > /dev/null 2>&1
if [ '$?' = '0' ];
then 
  rm rubygems_*
fi

echo 'Searching Fedora repositories...'
#reposync --repoid=fedora,updates,updates-testing
yum search all rubygem | awk '{print $1}' | sort -k1 > $fedora_gems_raw

# Striping uneeded symbols and the rubygem- prefix
sed -e 's/rubygem-//g' -e 's/.noarch//g' -e 's/.x86_64//g' -e '/-doc/d' -e '/i686/d' -e '/-devel/d' -e '/==/d' -e '/:/d' < $fedora_gems_raw > $fedora_gems

echo 'Done!'

# Install python-bugzilla first
echo 'Searching Bugzilla for Review Requests...'
# Save raw query
bugzilla query --product=fedora --bug_status=new,assigned --component='Package Review' --short_desc='rubygem-' | sort -k2 -r > $bugzilla_gems_raw

# Keep names only
bugzilla query --product=fedora --bug_status=new,assigned --component='Package Review' --short_desc='rubygem-' \
  | awk 'BEGIN { FS = " - " } ; { print $3 }' | awk 'BEGIN { FS = ":" } ; { print $2 }' | sed -e 's/ rubygem-//' \
  | sort -k1 > $bugzilla_gems

echo 'Done!'
