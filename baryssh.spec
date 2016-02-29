#
# spec file for package barySSH
#

Name:           barySSH
Version:        0.2
Release:        1%{?dist}
Summary:        TCP proxy for masking underlying protocols
License:        MIT
Group:          Applications/Internet
URL:            https://github.com/blaa/barySSH
Source0:        https://github.com/blaa/barySSH/archive/v%{version}.tar.gz

BuildArch:      noarch
Requires:       python
Requires:       python-twisted


%description
TCP proxy which masks (any) underlying protocols from trivial methods of detection.
Masking is time-based (both sides need to have a synchronized clock) and it's not trivial
to unmask given secure key on both ends.  But IT'S NOT A SECURE ENCRYPTION and is NOT
MEANT to be an encryption algorithm at all.

It can be used to mask SSH connections. It's compatible with the way sslh demultiplexes SSH.

%prep
%setup -q -n barySSH-%{version}

%install
install -d -m 0755 %{buildroot}%{_bindir}
install -d -m 0755 %{buildroot}%{_docdir}/%{name}-%{version}
install -m 0755 baryssh %{buildroot}%{_bindir}/baryssh
install -m 0444 LICENSE %{buildroot}%{_docdir}/%{name}-%{version}/
install -m 0444 README.md %{buildroot}%{_docdir}/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_bindir}/baryssh
%{_docdir}/%{name}-%{version}

%changelog
* Fri Feb  26 2016 Cezary Morga <cm@therek.net>
- Initial package

