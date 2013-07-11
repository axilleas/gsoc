#!/usr/bin/env python2

import json
import urllib2
import re
import os
import sys
import time
import pkgwat.api

# Declare files

gitlab_gems_file = os.path.realpath('gitlab53-gems')
rubygems_fedora = os.path.realpath('rubygems_fedora')
rubygems_gitlab = os.path.realpath('rubygems_gitlab')
rubygems_missing = os.path.realpath('rubygems_missing')
rubygems_common = os.path.realpath('rubygems_common')
gitlab_json = os.path.realpath('gitlab.json')
fedora_json = os.path.realpath('fedora.json')
upstream_json = os.path.realpath('upstream.json')
gems_versions_json = os.path.realpath('all_versions.json')
gems_bugzilla = os.path.realpath('rubygems_bugzilla_raw')
gems_bugzilla_common = os.path.realpath('rubygems_bugzilla_common')
versions_table = os.path.realpath('wiki_table_versions')


def gitlab_gems_all():
  '''file -> list

  Returns a sorted list of Gitlab's dependencies included in Gemfile.lock.

  '''
  gemfile_gitlab = urllib2.urlopen('https://raw.github.com/gitlabhq/gitlabhq/master/Gemfile.lock')
  gemfile_gitlab_shell = urllib2.urlopen('https://raw.github.com/gitlabhq/gitlab-shell/master/Gemfile.lock')

  gem_gitlab = gemfile_gitlab.readlines()
  gem_shell = gemfile_gitlab_shell.readlines()

  gems = []
  gems = gem_gitlab + gem_shell

  gitlab_gemlist = set()

  for line in gems:
    if line.startswith('  '):
      gitlab_gemlist.add(line.split()[0])
  
  return sorted(gitlab_gemlist)


def gitlab_gems_runtime(gitlab_list):
  '''file -> dictionary

  Returns a sorted list of Gitlab's runtime dependencies.

  '''
  gitlab_dict = {}
  with open(gitlab_list, 'r') as gitlab_file:
    for line in gitlab_file.readlines():
      name = '-'.join(line.split('-')[:-1])
      version = line.split('-')[-1].strip('\n')
      gitlab_dict[name] = version
  
  return gitlab_dict


def fedora_gems_rawhide(filename):
  '''file -> dictionary

  Returns a list of rubygems currently packaged in Fedora.
  
  Note: Input as a filename the one with gitlab gems in it (eg. gitlab53-gems).
  '''
  fedora_dict = {}

  gemlist = gitlab_gems_runtime(filename).keys()

  for gem in gemlist:
    search = pkgwat.api.releases('rubygem-%s' % gem)
    version = search['rows'][0]['stable_version'].split('-')[0]
    fedora_dict[gem] = version

  return fedora_dict
  

def find_upstream_gems(gitlab_list):
  '''file -> string
  
  Returns the version of a Ruby gem taken from rubygems.org API
  Note: Input as a filename the one with gitlab gems in it (eg. gitlab53-gems).
  '''
  upstream_dict = {}
  gl_list = gitlab_gems_runtime(gitlab_list).keys()
  
  for gem in gl_list:
    url = 'https://rubygems.org/api/v1/gems/%s.json' % gem
    js = json.load(urllib2.urlopen(url))
    version = js['version']
    upstream_dict[gem] = version

  return upstream_dict


def find_common(gitlab_gemlist, fedora_gemlist):
  ''' lists -> set

  Returns a set of common items between two lists.

  >>> common_gems(['sinatra', 'sidekiq', 'sass_rails', 'sass'],['sass', 'rspec', 'sass_rails'])
  set(['sass_rails', 'sass'])
  '''
  
  return sorted(set(gitlab_gemlist) & set(fedora_gemlist))


def find_missing(gitlab_gems, common_gems):
  """lists -> list
  
  Returns a list with duplicate items removed. It searches the first list
  and if an item is not in the second list it is added to the new list.
  
  >>> find_missing([1, 2, 3, 4, 5], [2, 4])
  [1, 3, 5]
  """
  missing_gems = []
  for gem in gitlab_gems:
    if gem not in common_gems:
      missing_gems.append(gem)

  return sorted(missing_gems)


def single_gem_dependencies(gem_name):
  '''List dependencies of a gem
  '''
  
  url = 'https://rubygems.org/api/v1/gems/%s.json' % gem_name
  js = json.load(urllib2.urlopen(url))
  deps = js['dependencies']
  runtime_deps = deps['runtime']
  dev_deps =deps['development']

  return runtime_deps


