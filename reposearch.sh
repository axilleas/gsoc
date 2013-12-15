#!/bin/bash

fedora_gems_raw=$PWD/rubygems_fedora_raw
fedora_gems=$PWD/rubygems_fedora
bugzilla_gems_raw=$PWD/rubygems_bugzilla_raw
bugzilla_gems=$PWD/rubygems_bugzilla

# Remove files if they already exist
ls -l | grep rubygem > /dev/null 2>&1
if [ '$?' = '0' ];
then
  rm rubygems_*
fi

echo 'Searching Fedora repositories...'
#reposync --repoid=fedora,updates,updates-testing
#yum search all rubygem | awk '{print $1}' | sort -k1 > $fedora_gems_raw
repoquery --disablerepo=fedora-gitlab,fedora-gitlab-noarch rubygem-* > $fedora_gems_raw

# Striping uneeded symbols and the rubygem- prefix
cat $fedora_gems_raw | sed -e 's/rubygem-//g;s/.fc19.noarch//g;s/.fc19.x86_64//g;/-doc/d;/-devel/d;/-debuginfo/d' | awk 'BEGIN { FS=":" }; {print $1}' | sed 's/.\{2\}$//g' > $fedora_gems

echo 'Done!'

# Install python-bugzilla first
echo 'Searching Bugzilla for Review Requests...'
# Save raw query
bugzilla query --product=fedora --bug_status=NEW,ASSIGNED --component='Package Review' --short_desc='rubygem-' | sort -k2 -r > $bugzilla_gems_raw

# Keep names only
bugzilla query --product=fedora --bug_status=NEW,ASSIGNED --component='Package Review' --short_desc='rubygem-' \
  | awk 'BEGIN { FS = " - " } ; { print $3 }' | awk 'BEGIN { FS = ":" } ; { print $2 }' | sed -e 's/ rubygem-//' \
  | sort -k1 > $bugzilla_gems

echo 'Done!'
