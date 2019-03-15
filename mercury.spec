Name:		mercury
Version:	1.0.1
Release:	2%{?dist}

Summary:	Mercury

Group:		Development/Libraries
License:	ANL
URL:		http://mercury-hpc.github.io/documentation/
Source0:	https://github.com/mercury-hpc/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.bz2
#Patch1:		https://github.com/mercury-hpc/mercury/commit/9f9dd80164a2b14b184f2b373efeb50a5fc80dc5.patch
Patch1:		https://github.com/mercury-hpc/mercury/compare/c68870ffc0409c29eece5ba036c6efd3c22cee41^...v1.0.1.patch

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
%setup -q
%patch1 -R -p1

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
%doc

%files devel
%{_includedir}
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_datadir}/cmake/


%changelog
* Fri Mar 15 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-2
- add patch to revert back to Dec 06, 2018 c68870f

* Mon Mar 11 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-1
- update to 1.0.1
- add patch for "HG Core: fix missing static inline in mercury_core.h"

* Wed Oct 24 2018 Brian J. Murrell <brian.murrell@intel> - 0.9.0-1.git.0f8f25b
- update mercury to git sha1 0f8f25bb3d57f117979de65cc3c05cf192cf4b31

* Mon Aug 20 2018 Brian J. Murrell <brian.murrell@intel> - 0.9.0-1.git.f7f6955
- initial package
