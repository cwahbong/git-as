PREFIX ?= /usr/local
BINPREFIX ?= "$(PREFIX)/bin"

all:

install:
	install git-as -m 755 $(BINPREFIX)

uninstall:
	rm -f $(BINPREFIX)/git-as
