Summary:	OpenBSD's ftpd ported to Linux (with IPv6 support)
Summary(pl):	Port ftpd z OpenBSD dla Linuksa (z obs³ug± IPv6)
Name:		ftpd-BSD
Version:	0.3.3
Release:	8
License:	BSD-like
Group:		Networking/Daemons
Source0:	ftp://quatramaran.ens.fr/pub/madore/ftpd-BSD/contrib/%{name}-%{version}.tar.gz
# Source0-md5:	db925235417c8699bb1eb8ca77811fc5
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
Source4:	ftpusers.tar.bz2
# Source4-md5: 76c80b6ec9f4d079a1e27316edddbe16
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
Obsoletes:	troll-ftpd
Obsoletes:	vsftpd
Obsoletes:	wu-ftpd
Conflicts:	man-pages < 1.51

%description
This is a Linux port of the BSD ftp server (ftpd). It doesn't have all
the bells and whistles of wu-ftpd, but it is also probably less buggy
and more secure (at least, it was certainly so before I ported it, and
I hope I didn't mess things up *too* much).

The source code was taken from the OpenBSD CVS as of 2000/07/07 (this
is after release 2.7). The ftpd version number is 6.5 and this port's
version number is 0.3.2.

Package comes with anonymous upload disabled. If you really want to
enable it - chmod /home/services/ftp/upload to 0730.

%description -l pl
Pakiet ten zawiera linuksowy port serwera ftp BSD (ftpd). Nie zawiera
on wszystkich wymy¶lnych elementów wu-ftpd, jest jednak
prawdopodobniej mniej zapluskwiony i bardziej bezpieczny (w kazdym
razie by³ takim zanim go przenios³em na Linuksa, i mam nadziejê, ¿e
nie naba³agani³em *za bardzo*). Kod ¼ród³owy pochodzi z repozytorium
CVS OpenBSD z dnia 2000/07/07 (tj. po wersji 2.7). Numer wersji ftpd
to 6.5, za¶ numer wersji tego portu to 0.3.2.

Pakiet przychodzi z wy³±czonym anonimowym uploadem. Je¶li naprawdê
chcesz go w³±czyæ - zmieñ uprawnienia do /home/services/ftp/upload
na 0730.

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
	$RPM_BUILD_ROOT/home/services/ftp/{upload,pub}

install ftpd $RPM_BUILD_ROOT%{_sbindir}/ftpd-BSD
install ftpd.8 $RPM_BUILD_ROOT%{_mandir}/man8/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/sysconfig/rc-inetd/ftpd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/pam.d/ftp
install %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/ftpd/ftpusers

bzip2 -dc %{SOURCE4} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/ftp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/rc-inetd/ftpd
%dir /home/services/ftp
%dir /home/services/ftp/pub
%attr(700,root,ftp) %verify(not mode) %dir /home/services/ftp/upload
%{_mandir}/man8/*
%lang(ja) %{_mandir}/ja/man5/ftpusers*
%lang(pl) %{_mandir}/pl/man5/ftpusers*
%lang(pt_BR) %{_mandir}/pt_BR/man5/ftpusers*
%lang(ru) %{_mandir}/ru/man5/ftpusers*
