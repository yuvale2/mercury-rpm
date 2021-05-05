Name: mercury
Version: 2.0.1~rc1
Release: 1%{?dist}

# dl_version is version with ~ removed
%{lua:
    rpm.define("dl_version " .. string.gsub(rpm.expand("%{version}"), "~", ""))
}

Summary:	Mercury

Group:		Development/Libraries
License:	Aregonee National Laboratory, Department of Energy License
URL:		http://mercury-hpc.github.io/documentation/
Source0:	https://github.com/mercury-hpc/mercury/archive/v%{dl_version}.tar.gz

%if 0%{?suse_version} > 0
BuildRequires:	libatomic1
%else
%if 0%{?rhel} < 8
BuildRequires:	openpa-devel
%endif
%endif
BuildRequires:	libfabric-devel >= 1.9.0-5
BuildRequires:	cmake
BuildRequires:	boost-devel
BuildRequires:	gcc-c++
%if 0%{?sle_version} >= 150000
# have choice for libffi.so.7()(64bit) needed by python3-base: ghc-bootstrap libffi7
# have choice for libffi.so.7(LIBFFI_BASE_7.0)(64bit) needed by python3-base: ghc-bootstrap libffi7
# have choice for libffi.so.7(LIBFFI_CLOSURE_7.0)(64bit) needed by python3-base: ghc-bootstrap libffi7
BuildRequires: libffi7
%endif
# according to https://en.opensuse.org/openSUSE:Build_Service_cross_distribution_howto
# this should be 120300
# according to my debugging, it's not even set until the rpm is being built
%if 0%{?suse_version} >= 1315 && !0%{?is_opensuse}
# have choice for libpsm_infinipath.so.1()(64bit) needed by libfabric1: libpsm2-compat libpsm_infinipath1
# have choice for libpsm_infinipath.so.1()(64bit) needed by openmpi-libs: libpsm2-compat libpsm_infinipath1
BuildRequires: libpsm_infinipath1
%endif


%description
Mercury

%package devel
Summary:	Mercury devel package
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	libfabric-devel >= 1.9.0-5

%description devel
Mercury devel

%prep

%autosetup -n mercury-%dl_version

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
      -DBUILD_TESTING=OFF                        \
      -DNA_USE_OFI=ON                            \
      -DBUILD_DOCUMENTATION=OFF                  \
      -DMERCURY_INSTALL_LIB_DIR=%{_libdir}       \
      -DBUILD_SHARED_LIBS=ON $MERCURY_SRC        \
      ..
make %{?_smp_mflags}


%install
cd build
%make_install

#%if 0%{?suse_version} >= 1315
#%post -n %{suse_libname} -p /sbin/ldconfig
#%postun -n %{suse_libname} -p /sbin/ldconfig
#%else
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
#%endif

