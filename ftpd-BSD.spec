Summary:	OpenBSD's ftpd ported to Linux (with IPv6 support)
Summary(pl):	Port ftpd z OpenBSD dla Linuxa (z wsparciem do IPv6)
Name:		ftpd-BSD
Version:	0.3.2
Release:	5
License:	BSD-like
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://quatramaran.ens.fr/pub/madore/ftpd-BSD/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
Patch0:		%{name}-anonuser.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-username.patch
Buildrequires:	libwrap-devel
Buildrequires:	pam-devel
Requires:	rc-inetd
Requires:	inetdaemon
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	wu-ftpd
Obsoletes:	proftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd

%description
This is a Linux port of the BSD ftp server (ftpd). It doesn't have all
the bells and whistles of wu-ftpd, but it is also probably less buggy
and more secure (at least, it was certainly so before I ported it, and
I hope I didn't mess things up *too* much).

The source code was taken from the OpenBSD CVS as of 2000/01/23 (this
is between releases 2.6 and 2.7). The ftpd version number is 6.4 and
this port's version number is 0.3.0.

%description -l pl
Pakiet ten zawiera linuksowy port serwera ftp BSD (ftpd). Nie zawiera
on wszystkich wymy�lnych element�w wu-ftpd, jest jednak
prawdopodobniej mniej zapluskwiony i bardziej bezpieczny (w kazdym
razie by� takim zanim go przenios�em na Linuksa, i mam nadziej�, �e
nie naba�agani�em *za bardzo*). Kod �r�d�owy pochodzi z repozytorium
CVS OpenBSD z dnia 2000/01/23 (tj. mi�dzy wersj� 2.6 a 2.7). Numer
wersji ftpd to 6.4, za� numer wersji tego portu to 0.3.0.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch1 -p2

%build
%{__make} -C ftpd OPT_CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debug:-O -g}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ftpd,pam.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/home/ftp/{upload,pub}

install ftpd/ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd-BSD
install ftpd/ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/ftpusers

gzip -9nf README

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pam.d/ftp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/rc-inetd/ftpd
%dir /home/ftp 
%dir /home/ftp/pub 
%attr(755,ftp,ftp) %dir /home/ftp/upload
%{_mandir}/man8/*
