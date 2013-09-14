%global homedir %{_datadir}/gitlab
%global repodir %{_libdir}/gitlab
%global confdir %{_sysconfdir}/gitlab

Summary:       ssh access and repository management for GitLab
Name:          gitlab-shell
Version:       1.7.1
Release:       1%{?dist}
Group:         Applications/Internet
License:       MIT
URL:           https://github.com/gitlabhq/gitlab-shell
Source0:       https://github.com/gitlabhq/gitlab-shell/archive/v%{version}.tar.gz
Requires: ruby(release)
Requires: git
Requires: redis
Requires(post): shadow-utils
BuildRequires: rubygem(spec)
BuildArch:     noarch
Provides:      %{name} = %{version}-%{release}

%description
ssh access and repository management for use with GitLab

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{name}

%prep
%setup -q

%build

%install

# Prepare directory structure

install -dm755 %{buildroot}%{homedir}
install -dm755 %{buildroot}%{homedir}/gitlab-shell
install -dm700 %{buildroot}%{homedir}/.ssh/
install -dm770 %{buildroot}%{repodir}/repositories
install -dm770 %{buildroot}%{repodir}/satellites
install -dm755 %{buildroot}%{confdir}
touch %{buildroot}%{homedir}/.ssh/authorized_keys
chmod 600 %{buildroot}%{homedir}/.ssh/authorized_keys
chmod g+s %{buildroot}%{repodir}/repositories

# Change paths in config file
sed -e "s|user: git|user: gitlab|" \
    -e "s|/home/git/repositories|%{repodir}/repositories|" \
    -e "s|/home/git|%{homedir}/|" \
    config.yml.example > %{buildroot}%{confdir}/%{name}.yml"

ln -s %{confdir}/shell.yml %{buildroot}%{homedir}/%{name}/config.yml"

cp -a CHANGELOG LICENSE README.md VERSION bin hooks lib spec support %{buildroot}%{homedir}


%check
pushd .%{homedir}
rspec spec/
popd

%post
# Add the "gitlab" user and group
getent group gitlab >/dev/null 2>&1 || groupadd -r gitlab &>/dev/null
getent passwd gitlab >/dev/null 2>&1 || \
    useradd -r -g gitlab -d $homedir -s /sbin/nologin -c "GitLab" gitlab &>/dev/null
fix_perms
exit 0

fix_perms() {
chown -R git:git $repodir $homedir
chmod -R go-rwx $homedir/.ssh
chmod g+s $datadir/repositories
}

%postun
%if getent passwd git >/dev/null 2>&1; then
userdel gitlab
%fi
%if getent group git >/dev/null 2>&1; then
groupdel gitlab
%fi

%files

%defattr(-,git,git,-)
%config(noreplace) %{confdir}/%{name}.yml
%dir %{homedir}/


%files doc


%changelog
* Sat Sep 14 2013 Axilleas Pipinellis <axilleaspi@ymail.com> - 1.7.1-1
- Initial package
