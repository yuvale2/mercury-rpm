NAME    := mercury
SRC_EXT := bz2
SOURCE   = https://github.com/mercury-hpc/$(NAME)/releases/download/v$(VERSION)/$(NAME)-$(VERSION).tar.$(SRC_EXT)
#PATCH1 is reversed for RPMS.
PATCH1  := https://github.com/mercury-hpc/mercury/compare/c68870ffc0409c29eece5ba036c6efd3c22cee41^...v1.0.1.patch
ID_LIKE1=$(shell . /etc/os-release; echo $$ID_LIKE)
ifeq ($(ID_LIKE1),debian)
# Debian can not use a reverse patch
PATCHES := $(shell rm -rf _topdir/BUILD) 0013-Update-copyright-date.patch \
	0012-Update-README-for-req-gcc-version-w-stdatomic.h.patch \
	0011-Update-CHANGELOG.patch \
	0010-HG-Fix-HG_Reset-to-reset-NA-resources-upon-NA-class-.patch \
	0009-HG-Util-move-inline-functions-for-get-set-and-export.patch \
	0008-Travis-update-build-script-to-OFI-1.7.0.patch \
	0007-Travis-update-build-script-to-OFI-1.7.0rc3.patch \
	0006-NA-SM-remove-page-size-check-that-would-prevent-to-r.patch \
	0005-Update-CMake-policy-for-CMake-3.12-and-above.patch \
	0004-HG-Core-fix-potential-race-when-forcing-a-handle-to-.patch \
	0003-Update-travis-CI-to-use-latest-libfabric-CMake-MPICH.patch \
	0002-NA-OFI-fix-cancelation-of-operations-that-cannot-be-.patch \
	0001-HG-fix-cancelation-of-HG-operations-fix-267.patch
else
PATCHES := c68870ffc0409c29eece5ba036c6efd3c22cee41^...v1.0.1.patch
endif

c68870ffc0409c29eece5ba036c6efd3c22cee41^...v1.0.1.patch:
	curl -f -L -O '$(PATCH1)'

include Makefile_packaging.mk