def bugzilla_gems(rubygems_bugzilla_raw):
  """Returns a dictionary with rubygems pending review for Fedora 
  and their status.

  """
  bz_dict = {}
  with open(rubygems_bugzilla_raw, 'r') as f:
    for line in f.readlines():
  
      split_line = re.split(' - ', line)
      strip_rubygem = re.search(r'rubygem-[\w-]+', line).group()
      gem_name = re.sub('rubygem-', '', strip_rubygem)
      bug_id = re.search(r'\d+', line).group()
      status = re.search(r'[A-Z]+', line).group()
      assignee = split_line[1]
      description = split_line[3].strip('\n')
      bz_dict[gem_name] = [bug_id, status, assignee, description]

  return bz_dict


def created_before_than(filename, days_ago):
  
  now = time.time()
  file_creation = os.path.getctime(filename)
  time_ago = now - days_ago * 60 * 60 * 24

  return file_creation > time_ago

def dict_to_json(dictionary, json_name):
  ''' dict -> file
  Convert a given dictionary to json and save it in a file named:
  json_name. You must complete the .json yourself. 
  '''
  with open(json_name, 'w') as j:
    j.write(json.dumps(dictionary))


def populate_dicts():
  '''
  Returns a tuple with populated dictionaries in this order: 
  gitlab, fedora, upstream, all
  '''
    
  print 'Populating dictionaries, this might take some time.'
  gitlab = gitlab_gems_runtime(gitlab_gems_file)
  fedora = fedora_gems_rawhide(gitlab_gems_file)
  upstream = find_upstream_gems(gitlab_gems_file)
    
  # Write results to json
  dict_to_json(gitlab, gitlab_json)
  dict_to_json(fedora, fedora_json)
  dict_to_json(upstream, upstream_json)

  return (gitlab, fedora, upstream)

def all_versions_dict():
  '''
  Returns a list with these dictionaries in this order:
  gitlab, fedora, upstream
  '''

  dicts = populate_dicts()
  versions = {}
  for gem in dicts[0].keys():
    versions[gem] = [dicts[0][gem], dicts[1][gem], dicts[2][gem]]
 
  return versions

def wiki_table():
  '''
  Wikify the versions of gems among gitlab, fedora and upstream.
  Results go in https://fedoraproject.org/wiki/User:Axilleas/GitLab
  '''
  gitlab = gitlab_gems_runtime(gitlab_gems_file)
  versions = all_versions_dict()

  with open(versions_table, 'a') as f:
    for gem in sorted(gitlab.keys()):
      f.write('|-' + '\n' + '|' + gem + '\n' + '|' + versions[gem][0] + '\n' + '|' \
      + versions[gem][1] + '\n' + '|' + versions[gem][2] + '\n')


def main():
  
  gitlab = gitlab_gems_runtime(gitlab_gems_file)
  
  # All Fedora gem packages that are in repos as list
  fedora = []
  with open(rubygems_fedora,'r') as f:
    for gem in f.readlines():
      fedora.append(gem.strip('\n'))

  with open(rubygems_gitlab, 'w') as f:
    for gem in gitlab.keys():
      f.write(gem + '\n')
  
  common = find_common(gitlab.keys(), fedora)
  with open(rubygems_common, 'w') as f:
    for gem in common:
      f.write(gem + '\n')
  
  missing_gems = find_missing(gitlab.keys(), common)
  with open(rubygems_missing, 'w') as f:
    for gem in missing_gems:
      f.write(gem + '\n')
 
  bz = bugzilla_gems(gems_bugzilla)
  bz_common = []
  for gem in bz.keys():
    if gem in missing_gems:
      bz_common.append(gem)

  with open(gems_bugzilla_common, 'w') as f:
    for gem in bz_common:
      f.write(gem + '\n')
  
  print '------------------------------------------------------'
  print 'Gitlab runtime gems  : ', len(gitlab.keys())
  print 'Gems in Fedora repos : ', len(fedora)
  print 'Common gems          : ', len(common)
  print 'To be packaged       : ', len(missing_gems)
  print 'Pending review in BZ : ', len(bz_common)
  print 'When BZ go in repos  : ', len(missing_gems) - len(bz_common)
  print
  print 'Fedora will have' , round(len(missing_gems)/float(len(fedora))*100,2), '% more ruby packages, that is', len(missing_gems)+len(fedora), 'gems in total.'
  print '------------------------------------------------------'
  
if __name__ == '__main__':
  main()
