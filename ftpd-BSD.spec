Summary:	OpenBSD's ftpd ported to Linux
Name:		ftpd-BSD
Version:	0.2.3
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Source0:	%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pamd
BuildRoot:	/tmp/%{name}-%{version}-root
Requires:	rc-inetd
Requires:	inetdaemon
Requires:	anonftp
Provides:	ftpserver

%description
This is a Linux port of the BSD ftp server (ftpd).  It doesn't have
all the bells and whistles of wu-ftpd, but it is also probably less
buggy and more secure (at least, it was certainly so before I ported
it, and I hope I didn't mess things up *too* much).

The source code was taken from the OpenBSD 2.6 distribution.  The ftpd
version number is 6.4 and this port's version number is 0.2.3.

%prep
%setup -q

%build
make

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/{%{_sbindir},%{_mandir}/man8,etc/{pam.d,sysconfig/rc-inetd}}

install -s ftpd 	$RPM_BUILD_ROOT%{_sbindir}/ftpd-BSD
install ftpd.8		$RPM_BUILD_ROOT%{_mandir}/man8/ftpd-BSD.8
install %{SOURCE1} 	$RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftp
install %{SOURCE2} 	$RPM_BUILD_ROOT/etc/pam.d/ftp

gzip -9nf README $RPM_BUILD_ROOT%{_mandir}/man8/*

cat << EOF >$RPM_BUILD_ROOT/etc/ftpusers
root
bin
daemon
adm
lp
sync
shutdown
halt
mail
news
uucp
operator
games
nobody
EOF

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet sever" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd restart
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz
%attr(755,root,root) %{_sbindir}/ftpd-BSD
%attr(640,root,root) %{_mandir}/man8/*
%attr(640,root,root) /etc/pam.d/ftp
%attr(640,root,root) /etc/ftpusers
%attr(640,root,root) /etc/sysconfig/rc-inetd/ftp
