Summary:	OpenBSD's ftpd ported to Linux (with IPv6 support)
Name:		ftpd-BSD
Version:	0.3.0
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	ftp://quatramaran.ens.fr/pub/madore/ftpd-BSD/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
Buildrequires:	libwrap-devel
Buildrequires:	pam-devel
Requires:	rc-inetd
Requires:	inetdaemon
Requires:	anonftp
Provides:	ftpserver
BuildRoot:	/tmp/%{name}-%{version}-root
Obsoletes:	wu-ftpd
Obsoletes:	proftpd
Obsoletes:	heimdal-ftpd

%description
This is a Linux port of the BSD ftp server (ftpd). It doesn't have all the
bells and whistles of wu-ftpd, but it is also probably less buggy and more
secure (at least, it was certainly so before I ported it, and I hope I
didn't mess things up *too* much).

The source code was taken from the OpenBSD CVS as of 2000/01/23 (this is
between releases 2.6 and 2.7). The ftpd version number is 6.4 and this
port's version number is 0.3.0.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/man8,etc/{pam.d,sysconfig/rc-inetd}}

install -s ftpd 	$RPM_BUILD_ROOT%{_sbindir}/ftpd-BSD
install ftpd.8		$RPM_BUILD_ROOT%{_mandir}/man8/
install %{SOURCE1} 	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd
install %{SOURCE2} 	$RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE3} 	$RPM_BUILD_ROOT/etc/ftpusers

gzip -9nf README $RPM_BUILD_ROOT%{_mandir}/man8/*

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_sbindir}/ftpd-BSD
%attr(640,root,root) %{_mandir}/man8/*
%attr(640,root,root) %config %verify(not size mtime md5) /etc/pam.d/ftp
%attr(640,root,root) /etc/ftpusers
%attr(640,root,root) /etc/sysconfig/rc-inetd/ftpd
