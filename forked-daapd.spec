#
# Needs libevent version 1; use branch japhy-libevent1_on_th for Th.
#
Summary:	DAAP and RSP media server
Summary(pl.UTF-8):	Serwer multimediów DAAP i RSP
Name:		forked-daapd
Version:	0.16
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Source0:	http://alioth.debian.org/~jblache/forked-daapd/%{name}-%{version}.tar.gz
# Source0-md5:	cc35619babefea35db9ee22e6f1d036b
Source1:	%{name}.init
URL:		http://blog.technologeek.org/category/hacks/forked-daapd
BuildRequires:	alsa-lib-devel
BuildRequires:	avahi-devel
BuildRequires:	ffmpeg-devel
BuildRequires:	flac-devel
BuildRequires:	gperf
BuildRequires:	libantlr3c-devel
BuildRequires:	libavl-devel
BuildRequires:	libconfuse-devel
BuildRequires:	libevent-devel < 2
BuildRequires:	libgcrypt-devel
BuildRequires:	libplist-devel
BuildRequires:	libunistring-devel
BuildRequires:	mxml-devel
BuildRequires:	pkg-config
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRequires:	sed >= 4.0
BuildRequires:	sqlite3-devel
BuildRequires:	sqlite3-devel(load_extension)
BuildRequires:	sqlite3-devel(unlock_notify)
BuildRequires:	taglib-devel
BuildRequires:	zlib-devel
Requires:	sqlite3(load_extension)
Requires:	sqlite3(unlock_notify)
Provides:	group(forked-daapd)
Provides:	user(forked-daapd)
Requires:	rc-scripts
Requires(postun):	/usr/sbin/userdel
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(postun):	/usr/sbin/groupdel
Requires(pre):	/usr/bin/getgid
Requires(pre):	/usr/sbin/groupadd
Obsoletes:	mt-daapd
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
forked-daapd is a DAAP and RSP media server, with support for Linux
and FreeBSD. It is a complete rewrite of mt-daapd (Firefly Media
Server).

%description -l pl.UTF-8
forked-daapd jest serwerem multimediów DAAP i RSP działającym w
Linuksie i FreeBSD. Jest kompletną reimplementacją mt-daapd (Firefly
Media Server)

%prep
%setup -q
# sed -i~ 's!event-config.h!event2/event-config.h!' src/ev*/*.c
sed -i~ '/uid =/s/daapd/forked-daapd/' forked-daapd.conf
sed -i~ 's!/var/log/!/var/log/forked-daapd/!' forked-daapd.conf

%build
%configure \
	--enable-flac \
	--enable-musepack \
	--enable-itunes

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d/ $RPM_BUILD_ROOT/var/log/forked-daapd/
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 263 forked-daapd
%useradd -u 263 -d /var/cache/forked-daapd -g forked-daapd -c "%{name} user" forked-daapd

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = 0 ]; then
        %service %{name} stop
        /sbin/chkconfig --del %{name}
fi

%postun
if [ "$1" = "0" ]; then
        %userremove forked-daapd
        %groupremove forked-daapd
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog* NEWS README UPGRADING
%attr(755,root,root) %{_sbindir}/forked-daapd
%attr(755,root,root) %{_libdir}/%{name}/*.so
%{_libdir}/%{name}/*.la
%{_mandir}/man8/%{name}.8*
%attr(755,forked-daapd,forked-daapd) %dir /var/cache/forked-daapd
%attr(755,forked-daapd,forked-daapd) %dir /var/log/forked-daapd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/forked-daapd.conf
%attr(755,root,root) /etc/rc.d/init.d/%{name}
