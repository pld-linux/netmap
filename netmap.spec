Summary:	Network weathermap creator
Summary(pl):	Kreator sieciowych map pogody
Name:		netmap
Version:	1.3.0
Release:	1
License:	GPL v2
Group:		Networking
Source0:	http://aetos.it.teithe.gr/~v13/netmap/%{name}-%{version}.tar.gz
# Source0-md5:	dde4ac662f207b69c3b8f3d82720e433
URL:		http://aetos.it.teithe.gr/~v13/netmap/
BuildRequires:	libpq++-devel
BuildRequires:	openssl-devel
BuildRequires:	net-snmp-devel
BuildRequires:	v-lib-devel >= 1.5.3.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/%{name}

%description
Netmap is a program to create network weathermaps based on existing
images created by other software. It uses SNMP to collect data from
other devices and it does not depend on MRTG or any other statistics
program.

%description -l pl
Netmap to program do tworzenia sieciowych map pogody w oparciu o
istniej±ce obrazy stworzone innym oprogramowaniem. U¿ywa SNMP do
gromadzenia danych z innych urz±dzeñ i nie wymaga MRTG ani ¿adnego
innego programu do statystyk.

%prep
%setup -q

%build
sed -i -e 's#ADMINDIR=.*#ADMINDIR=%{_datadir}/%{name}/admin#g' configure*
sed -i -e 's#UIDIR=.*#UIDIR=%{_datadir}/%{name}/ui#g' configure*
%configure \
	--enable-mod_php \
	--with-openssl=%{_libdir} \
	--with-snmp=%{_prefix}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/cron.d,/var/lib/%{name}/{cache,img}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

echo "*/10 * * * * nobody %{_bindir}/netmap > /dev/null" > $RPM_BUILD_ROOT/etc/cron.d/%{name}

mv -f $RPM_BUILD_ROOT%{_sysconfdir}/db.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/db.conf
mv -f $RPM_BUILD_ROOT%{_sysconfdir}/netmap.conf.sample $RPM_BUILD_ROOT%{_sysconfdir}/netmap.conf

rm -rf $RPM_BUILD_ROOT%{_prefix}/db

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog doc/*.ps
%doc db/create.sql db/*db
/etc/cron.d/%{name}
%dir %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/netmap.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/db.conf
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}
%dir /var/lib/%{name}
%attr(770,root,http) /var/lib/%{name}/*
