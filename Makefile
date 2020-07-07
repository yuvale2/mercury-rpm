NAME       := mercury
SRC_EXT    := gz
DL_VERSION := 2.0.0rc1

SLES_15_REPOS = $(OPENSUSE_REPOS_MIRROR)/repositories/science:/HPC/openSUSE_Leap_15.1/

include packaging/Makefile_packaging.mk

9da3e5b.tar.gz:
	rm -f ./$@
	curl -f -L -O 'https://github.com/mercury-hpc/kwsys/archive/$@'

3c76b32.tar.gz:
	rm -f ./$@
	curl -f -L -O 'https://github.com/mercury-hpc/mchecksum/archive/$@'

749783c.tar.gz:
	rm -f ./$@
	curl -f -L -O 'https://github.com/mercury-hpc/preprocessor/archive/$@'
