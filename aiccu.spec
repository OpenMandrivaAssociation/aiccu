############################################################
# AICCU - Automatic IPv6 Connectivity Client Utility
# by Jeroen Massar <jeroen@sixxs.net>
# (c) Copyright 2003-2005 SixXS
############################################################
# AICCU RPM Spec File
############################################################

Summary:	SixXS Automatic IPv6 Connectivity Client Utility
Name:		aiccu
Version:	2007.01.15
Release:	2
License:	BSD
Group:		System/Servers
URL:		http://www.sixxs.net/tools/aiccu/
Source0:	http://www.sixxs.net/archive/sixxs/aiccu/unix/aiccu_20070115.tar.gz
Source1:	aiccu.service
Patch0:		aiccu-cloexec.patch
Patch1:		aiccu-run.patch
Patch2:		aiccu-syslog-daemon.patch
Patch3:		aiccu-gnutls34.patch
BuildRequires:	gnutls-devel
BuildRequires:	systemd-units
Requires:	iproute2

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
%setup_compile_flags
%make RPM_OPT_FLAGS="%{optflags} -Wno-error"

%install
%makeinstall_std

# remove old-style init script
rm %{buildroot}%{_sysconfdir}/init.d/*

mkdir -p %{buildroot}%{_unitdir}
install -p %{SOURCE1} %{buildroot}%{_unitdir}/

%files
%doc doc/README doc/LICENSE
%{_sbindir}/aiccu
# aiccu.conf contains the users's SixXS password, so don't
# make it readable by non-root
%attr(600, root,root) %config(noreplace) %{_sysconfdir}/aiccu.conf
%{_unitdir}/aiccu.service
