NAME       := mercury
SRC_EXT    := bz2

SLES_15_REPOS = $(OPENSUSE_REPOS_MIRROR)/repositories/science:/HPC/openSUSE_Leap_15.1/

include packaging/Makefile_packaging.mk
