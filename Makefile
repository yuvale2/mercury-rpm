NAME    := mercury
SRC_EXT := bz2
SOURCE   = https://github.com/mercury-hpc/$(NAME)/releases/download/v$(VERSION)/$(NAME)-$(VERSION).tar.$(SRC_EXT)
PATCHES := v1.0.1...cc0807e8377e129945834d292be21a6667a8cbb3.patch

include Makefile_packaging.mk
