%bcond_without pgm

Name:           zeromq4
Version:        4.1.4
Release:        2
Summary:        Software library for fast, message-based applications

Group:          System Environment/Libraries
License:        LGPLv3+ with exceptions
URL:            http://www.zeromq.org/
Source0:        %{name}-%{version}.tar.gz
BuildRequires:  glib2-devel
BuildRequires:  libuuid-devel
BuildRequires:  libsodium-devel
%if %{with pgm}
BuildRequires:  openpgm-devel
%endif
BuildRequires:  chrpath

Provides:       zeromq3 = %{version}-%{release}
Obsoletes:      zeromq3 < 3.2.4-2

%description
The 0MQ lightweight messaging kernel is a library which extends the
standard socket interfaces with features traditionally provided by
specialized messaging middle-ware products. 0MQ sockets provide an
abstraction of asynchronous message queues, multiple messaging
patterns, message filtering (subscriptions), seamless access to
multiple transport protocols and more.

This package contains the ZeroMQ shared library for versions 4.x.


%package devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Conflicts:      zeromq-devel%{?_isa}
Provides:       zeromq3-devel = %{version}-%{release}
Obsoletes:      zeromq3-devel < 3.2.4-2


%description devel
The %{name}-devel package contains libraries and header files for 
developing applications that use %{name} 4.x.


%prep
%setup -qn %{name}-%{version}
chmod -x src/tcp.cpp
chmod -x src/dist.cpp

# Generate configure script
./autogen.sh

# Don't turn warnings into errors
sed -i "s/libzmq_werror=\"yes\"/libzmq_werror=\"no\"/g" \
    configure


%build
%configure \
%if %{with pgm}
            --with-system-pgm \
%endif
            --disable-static \
            --disable-silent-rules
make %{?_smp_mflags}


%install
make install DESTDIR=%{buildroot} INSTALL="install -p"
chrpath --delete %{buildroot}%{_bindir}/curve_keygen

# remove *.la
rm %{buildroot}%{_libdir}/libzmq.la


%check
make check


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc AUTHORS COPYING COPYING.LESSER NEWS
%{_bindir}/curve_keygen
%{_libdir}/libzmq.so.*

%files devel
%{_libdir}/libzmq.so
%{_libdir}/pkgconfig/libzmq.pc
%{_includedir}/zmq*
%{_mandir}/man3/zmq*.3*
%{_mandir}/man7/zmq*.7*


%changelog
* Mon Nov 09 2015 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com.pl> 4.1.4-2
- tito: use ReleaseTagger (tomasz.rostanski@thalesgroup.com.pl)
- Fix test_filter_ipc for cleared supplementary groups (ab@fmap.me)
- zeromq4.spec: remove dist name from rpm version
  (tomasz.rostanski@thalesgroup.com.pl)

* Mon Nov 2 2015 Tomasz Rostanski <tomasz.rostanski@thalesgroup.com> - 4.1.4-1
- updated to 4.1.4

* Mon Sep 22 2014 Thomas Spura <tomspur@fedoraproject.org> - 4.0.4-2
- fix buildroot macros (#1069556)

* Thu Apr 17 2014 Thomas Spura <tomspur@fedoraproject.org> - 4.0.4-1
- update to 4.0.4

* Tue Feb 25 2014 Thomas Spura <tomspur@fedoraproject.org> - 4.0.3-2
- fix spurious-executable-perm
- also provide/obsolete zeromq3-devel

* Tue Feb  4 2014 Thomas Spura <tomspur@fedoraproject.org> - 4.0.3-1
- disable silent rules in configure
- delete rpath with chrpath
- provide zeromq3 with the version from zeromq4

* Thu Dec 12 2013 Jose Pedro Oliveira <jpo at di.uminho.pt> - 4.0.3-0.1
- initial zeromq v4 package (based on zeromq3's specfile)

# vim:set ai ts=4 sw=4 sts=4 et:
