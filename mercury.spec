Name: mercury
Version: 2.3.0.1
Release: 2%{?dist}

# dl_version is version with ~ removed
%{lua:
    rpm.define("dl_version " .. string.gsub(rpm.expand("%{version}"), "~", ""))
}

%if 0%{?rhel} > 0
%if 0%{?rhel} > 7
# only RHEL 8+ has a new enough ucx-devel
%global ucx 1
%else
%global ucx 0
%endif
%else
# but assume that anything else does also
%global ucx 1
%endif

# necessary for old cmake environments (e.g., CentOS7)
%{?!cmake_build:%global cmake_build %__cmake --build %{_vpath_srcdir}}
%{?!cmake_install:%global cmake_install %make_install}

Summary:  RPC library for HPC systems
License:  BSD
Group:    Development/Libraries
URL:      http://mercury-hpc.github.io/
Source0:  https://github.com/yuvale2/mercury/archive/refs/tags/v2.3.0.1.tar.gz

BuildRequires:  libfabric-devel >= 1.14.0
BuildRequires:  cmake
BuildRequires:  boost-devel
BuildRequires:  gcc-c++
%if %{ucx}
%if 0%{?suse_version}
BuildRequires: libucp-devel, libucs-devel, libuct-devel
%else
BuildRequires: ucx-devel
%endif
%endif

%description
Mercury is a Remote Procedure Call (RPC) framework specifically
designed for use in High-Performance Computing (HPC) systems with
high-performance fabrics. Its network implementation is abstracted
to make efficient use of native transports and allow easy porting
to a variety of systems. Mercury supports asynchronous transfer of
parameters and execution requests, and has dedicated support for
large data arguments that are transferred using Remote Memory
Access (RMA). Its interface is generic and allows any function
call to be serialized. Since code generation is done using the C
preprocessor, no external tool is required.


%package devel
Summary:  Mercury devel package
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Mercury development headers and libraries.


%if %{ucx}
%package ucx
Summary:  Mercury with UCX
Requires: %{name}%{?_isa} = %{version}-%{release}

%description ucx
Mercury plugin to support the UCX transport.
%endif

%if 0%{?suse_version}
%global __debug_package 1
%global _debuginfo_subpackages 0
%debug_package
%endif

%prep
%autosetup -p1 -n mercury-%dl_version

%build
# Pass -pie linker flags manually on CentOS7 due to CMake PIE issues
# see: https://cmake.org/cmake/help/latest/policy/CMP0083.html#policy:CMP0083
%cmake  -DCMAKE_IN_SOURCE_BUILD:BOOL=ON                   \
        -DCMAKE_BUILD_TYPE:STRING=RelWithDebInfo          \
%if 0%{?rhel} && 0%{?rhel} < 8
        -DCMAKE_EXE_LINKER_FLAGS:STRING="-pie ${LDFLAGS}" \
%endif
        -DCMAKE_SKIP_INSTALL_RPATH:BOOL=ON                \
        -DBUILD_DOCUMENTATION:BOOL=OFF                    \
        -DBUILD_EXAMPLES:BOOL=OFF                         \
        -DBUILD_TESTING:BOOL=ON                           \
        -DBUILD_TESTING_PERF:BOOL=ON                      \
        -DBUILD_TESTING_UNIT:BOOL=OFF                     \
        -DMERCURY_ENABLE_DEBUG:BOOL=ON                    \
        -DMERCURY_INSTALL_DATA_DIR:PATH=%{_libdir}        \
        -DMERCURY_INSTALL_LIB_DIR:PATH=%{_libdir}         \
        -DMERCURY_USE_BOOST_PP:BOOL=ON                    \
        -DMERCURY_USE_CHECKSUMS:BOOL=OFF                  \
        -DMERCURY_USE_SYSTEM_BOOST:BOOL=ON                \
        -DMERCURY_USE_XDR:BOOL=OFF                        \
        -DNA_USE_DYNAMIC_PLUGINS:BOOL=ON                  \
        -DNA_INSTALL_PLUGIN_DIR:PATH=%{_libdir}/mercury   \
        -DNA_USE_SM:BOOL=ON                               \
        -DNA_USE_UCX:BOOL=%{ucx}                          \
        -DNA_USE_OFI:BOOL=ON
%cmake_build

%install
%cmake_install

%if 0%{?suse_version} >= 1315
# only suse needs this; EL bakes it into glibc
%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig
%else
%if 0%{?rhel} < 8
%ldconfig_scriptlets
%endif
%endif

%files
%license LICENSE.txt
%doc Documentation/CHANGES.md
%{_bindir}/hg_*
%{_bindir}/na_*
%{_libdir}/*.so.*
%{_libdir}/mercury/libna_plugin_ofi.so

%if %{ucx}
%files ucx
%{_libdir}/mercury/libna_plugin_ucx.so
%endif

%files devel
%license LICENSE.txt
%doc README.md
%{_includedir}/*
%{_libdir}/libmercury.so
%{_libdir}/libmercury_util.so
%{_libdir}/libna.so
%{_libdir}/pkgconfig/*.pc
%{_libdir}/cmake/

%changelog
* Thu Jun 22 2023 Brian J. Murrell <brian.murrell@intel> - 2.3.0-2
- Rebuild for EL9

* Wed Jun  7 2023 Jerome Soumagne <jerome.soumagne@intel.com> - 2.3.0-1
- Update to 2.3.0
- Add hg_info tool
- Fix pie flags on CentOS7
- Remove na_ucx_src_port.patch and old patches

* Tue Apr 25 2023 Jerome Soumagne <jerome.soumagne@intel.com> - 2.3.0~rc5-1
- Update to 2.3.0rc5
- Remove na_ucx.c patch and add temporary na_ucx_src_port.patch
- Update build to make use of NA dynamic plugins
- Fix source URL and package perf tests

* Thu Dec 22 2022 Joseph Moore <alexander.a.oganezov@intel.com> - 2.2.0-6
- Regenerate packages for LEAP15.4

* Thu Nov 17 2022 Joseph Moore <joseph.moore@intel.com> - 2.2.0-5
- Update na_ucx.c patch to support reconnection following a disconnect.

* Wed Oct 05 2022 Joseph Moore <joseph.moore@intel.com> - 2.2.0-4
- Update na_ucx.c patch to include UCX status to NA error mapping.

* Tue Sep 20 2022 Joseph Moore <joseph.moore@intel.com> - 2.2.0-3
- Fix defect in connect function.

* Fri Sep 09 2022 Joseph Moore <joseph.moore@intel.com> - 2.2.0-2
- Add na_ucx.c patch to change ep creation for single IB device.

* Fri Aug  5 2022 Jerome Soumagne <jerome.soumagne@intel.com> - 2.2.0-1
- Update to 2.2.0

* Mon Aug  1 2022 Jerome Soumagne <jerome.soumagne@intel.com> - 2.2.0~rc6-2
- Rebuild after libfabric rpm dropped CXI compat patch
- Drop CXI compat patch

* Mon Jun 27 2022 Jerome Soumagne <jerome.soumagne@intel.com> - 2.2.0~rc6-1
- Update to 2.2.0rc6
- Skip install rpath, enable debug log.
- Remove openpa dependency.

* Fri Apr 22 2022 Joseph Moore <joseph.moore@intel.com> - 2.1.0~rc4-9
- Change ucx unified mode to off (updated UCX patch file).

* Fri Apr  1 2022 Brian J. Murrell <brian.murrell@intel> - 2.1.0~rc4-8
- Build with ucx subpackage on supported platforms
- Removed invalid build options:
  * MERCURY_ENABLE_VERBOSE_ERROR
  * MERCURY_USE_SELF_FORWARD

* Thu Mar 31 2022 Joseph Moore <joseph.moore@intel.com> - 2.1.0~rc4-7
- Apply daos-9679 address parsing change and active message revision to na_ucx.c.

* Fri Mar 11 2022 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.1.0~rc4-6
- Apply cxi provider patch

* Tue Feb 22 2022 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.1.0~rc4-5
- Apply doas-9561 workaround

* Thu Feb 17 2022 Brian J. Murrell <brian.murrell@intel> - 2.1.0~rc4-4
- Fix issues with %%post* ldconfig
  - No lines are allowed after %%post -p
  - These are not needed on EL8 as it's glibc does the work

* Thu Dec 23 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.1.0~rc4-3
- Remove daos-9173 workaround
- Apply cpu usage fix to mercury

* Tue Dec 7 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.1.0~rc4-2
- Apply DAOS-9173 workaround patch to na_ofi.c

* Tue Nov 30 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.1.0~rc4-1
- Update to version v2.1.0rc4

* Tue Oct 12 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.1.0~rc2-1
- Update to version v2.1.0rc2

* Fri May 14 2021 Alexander Oganezov <alexander.a.oganezov@intel.com> - 2.0.1-1
- Update to version v2.0.1

* Mon May 10 2021 Brian J. Murryyell <brian.murrell@intel> - 2.0.1~rc1-2
- Enable debuginfo package building for SUSE

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
- Add %%license

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
