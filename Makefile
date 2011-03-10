# Makefile

SHELL := sh -e

SCRIPTS =	"debian/preinst install" \
		"debian/postinst configure" \
		"debian/prerm remove" \
		"debian/postrm remove" \
		"scripts/canaima-semilla.sh" \
		"scripts/funciones-semilla.sh" \
		"scripts/manual-canaima-semilla.sh"

all: build

test:

	@echo -n "\n===== Comprobando posibles errores de sintaxis en los scripts de mantenedor =====\n"

	@for SCRIPT in $(SCRIPTS); \
	do \
		echo -n "$${SCRIPT}\n"; \
		bash -n $${SCRIPT}; \
	done

	@echo -n "¡TODO BIEN!\n=================================================================================\n\n"

build:
	$(MAKE) clean

	# Generar la documentación con python-sphinx
	rst2man --language="es" --title="CANAIMA SEMILLA" documentos/man-canaima-semilla.rst documentos/canaima-semilla.1
	$(MAKE) -C documentos latex
	$(MAKE) -C documentos html
	$(MAKE) -C documentos/_build/latex all-pdf

	$(MAKE) test

install:

	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/canaima-semilla/semillero/
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp -r desktop/manual-canaima-semilla.desktop $(DESTDIR)/usr/share/applications/
	cp -r scripts/canaima-semilla.sh $(DESTDIR)/usr/bin/canaima-semilla
	ln -s /usr/bin/canaima-semilla $(DESTDIR)/usr/bin/c-s
	cp -r scripts/manual-canaima-semilla.sh $(DESTDIR)/usr/bin/manual-canaima-semilla
	cp -r scripts perfiles $(DESTDIR)/usr/share/canaima-semilla/
	cp -r conf/variables.conf $(DESTDIR)/usr/share/canaima-semilla/

uninstall:

	rm -rf $(DESTDIR)/usr/share/canaima-semilla
	rm -rf $(DESTDIR)/usr/bin/canaima-semilla
	rm -rf $(DESTDIR)/usr/bin/c-s
	rm -rf $(DESTDIR)/usr/bin/manual-semilla
	rm -rf $(DESTDIR)/etc/skel/.config/canaima-semilla/
	rm -rf $(DESTDIR)/usr/share/applications/manual-semilla.desktop

clean:

	rm -rf documentos/_build/*
	rm -rf documentos/canaima-semilla.1

distclean:

reinstall: uninstall install
