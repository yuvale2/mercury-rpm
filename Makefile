NAME    := mercury
SRC_EXT := bz2
SOURCE   = https://github.com/mercury-hpc/$(NAME)/releases/download/v$(VERSION)/$(NAME)-$(VERSION).tar.$(SRC_EXT)
PATCHES := v1.0.1...cc0807e8377e129945834d292be21a6667a8cbb3.patch                                   \
	       cc0807e8377e129945834d292be21a6667a8cbb3...f0b9f992793be46f1c6ae47b30d1c3ccb525cfbf.patch \
	       f0b9f992793be46f1c6ae47b30d1c3ccb525cfbf...616fee16a3c09eb93d804b627e64ea1c84c6b4d4.patch \
	       616fee16a3c09eb93d804b627e64ea1c84c6b4d4...7b529b63e4003fb15ebdbf2dfdf29ab2a3d3c132.patch

LEAP_42_REPOS = $(OPENSUSE_REPOS_MIRROR)/repositories/science:/HPC/openSUSE_Leap_42.3/
SLES_12_REPOS = $(OPENSUSE_REPOS_MIRROR)/repositories/science:/HPC/openSUSE_Leap_42.3/
SLES_15_REPOS = $(OPENSUSE_REPOS_MIRROR)/repositories/science:/HPC/openSUSE_Leap_15.1/

include packaging/Makefile_packaging.mk
