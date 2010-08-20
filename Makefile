# Makefile

SHELL := sh -e

SCRIPTS = functions/* scripts/*.sh scripts/*/*

all: test build

test:
	@echo -n "Comprobando posibles errores de sintaxis"

	@for SCRIPT in $(SCRIPTS); \
	do \
		sh -n $${SCRIPT}; \
		echo -n "."; \
	done

	@echo "\nHecho!"

	@echo -n "Iniciando bashisms"

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

	@echo "\nHecho!"

build:
	@echo "Nada para compilar!"

install:
	# Installing shared data
	mkdir -p $(DESTDIR)/usr/share/canaima-semilla/
	cp -r data functions scripts hooks includes lists repositories templates $(DESTDIR)/usr/share/canaima-semilla/

	# Installing executables
	mkdir -p $(DESTDIR)/usr/bin/
	cp $(DESTDIR)/usr/share/canaima-semilla/scripts/build/canaima-semilla $(DESTDIR)/usr/bin/

	# Installing documentation
	mkdir -p $(DESTDIR)/usr/share/doc/canaima-semilla
	cp AUTHORS CREDITS README $(DESTDIR)/usr/share/doc/canaima-semilla/

	# Installing manpages
	for MANPAGE in manuales/*; \
	do \
		SECTION="$$(basename $${MANPAGE} | awk -F. '{ print $$2 }')"; \
		install -D -m 0644 $${MANPAGE} $(DESTDIR)/usr/share/man/man$${SECTION}/$$(basename $${MANPAGE}); \
	done

uninstall:
	# Uninstalling shared data
	rm -rf $(DESTDIR)/usr/share/canaima-semilla/
	
	# Uninstalling executables
	rm -f $(DESTDIR)/usr/bin/canaima-semilla

	# Uninstalling documentation
	rm -rf $(DESTDIR)/usr/share/doc/canaima-semilla/

	# Uninstalling manpages
	for MANPAGE in manuales/*; \
	do \
		SECTION="$$(basename $${MANPAGE} | awk -F. '{ print $$2 }')"; \
		rm -f $(DESTDIR)/usr/share/man/man$${SECTION}/$$(basename $${MANPAGE} .en.$${SECTION}).$${SECTION}; \
	done

clean:

distclean:

reinstall: uninstall install
