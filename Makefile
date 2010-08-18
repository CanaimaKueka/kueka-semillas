# Makefile

SHELL := sh -e

LANGUAGES = es

SCRIPTS = functions/* scripts/*.sh scripts/*/*

all: test build

test:
	@echo -n "Comprobando posibles errores de sintaxis..."

	@for SCRIPT in $(SCRIPTS); \
	do \
		sh -n $${SCRIPT}; \
		echo -n "."; \
	done

	@echo "Hecho!"

	@echo -n "Iniciando bashisms..."

	@if [ -x /usr/bin/checkbashisms ]; \
	then \
		for SCRIPT in $(SCRIPTS); \
		do \
			checkbashisms -f -x $${SCRIPT} || true; \
			echo -n "."; \
		done; \
	else \
		echo "ADVERTENCIA: Obviando bashisms - Necesitas instalar el paquete devscripts"; \
	fi

	@echo " Hecho!"

build:
	@echo "Nada para compilar!"

install:
	# Installing shared data
	mkdir -p $(DESTDIR)/usr/share/canaima-semilla
	cp -r data functions scripts hooks includes lists repositories templates $(DESTDIR)/usr/share/canaima-semilla

	# Installing executables
	mkdir -p $(DESTDIR)/usr/bin
	mv $(DESTDIR)/usr/share/canaima-semilla/scripts/build/canaima-semilla $(DESTDIR)/usr/bin

	# Installing documentation
	mkdir -p $(DESTDIR)/usr/share/doc/canaima-semilla
	cp -r COPYING docs/* $(DESTDIR)/usr/share/doc/canaima-semilla

	# Installing manpages
	for MANPAGE in manpages/es/*; \
	do \
		SECTION="$$(basename $${MANPAGE} | awk -F. '{ print $$2 }')"; \
		install -D -m 0644 $${MANPAGE} $(DESTDIR)/usr/share/man/man$${SECTION}/$$(basename $${MANPAGE}); \
	done

	for LANGUAGE in $(LANGUAGES); \
	do \
		for MANPAGE in manpages/$${LANGUAGE}/*; \
		do \
			SECTION="$$(basename $${MANPAGE} | awk -F. '{ print $$3 }')"; \
			install -D -m 0644 $${MANPAGE} $(DESTDIR)/usr/share/man/$${LANGUAGE}/man$${SECTION}/$$(basename $${MANPAGE} .$${LANGUAGE}.$${SECTION}).$${SECTION}; \
		done; \
	done

	# Installing logfile
	mkdir -p $(DESTDIR)/var/log

uninstall:
	# Uninstalling shared data
	rm -rf $(DESTDIR)/usr/share/canaima-semilla
	rmdir --ignore-fail-on-non-empty $(DESTDIR)/usr/share/canaima-semilla

	# Uninstalling executables
	rm -f $(DESTDIR)/usr/bin/canaima-semilla

	# Uninstalling documentation
	rm -rf $(DESTDIR)/usr/share/doc/canaima-semilla

	# Uninstalling manpages
	for MANPAGE in manpages/es/*; \
	do \
		SECTION="$$(basename $${MANPAGE} | awk -F. '{ print $$2 }')"; \
		rm -f $(DESTDIR)/usr/share/man/man$${SECTION}/$$(basename $${MANPAGE} .en.$${SECTION}).$${SECTION}; \
	done

	for LANGUAGE in $(LANGUAGES); \
	do \
		for MANPAGE in manpages/$${LANGUAGE}/*; \
		do \
			SECTION="$$(basename $${MANPAGE} | awk -F. '{ print $$3 }')"; \
			rm -f $(DESTDIR)/usr/share/man/$${LANGUAGE}/man$${SECTION}/$$(basename $${MANPAGE} .$${LANGUAGE}.$${SECTION}).$${SECTION}; \
		done; \
	done

clean:

distclean:

reinstall: uninstall install