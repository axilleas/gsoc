#!/bin/bash

# Give execute permissions if not set
chmod +x *sh *py

# Find total gems packaged in Fedora
sh reposearch.sh

# Remove unessecary file
#rm rubygems_fedora_raw

# libv8 is a tricky one
sed -i 's/-x86_64-linux//' gitlab53-gems

# Find missing gems
python2 gemfile.py
