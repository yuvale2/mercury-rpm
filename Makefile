NAME        := mercury
VERSION     := 0.9.0
RELEASE     := 1.git.0f8f25b
DIST        := $(shell rpm --eval %{dist})
SRPM        := _topdir/SRPMS/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).src.rpm
RPMS        := _topdir/RPMS/x86_64/$(NAME)-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm           \
	       _topdir/RPMS/x86_64/$(NAME)-devel-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm     \
	       _topdir/RPMS/x86_64/$(NAME)-debuginfo-$(VERSION)-$(RELEASE)$(DIST).x86_64.rpm
SPEC        := $(NAME).spec
SRC_EXT     := gz
#SOURCE1     := $(NAME)-$(VERSION).tar.$(SRC_EXT)
#SOURCE1_URL := https://github.com/mercury-hpc/mercury/releases/download/v$(VERSION)/$(SOURCE)
#PATCH1      := v0.9.0..f7f6955.patch
#SOURCES     := _topdir/SOURCES/$(SOURCE) _topdir/SOURCES/$(PATCH1)
shortcommit0 := 0f8f25b
shortcommit1 := 9da3e5b
shortcommit2 := 749783c
shortcommit3 := 5092f6b
SOURCE0      := $(shortcommit0).tar.$(SRC_EXT)
SOURCE0_URL  := https://github.com/mercury-hpc/mercury/archive/$(SOURCE0)
SOURCE1      := $(shortcommit1).tar.$(SRC_EXT)
SOURCE1_URL  := https://github.com/mercury-hpc/kwsys/archive/$(SOURCE1)
SOURCE2      := $(shortcommit2).tar.$(SRC_EXT)
SOURCE2_URL  := https://github.com/mercury-hpc/preprocessor/archive/$(SOURCE2)
SOURCE3      := $(shortcommit3).tar.$(SRC_EXT)
SOURCE3_URL  := https://github.com/mercury-hpc/mchecksum/archive/$(SOURCE3)
SOURCES      := _topdir/SOURCES/$(SOURCE0) _topdir/SOURCES/$(SOURCE1) \
	        _topdir/SOURCES/$(SOURCE2) _topdir/SOURCES/$(SOURCE3)
TARGETS      := $(RPMS) $(SRPM)

all: $(TARGETS)

%/:
	mkdir -p $@

_topdir/SOURCES/%: % | _topdir/SOURCES/
	ln $< $@

$(shortcommit0).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE0_URL)'

$(shortcommit1).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE1_URL)'

$(shortcommit2).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE2_URL)'

$(shortcommit3).tar.$(SRC_EXT):
	curl -f -L -O '$(SOURCE3_URL)'

# see https://stackoverflow.com/questions/2973445/ for why we subst
# the "rpm" for "%" to effectively turn this into a multiple matching
# target pattern rule
$(subst rpm,%,$(RPMS)): $(SPEC) $(SOURCES)
	rpmbuild -bb --define "%_topdir $$PWD/_topdir" $(SPEC)

$(SRPM): $(SPEC) $(SOURCES)
	rpmbuild -bs --define "%_topdir $$PWD/_topdir" $(SPEC)

srpm: $(SRPM)

rpms: $(RPMS)

ls: $(TARGETS)
	ls -ld $^

mockbuild: $(SRPM)
	mock $<

rpmlint: $(SPEC)
	rpmlint $<
