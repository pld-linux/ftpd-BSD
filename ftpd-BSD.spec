Summary:	OpenBSD's ftpd ported to Linux (with IPv6 support)
Summary(pl):	Port ftpd z OpenBSD dla Linuxa (z obs�ug� IPv6)
Name:		ftpd-BSD
Version:	0.3.3
Release:	6
License:	BSD-like
Group:		Networking/Daemons
Source0:	ftp://quatramaran.ens.fr/pub/madore/ftpd-BSD/contrib/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
Patch0:		%{name}-anonuser.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-username.patch
Patch3:		%{name}-SA_LEN.patch
Patch4:		%{name}-no_libnsl.patch
URL:		http://www.eleves.ens.fr:8080/home/madore/programs/#prog_ftpd-BSD
Buildrequires:	libwrap-devel
Buildrequires:	pam-devel
Requires:	rc-inetd
Requires:	inetdaemon
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Provides:	ftpserver
Obsoletes:	ftpserver
Obsoletes:	anonftp
Obsoletes:	bftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	muddleftpd
Obsoletes:	proftpd
Obsoletes:	proftpd-common
Obsoletes:	proftpd-inetd
Obsoletes:	proftpd-standalone
Obsoletes:	pure-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd

%description
This is a Linux port of the BSD ftp server (ftpd). It doesn't have all
the bells and whistles of wu-ftpd, but it is also probably less buggy
and more secure (at least, it was certainly so before I ported it, and
I hope I didn't mess things up *too* much).

The source code was taken from the OpenBSD CVS as of 2000/07/07 (this
is after release 2.7). The ftpd version number is 6.5 and this port's
version number is 0.3.2.

Package comes with anonymous upload disabled. If you really want to
enable it - chmod /home/ftp/upload to 0730.

%description -l pl
Pakiet ten zawiera linuksowy port serwera ftp BSD (ftpd). Nie zawiera
on wszystkich wymy�lnych element�w wu-ftpd, jest jednak
prawdopodobniej mniej zapluskwiony i bardziej bezpieczny (w kazdym
razie by� takim zanim go przenios�em na Linuksa, i mam nadziej�, �e
nie naba�agani�em *za bardzo*). Kod �r�d�owy pochodzi z repozytorium
CVS OpenBSD z dnia 2000/07/07 (tj. po wersji 2.7). Numer wersji ftpd
to 6.5, za� numer wersji tego portu to 0.3.2.

Pakiet przychodzi z wy��czonym anonimowym uploadem. Je�li naprawd�
chcesz go w��czy� - zmie� uprawnienia do /home/ftp/upload na 0730.

%prep
%setup -q -n ftpd-bsd-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%{__make} OPT_CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8} \
	$RPM_BUILD_ROOT%{_sysconfdir}/{ftpd,pam.d,sysconfig/rc-inetd} \
	$RPM_BUILD_ROOT/home/ftp/{upload,pub}

install ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd-BSD
install ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/ftpusers

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rc-inetd start\" to start inet server" 1>&2
fi

%postun
if [ -f /var/lock/subsys/rc-inetd ]; then
	/etc/rc.d/init.d/rc-inetd reload
fi

%files
%defattr(644,root,root,755)
%doc README*
%attr(755,root,root) %{_sbindir}/ftpd-BSD
%dir %{_sysconfdir}/ftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pam.d/ftp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/rc-inetd/ftpd
%dir /home/ftp
%dir /home/ftp/pub
%attr(700,root,ftp) %verify(not mode) %dir /home/ftp/upload
%{_mandir}/man8/*
