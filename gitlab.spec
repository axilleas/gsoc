%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}


%global appdir %{_var}/lib/gitlab
%global apprundir %{_var}/run/gitlab

%global homedir %{_datarootdir}/%{name}
%global datadir %{_sharedstatedir}/%{name}
%global confdir deploy/common

%{_libdir} 	/usr/lib
%{_sharedstatedir} 	/var/lib
%{_sysconfdir} 	/etc

Summary:       Self hosted Git management software
Name:          gitlab
Version:       6.0.1
Release:       1%{?dist}
Group:         Applications/Internet
License:       MIT
URL:           http://www.gitlab.org
Source0:       
BuildArch:     noarch
Provides:      gitlab = %{version}-%{release}

Requires: ruby(release)
Requires: ruby(rubygems)

Requires:      systemd-units

# regular packages
Requires: git
Requires: openssh-server
Requires: redis
Requires: python

# gems
Requires: %{name}-shell
Requires: rubygem-rails = 3.2.13
Requires: rubygem-mysql2
Requires: rubygem-pg
Requires: rubygem-devise >= 2.2
Requires: rubygem-devise < 3.0
Requires: rubygem-omniauth >= 1.1.3
Requires: rubygem-omniauth < 1.2
Requires: rubygem-omniauth-google-oauth2
Requires: rubygem-omniauth-twitter
Requires: rubygem-omniauth-github
Requires: rubygem-gitlab_git = 2.1.1
Requires: rubygem-gitlab-grack >= 1.0.1 # require: 'grack'
Requires: rubygem-gitlab-grack < 1.1    # require: 'grack'
Requires: rubygem-gitlab_omniauth-ldap = 1.0.3 # require: "omniauth-ldap"
Requires: rubygem-gitlab-pygments.rb >= 0.5.2 # require: 'pygments.rb'
Requires: rubygem-gitlab-pygments.rb < 0.6   # require: 'pygments.rb'
Requires: rubygem-gitlab-gollum-lib >= 1.0.1  # require: 'gollum-lib'
Requires: rubygem-gitlab-gollum-lib < 1.1     # require: 'gollum-lib'
Requires: rubygem-github-linguist # require: "linguist"
Requires: rubygem-grape >= 0.5.0
Requires: rubygem-grape < 0.6
Requires: rubygem-grape-entity >= 0.3.0
Requires: rubygem-grape-entity < 0.4
Requires: rubygem-stamp
Requires: rubygem-enumerize
Requires: rubygem-kaminari >= 0.14.1
Requires: rubygem-kaminari < 0.15
Requires: rubygem-haml-rails
Requires: rubygem-carrierwave
Requires: rubygem-six
Requires: rubygem-seed-fu
Requires: rubygem-redcarpet >= 2.2.2
Requires: rubygem-redcarpet < 2.3
Requires: rubygem-github-markup >= 0.7.4  # require: 'github/markup'
Requires: rubygem-github-markup < 0.8     # require: 'github/markup'
Requires: rubygem-asciidoctor
Requires: rubygem-unicorn >= 4.6.3
Requires: rubygem-unicorn < 4.7
Requires: rubygem-state_machine
Requires: rubygem-acts-as-taggable-on
Requires: rubygem-slim
Requires: rubygem-sinatra # require: nil
Requires: rubygem-sidekiq
Requires: rubygem-httparty
Requires: rubygem-colored
Requires: rubygem-settingslogic
Requires: rubygem-foreman
Requires: rubygem-redis-rails
Requires: rubygem-tinder >= 1.9.3
Requires: rubygem-tinder < 1.10
Requires: rubygem-hipchat >= 0.9.0
Requires: rubygem-hipchat < 0.10
Requires: rubygem-d3_rails >= 3.1.4
Requires: rubygem-d3_rails < 3.2
Requires: rubygem-underscore-rails >= 1.4.4
Requires: rubygem-underscore-rails < 1.5
Requires: rubygem-sanitize
Requires: rubygem-sass-rails
Requires: rubygem-coffee-rails
Requires: rubygem-uglifier
Requires: rubygem-therubyracer
Requires: rubygem-turbolinks
Requires: rubygem-jquery-turbolinks
Requires: rubygem(chosen-rails) = 1.0.0
Requires: rubygem(select2-rails)
Requires: rubygem(jquery-atwho-rails) = 0.3.0
Requires: rubygem(jquery-rails) = 2.1.3
Requires: rubygem(jquery-ui-rails) = 2.0.2
Requires: rubygem(modernizr) = 2.6.2
Requires: rubygem(raphael-rails)
Requires: rubygem(bootstrap-sass)
Requires: rubygem(font-awesome-rails)
Requires: rubygem(gemoji) >= 1.2.1 # require: 'emoji/railtie'
Requires: rubygem(gemoji) < 1.3
Requires: rubygem(gon)

BuildRequires: ruby(release)
BuildRequires: ruby-devel
BuildRequires: ruby
BuildRequires: systemd-units

%description


%prep
%setup -q


%build

%install
#prepare dir structure
install -d -m0755 %{buildroot}%{homedir}
install -d -m0755 %{buildroot}%{datadir}
install -d -m0755 %{buildroot}%{datadir}/tmp
install -d -m0755 %{buildroot}%{datadir}/tmp/pids
install -d -m0755 %{buildroot}%{datadir}/config

mkdir -p %{buildroot}%{_unitdir}
mv %{buildroot}%{brokerdir}/systemd/unicorn.service %{buildroot}%{_unitdir}
mv %{buildroot}%{brokerdir}/systemd/sidekiq.service %{buildroot}%{_unitdir}

%post
systemctl --system daemon-reload

%files
%doc LICENSE COPYRIGHT

%defattr(-,git,git,-)
%config(noreplace) 

%files doc


%changelog
