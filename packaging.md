## Overview

Build for Fedora 19 all gitlab gems with its fixed dependencies?, skipping tests
where difficult to run and put them in a public [repo](http://repos.fedorapeople.org/repos/axilleas/gitlab/fedora-19/).

## Crappy stoppers

* Gems gitlab < fedora (hard, will have to test if work)

* Gems gitlab > fedora (easy if gitlab == upstream then ask maintainer to update, hard if gitlab < upstream then ask? maintainer to update)


## Workflow

1. Check in [table](https://fedoraproject.org/wiki/User:Axilleas/GitLab#Packages) what's missing, build next gem in line.
2. First run rpmbuild, check what fails, keep track what gets built, then build in mock.
3. Copy mockbuilds in `~/repo/gitlab/fedora-19/`
4. Make f19 git branch in `~/git/fedora/packages/`
5. mkdir gemname in `~/git/fedora/packages`, copy SPECs and commit with below messages.

------



###Track what gets built:
```
act-as-taggable         : 2.4.1 ok, test need download, no test run
backports               : 3.3.3 (gitlab 3.3.2 test and request upstream update), no test run, where to put dirs
carrierwave             : 0.9 (gitlab 0.8), license/test need download, 
celluloid               : 0.14.1  ok, license need download, spec/ does not include all needed files
chosen-rails            : 1.0.0 (gitlab 0.9.8, 2 years ago) latest version needs extra dep (compass-rails)
(compass-rails)         : required by chosen-rails-1.0.0, no test run
connection_pool         : 1.1.0  ok, test fail
d3_rails                : 3.2.8 (gitlab 3.1.10), no test included, app dir should be considered as vendor/?
descendants_tracker     : 0.0.1  ok, test fail
devise                  : 3.0.1 (gitlab 2.2.5), needs warden 1.2.3 (f19 1.2.1), needs thread_safe
(thread_safe)           : required by devise-3.0.1, test fail (see below)
devise 2.2.5            : 2.2.5 ok, tests need multi_json-1.7.2
enumerize               : 0.6.1 ok, test fail
escape_utils            : 0.3.2 (gitlab 0.2.4), test pass, ready for BZ
faraday                 : 0.8.8 (gitlab 0.8.7 test and request gitlab update), test pass
faraday_middleware      : 0.9.0  ok,
font-awesome-rails      : 3.2.1.2 ok, test fail
foreman                 : 0.63.0 ok, license need download, test fail need unpackaged gems
gemoji                  : 1.4.0 (gitlab 1.2.1 test and request gitlab update), license need download and clarification in spec
github-linguist         : 2.8.12 (gitlab 2.3.4), no test/license is shipped
github-markdown         : 0.5.3 ok, no license is shipped, test fail
github-markup           : 0.7.5 ok, test fail
gon                     : 4.1.1 ok, license not present as a file, test fail due to unpackaged gems (rabl, rabl-rails, jbuilder)
grape                   : 0.5.0 (gitlab 0.4.1), test need unpackaged gems (see Gemfile)
virtus                  : 0.5.5 ok, required by grape, test pass (1 pending)
grape-entity            : 0.3.0 ok, test fail
hipchat                 : 0.11.0 (gitlab 0.9.0), test fail
http_parser.rb          : 0.5.3 ok, test pass (need to export LANG utf8), ready for BZ
httpauth                : 0.2.0 ok, doesn't ship test
jquery-atwho-rails      : 0.3.1 (gitlab 0.3.0 test and request update), test fail (missing generator_rspec), license missing
jquery-turbolinks       : 1.0.0 ok, test in coffeescript did not check
jquery-ui-rails         : 2.0.2 (upstream 4.0.4), doesn't ship test
jwt                     : 0.1.8 ok, license not included, 
kaminari                : 0.14.1 ok, test fail due to deps (resolve later)
modernizr               : 2.6.2 ok, missing license file (report upstream), to tests available, ready for BZ
mysql2                  : 0.3.13 (gitlab 0.3.11 test and request update)
oauth2                  : 0.8.1 (upstream 0.9.2), required by omniauth-oauth2, test fail 
omniauth                : 1.1.4 ok, submitted to BZ , required by omniauth-oauth2
omniauth-github         : 1.1.0 ok, missing license file, 
omniauth-google-oauth2  : 0.2.0 (gitlab 0.1.19), missing license/url (report upstream), test fail
omniauth-oauth          : 1.0.1 ok, test fail
omniauth-oauth2         : 1.1.1 ok, missing license file (report upstream), 1.1.1 needs oauth2 < 0.9
omniauth-twitter        : 1.0.0 (gitlab 0.0.17), missing license file (report upstream), test fail
orm_adapter             : 0.4.0 ok, submitted to BZ 
posix-spawn             : 0.3.6 ok, test fail
puma                    : 2.4.0 (gitlab 2.3.1), test fail
pygments.rb             : 0.5.2 (gitlab 0.4.2), requires posix-spawn, yajl-ruby, todo: remove .py[oc], exclude autorequires /usr/bin/env, test pass
pyu-ruby-sasl           : 0.0.3.3 ok, license not included (report upstream), test fail due to missing gem (spec)
redis                   : 3.0.4 ok, submitted in BZ
redis-actionpack        : 3.2.3 ok, required by redis-rails, omit test
redis-activesupport     : 3.2.3 ok, required by redis-rails, omit test
redis-namespace         : 1.3.0 ok, test fail, maybe do same trick with redis
redis-rack              : 1.4.2 ok, required by redis-actionpack, test fail
redis-rails             : 3.2.3 ok, omit test
redis-store             : 1.1.3 ok, required by redis-{rails,actionpack,rack,activesupport}, test fail
yajl-ruby               : 1.1.0 ok, test pass, ready to BZ
rubyntlm                : 0.3.3 (gitlab 0.1.1), missing license (https://github.com/WinRb/rubyntlm/issues/5), test fail 
seed-fu                 : 2.2.0 ok, test not included (request upstream)
select2-rails           : 3.4.7 (gitlab 3.4.2 test and request update), missing license file (report upstream), 
settingslogic           : 2.0.9 ok, test pass, ready for submission to BZ
sidekiq                 : 2.13.0 (gitlab 2.12.4 test and request update), some test fail
simple_oauth            : 0.2.0 (gitlab 0.1.9 test and request update), some test fail
six                     : 0.2.0 ok, doesn't ship with license/tests
stamp                   : 0.5.0 ok, test pass, ready for sumbission in BZ
stringex                : 2.0.8 (gitlab 1.5.1), test fail
tinder                  : 1.9.2 ok, test fail
twitter-stream          : 0.1.16 ok, test pass, ready for sumbission in BZ
underscore-rails        : 1.5.1 (gitlab 1.4.4), license file not included (https://github.com/rweng/underscore-rails/issues/19)
unicorn                 : 4.6.3 ok, some tests fail

libv8                   : 3.16.14.1 (gitlab 3.11.8.17), missing license file (report upstream), 

raphael-rails           : 2.1.1 (gitlab git v2.1.0)

gitlab-grit             : 2.6.0, test not included
gitlab-gollum-lib       : 1.0.1, test not included
gitlab-grack            : 1.0.1, license not included, some tests fail, gemspec has the old name (request change)
gitlab-pygments.rb      : 0.3.2, license not included, in fail test, gemspec has the old name (request change)
gitlab_git              : 2.1.0, license not included, test not included (PR for gemspec: add LICENSE, spec/, support/ to files, change page url)
gitlab_omniauth-ldap    : 1.0.3, license missing, test pass

```

-----------------------------------

### Macros for Fedora spec

```
%doc %{gem_instdir}/LICENSE
%exclude %{gem_instdir}/.*

%doc %{gem_instdir}/CHANGELOG.md
%doc %{gem_instdir}/README.md
%{gem_instdir}/Gemfile
%{gem_instdir}/Rakefile
%{gem_instdir}/%{gem_name}.gemspec
%{gem_instdir}/spec/
%{gem_instdir}/test/
%{gem_instdir}/Guardfile

%check
pushd .%{gem_instdir}
testrb -Ilib test/
rspec spec/
popd

BuildRequires: rubygem(test-unit)
BuildRequires: rubygem(rspec)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(mocha)
```

------------------------

### Gem packaging on GitLab forks

#### [gitlab-grit](https://github.com/gitlabhq/grit)

All other forks depend on this. Upstream is idle for too long with many 
PRs and bugs not addressed. Seems their main concern is now rugged, a replacement 
of grit. That is the main reason GitLab went on a fork (the plan is to switch from 
grit to rugged once the latter gets all the needed functionality, likely won't happen in another year or so).
See upstream grit [sparse commits](https://github.com/mojombo/grit/commits/master) and sumbitted [issues](https://github.com/mojombo/grit/issues).

#### [gitlab-gollum-lib](https://github.com/gitlabhq/gollum-lib)

Upstream is `v1.0.6`, gitlab uses upstream's `v1.0.0` and have released a `1.0.1` version with changes:

1. `s/grit/gitlab-grit` in gemspec deps
2. rename gem name to gitlab-gollum-lib

Compare: https://github.com/gitlabhq/gollum-lib/commits/gitlab-gollum-lib with https://github.com/gollum/gollum-lib/commits/v1.0.0


#### [gitlab-grack](https://github.com/gitlabhq/grack)

Upstream was idle for some time (2 commits in 2011, 4 in 2012) and it seems GitLab
picked it off the 2010 codebase and went on to release a 1.0.1 version two months ago.
It seems that now there has been added another person to the upstream grack team
and been pushing some code recently. As ar as I know gitlab hasn't approached upstream
for their changes.

#### [gitlab-pygments.rb](https://github.com/gitlabhq/pygments.rb)

As already discussed, there is a [pending PR](https://github.com/tmm1/pygments.rb/pull/77)
to be merged upstream and finally drop the fork. 

#### [gitlab_git](https://github.com/gitlabhq/gitlab_git)

Wrapper around gitlab-grit. Not a fork but depends on gitlab-grit.

#### [gitlab_omniauth-ldap](https://github.com/gitlabhq/omniauth-ldap)

4 significant changes from upstream:

1. GitLab fork is missing the commits upstream made on 27 Sep 2012 [0]
2. GitLab fork [update net-ldap to fix LDAP authentication issues](https://github.com/gitlabhq/omniauth-ldap/commit/8c50f199f8e2d8a4dc901ddbbe3e37a2630843ac)
3. GitLab fork [fix ldap blank password](https://github.com/gitlabhq/omniauth-ldap/commit/536c321236702dd9b759831f8ce5f2bc250d43b0)
4. GitLab fork [fix some failing tests](https://github.com/gitlabhq/omniauth-ldap/commit/d92ef39dcd9a392fe458ca868e9ba2a501b11881)

[0] Compare: https://github.com/intridea/omniauth-ldap/commits/master with https://github.com/gitlabhq/omniauth-ldap/commits/master

#### gitlab_meta

Doesn't need to be packaged, it only counts the number it gets downloaded from rubygems.org





