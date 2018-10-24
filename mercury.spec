%global commit0 0f8f25bb3d57f117979de65cc3c05cf192cf4b31
%global shortcommit0 %%(c=%%{commit0}; echo ${c:0:7})
%global commit1 9da3e5bc847fa4187f42f60700e343a9ed09a161
%global shortcommit1 %%(c=%%{commit1}; echo ${c:0:7})
%global commit2 749783cf72ae26dd668c5539afd9990d0cf0a053
%global shortcommit2 %%(c=%%{commit2}; echo ${c:0:7})
%global commit3 5092f6bc2af791310390b0ff66f2e1264a9f3bd5
%global shortcommit3 %%(c=%%{commit3}; echo ${c:0:7})

%bcond_with use_release

Name:		mercury
Version:	0.9.0
Release:	1.git.%{shortcommit0}%{?dist}

Summary:	Mercury

Group:		Development/Libraries
License:	ANL
URL:		http://mercury-hpc.github.io/documentation/
%if %{with use_release}
Source0:	https://github.com/mercury-hpc/mercury/releases/download/%{shortcommit0}/mercury-%{shortcommit0}.tar.bz2
Patch1:		v0.9.0..f7f6955.patch
%else
#Source0:	https://github.com/mercury-hpc/mercury/releases/download/v%{version}/mercury-%{version}.tar.bz2
Source0:	https://github.com/mercury-hpc/mercury/archive/%{shortcommit0}.tar.gz
Source1:	https://github.com/mercury-hpc/kwsys/archive/%{shortcommit1}.tar.gz
Source2:	https://github.com/mercury-hpc/preprocessor/archive/%{shortcommit2}.tar.gz
Source3:	https://github.com/mercury-hpc/mchecksum/archive/%{shortcommit3}.tar.gz
%endif

BuildRequires:	openpa-devel
BuildRequires:	libfabric-devel >= 1.5.0
BuildRequires:	cmake
BuildRequires:	boost-devel

%description
Mercury

%package devel
Summary:	Mercury devel package

%description devel
Mercury devel

%prep
%if %{with use_release}
%setup -q
%patch1 -p1
%else
%setup -q -n mercury-%{commit0}
rmdir Testing/driver/kwsys/
tar -C Testing/driver/ -xzf %{SOURCE1}
mv Testing/driver/kwsys{-%{commit1},}
rmdir src/boost
%endif
tar -C src -xzf %{SOURCE2}
mv src/preprocessor-%{commit2} src/boost
%if ! %{with use_release}
rmdir src/mchecksum
tar -C src -xzf %{SOURCE3}
mv src/mchecksum{-%{commit3},}
%endif

%build
mkdir build
cd build
MERCURY_SRC=".."
cmake -DMERCURY_USE_CHECKSUMS=OFF                \
      -DCMAKE_INSTALL_PREFIX=%{_prefix}          \
      -DBUILD_EXAMPLES=OFF                       \
      -DMERCURY_USE_BOOST_PP=ON                  \
      -DMERCURY_USE_SYSTEM_BOOST=ON              \
      -DMERCURY_USE_SELF_FORWARD=ON              \
      -DMERCURY_ENABLE_VERBOSE_ERROR=ON          \
      -DBUILD_TESTING=ON                         \
      -DNA_USE_OFI=ON                            \
      -DBUILD_DOCUMENTATION=OFF                  \
      -DMERCURY_INSTALL_LIB_DIR=%{_libdir}       \
      -DBUILD_SHARED_LIBS=ON $MERCURY_SRC        \
      ..
make %{?_smp_mflags}


%install
cd build
%make_install


%files
%{_libdir}/*.so.*
%if %{with use_release}
%endif
%doc

%files devel
%{_includedir}
%{_libdir}/*.so
%if %{with use_release}
%endif
%{_libdir}/pkgconfig
%{_datadir}/cmake/


%changelog
* Wed Oct 24 2018 Brian J. Murrell <brian.murrell@intel> - 0.9.0-1.git.0f8f25b
- update mercury to git sha1 0f8f25bb3d57f117979de65cc3c05cf192cf4b31

* Mon Aug 20 2018 Brian J. Murrell <brian.murrell@intel> - 0.9.0-1.git.f7f6955
- initial package