%files
%license COPYING
%{_libdir}/*.so.*
%doc

%files devel
%{_includedir}
%{_libdir}/*.so
%{_libdir}/pkgconfig
%{_datadir}/cmake/


%changelog
* Wed Jan 20 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.0.1~rc1-1
- Update to version v2.0.1rc1

* Wed Nov 18 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.0.0-1
- Update to release v2.0.0

* Wed Oct 28 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.0.0~rc3-1
- Update to release v2.0.0rc3

* Mon Oct 12 2020 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.0.0~rc2-1
- Update to release v2.0.0rc2

* Tue Aug 18 2020 Brian J. Murryyell <brian.murrell@intel> - 2.0.0~rc1-2
- Use release tarball and not individual submodule tarballs

* Mon Jul 6 2020 Alexander A Oganezov <alexander.a.oganezov@intel.com> - 2.0.0~rc1-1
- Update to release v2.0.0rc1

* Mon Jun 22 2020 Brian J. Murryyell <brian.murrell@intel> - 2.0.0~a1-2
- Fix License:
- Add %license

* Thu May 07 2020 Brian J. Murrell <brian.murrell@intel> - 2.0.0~a1-1
- Fix pre-release tag in Version:
- Add Requires: libfabric-devel to devel package

* Thu Apr 9 2020 Alexander A Oganezov <alexander.a.oganezov@intel.com> - 2.0.0a1-0.8
- Update to 4871023058887444d47ead4d089c99db979f3d93

* Tue Mar 17 2020 Alexander A Oganezov <alexander.a.oganezov@intel.com> - 2.0.0a1-0.7
- Update to 41caa143a07ed179a3149cac4af0dc7aa3f946fd

* Thu Mar 12 2020 Alexander A Oganezov <alexander.a.oganezov@intel.com> - 2.0.0a1-0.6
- Update to 299b06d47e6c1d59a45985dcbbebe3caca0189d0

* Tue Mar 10 2020 Alexander A Oganezov <alexander.a.oganezov@intel.com> - 2.0.0a1-0.5
- Updated to ad5a3b3dbf171a97e1ca5f1683299db1c69b03ea

* Thu Mar 05 2020 Vikram Chhabra <vikram.chhabra@intel.com> - 2.0.0a1-0.4
- Updated to latest master with HG_Forward fix.

* Tue Feb 11 2020 Yulu Jia <yulu.jia@intel.com> - 2.0.0a1-0.3
- Remove nameserver patch

* Sun Feb 09 2020 Yulu Jia <yulu.jia@intel.com> - 2.0.0a1-0.2
- Update patch to enable ip:port URI format for psm2

* Tue Feb 04 2020 Brian J. Murrell <brian.murrell@intel.com> - 2.0.0a1-0.1
- Update to 2.0.0a1

* Tue Jan 28 2020 Yulu Jia <yulu.jia@intel.com> - 1.0.1-22
- Update to c2c2628
- Apply patch to enable ip:port URI format for psm2

* Mon Dec 2 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-21
- Removed sl_patch on top of 7b529b
- Updated to 9889a0

* Thu Oct 31 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-20
- sl_patch on top of 7b529b

* Wed Oct 23 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-19
- Update to 7b529b

* Tue Oct 22 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-18
- Reverting from 6a8b693 due to mercury segfaults

* Mon Oct 21 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-17
- Update to 6a8b693

* Wed Oct 16 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-16
- Fixed spec to apply patch for 616fee properly

* Tue Oct 15 2019 Alexander Oganezov <alexander.a.oganezov@intel> - 1.0.1-15
- Update to 616fee to get latest changes

* Wed Oct 02 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-14
- Update to cc0807 to include the HG_Cancel() fix.
- Update to f0b9f9 to get latest changes

* Wed Oct 02 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-13
- Once again revert previous update

* Wed Oct 02 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-12
- Update to cc0807 to include the HG_Cancel() fix.
- Update to f0b9f9 to get latest changes

* Wed Sep 25 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-11
- Back out previous update
  - not all consumers are ready for it yet so they need to
    pin their BR

* Fri Sep 20 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-10
- Update to cc0807 to include the HG_Cancel() fix.
- Update to f0b9f9 to get latest changes

* Thu Aug 08 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-9
- Revert previous update

* Fri Aug 02 2019 Yulu Jia <yulu.jia@intel> - 1.0.1-8
- Update to cc0807 to include the HG_Cancel() fix.
- Roll the version number back to 1.0.1

* Fri Aug 02 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-7
- Revert back to the 1.0.1-4 release as the upgrade included
  in -5 (and the subsequent fix in -6) was premature

* Thu Aug 01 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-6
- Roll the version number back to 1.0.1

* Fri Jul 26 2019 Yulu Jia <yulu.jia@intel> - 1.0.1-5
- Update to cc0807 to include the HG_Cancel() fix.

* Thu May 02 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-4
- Devel package needs to require the lib package

* Fri Mar 15 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-2
- Add patch to revert back to Dec 06, 2018 c68870f

* Mon Mar 11 2019 Brian J. Murrell <brian.murrell@intel> - 1.0.1-1
- Update to 1.0.1
- Add patch for "HG Core: fix missing static inline in mercury_core.h"

* Wed Oct 24 2018 Brian J. Murrell <brian.murrell@intel> - 0.9.0-1.git.0f8f25b
- Update mercury to git sha1 0f8f25bb3d57f117979de65cc3c05cf192cf4b31

* Mon Aug 20 2018 Brian J. Murrell <brian.murrell@intel> - 0.9.0-1.git.f7f6955
- Initial package
