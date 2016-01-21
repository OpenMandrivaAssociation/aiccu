############################################################
# AICCU - Automatic IPv6 Connectivity Client Utility
# by Jeroen Massar <jeroen@sixxs.net>
# (c) Copyright 2003-2005 SixXS
############################################################
# AICCU RPM Spec File
############################################################

Summary:   SixXS Automatic IPv6 Connectivity Client Utility
Name:      aiccu
Version:   2007.01.15
Release:   1
License:   BSD
Group:     System/Servers
URL:       http://www.sixxs.net/tools/aiccu/
Source0:    http://www.sixxs.net/archive/sixxs/aiccu/unix/aiccu_20070115.tar.gz
Source1:   aiccu.service
Patch0: aiccu-cloexec.patch
Patch1: aiccu-run.patch
Patch2: aiccu-syslog-daemon.patch
Patch3: aiccu-gnutls34.patch
BuildRequires: gnutls-devel
BuildRequires: systemd-units
Requires:  iproute2
Requires(post): systemd-units
Requires(preun): systemd-units
Requires(postun): systemd-units

%description
This client automatically gives one IPv6 connectivity
without having to manually configure interfaces etc.
One does need a SixXS account and at least a tunnel. These
can be freely & gratis requested from the SixXS website.
For more information about SixXS check http://www.sixxs.net

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1 -b .run
%patch2 -p1 -b .syslog-daemon
%patch3 -p1

# fix executable permissions on non-executable content
# so debuginfo can pick them up properly
find . -type f -not -name rules -and -not -name *init* -exec chmod a-x \{\} \;

%build
%make RPM_OPT_FLAGS="$RPM_OPT_FLAGS -Wno-error"

%install
mkdir -p $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# remove old-style init script
rm $RPM_BUILD_ROOT%{_sysconfdir}/init.d/*

mkdir -p $RPM_BUILD_ROOT%{_unitdir}
install -p %{SOURCE1} $RPM_BUILD_ROOT%{_unitdir}/

%post
%systemd_post aiccu.service

%preun
%systemd_preun aiccu.service

%postun
%systemd_postun_with_restart aiccu.service 

%files
%doc doc/README doc/LICENSE
%{_sbindir}/aiccu
# aiccu.conf contains the users's SixXS password, so don't
# make it readable by non-root
%attr(600, root,root) %config(noreplace) %{_sysconfdir}/aiccu.conf
%{_unitdir}/aiccu.service
