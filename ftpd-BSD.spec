Summary:	OpenBSD's ftpd ported to Linux (with IPv6 support)
Summary(pl):	Port ftpd z OpenBSD dla Linuxa (z wsparciem do IPv6)
Name:		ftpd-BSD
Version:	0.3.3
Release:	1
License:	BSD-like
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Source0:	ftp://quatramaran.ens.fr/pub/madore/ftpd-BSD/contrib/%{name}-%{version}.tar.gz
Source1:	%{name}.inetd
Source2:	%{name}.pamd
Source3:	%{name}-ftpusers
Patch0:		%{name}-anonuser.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-username.patch
Patch3:		%{name}-SA_LEN.patch
Patch4:		ftpd-BSD-no_libnsl.patch
URL:		http://www.eleves.ens.fr:8080/home/madore/programs/#prog_ftpd-BSD
Buildrequires:	libwrap-devel
Buildrequires:	pam-devel
Requires:	rc-inetd
Requires:	inetdaemon
Provides:	ftpserver
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Obsoletes:	bftpd
Obsoletes:	heimdal-ftpd
Obsoletes:	linux-ftpd
Obsoletes:	proftpd
Obsoletes:	pure-ftpd
Obsoletes:	wu-ftpd
Obsoletes:	muddleftpd

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
on wszystkich wymy¶lnych elementów wu-ftpd, jest jednak
prawdopodobniej mniej zapluskwiony i bardziej bezpieczny (w kazdym
razie by³ takim zanim go przenios³em na Linuksa, i mam nadziejê, ¿e
nie naba³agani³em *za bardzo*). Kod ¼ród³owy pochodzi z repozytorium
CVS OpenBSD z dnia 2000/01/23 (tj. miêdzy wersj± 2.6 a 2.7). Numer
wersji ftpd to 6.4, za¶ numer wersji tego portu to 0.3.0.

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
%dir %{_sysconfdir}/ftpd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/pam.d/ftp
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ftpd/ftpusers
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sysconfig/rc-inetd/ftpd
%dir /home/ftp 
%dir /home/ftp/pub 
%attr(755,ftp,ftp) %dir /home/ftp/upload
%{_mandir}/man8/*
