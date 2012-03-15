# Makefile

SHELL := sh -e

SCRIPTS = "debian/preinst install" "debian/postinst configure" "debian/prerm remove" "debian/postrm remove"

all: test build

test:

	@echo -n "\n===== Comprobando posibles errores de sintaxis en los scripts de mantenedor =====\n"

	@for SCRIPT in $(SCRIPTS); \
	do \
		echo -n "$${SCRIPT}\n"; \
		bash -n $${SCRIPT}; \
	done

	@echo -n "¡TODO BIEN!\n=================================================================================\n\n"


build:
	@echo "Nada para compilar!"


install:
	# Installing shared data
	mkdir -p $(DESTDIR)/usr/share/canaima-semilla-gui/
	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/share/icons/canaima-iconos/apps/48
	mkdir -p $(DESTDIR)/usr/share/applications/
	mkdir -p $(DESTDIR)/usr/share/gnome/help

	cp -r scripts $(DESTDIR)/usr/share/canaima-semilla-gui
	cp -r images $(DESTDIR)/usr/share/canaima-semilla-gui/
	cp -r images/c-s.png $(DESTDIR)/usr/share/icons/canaima-iconos/apps/48
	cp -r desktop/canaima-semilla-gui.desktop $(DESTDIR)/usr/share/applications
	cp -r scripts/canaima-semilla-gui $(DESTDIR)/usr/bin/
	cp -r ayuda/canaima-semilla-gui $(DESTDIR)/usr/share/gnome/help

uninstall:
	# Uninstalling shared data
	rm -rf $(DESTDIR)/usr/share/canaima-semilla-gui/
	rm -rf $(DESTDIR)/usr/share/applications/canaima-semilla-gui.desktop
	rm -rf $(DESTDIR)/usr/share/gnome/help/canaima-semilla-gui
	rm -rf $(DESTDIR)/usr/share/icons/canaima-iconos/apps/48/c-s.png
	
	# Uninstalling executables
	rm -rf $(DESTDIR)/usr/bin/canaima-semilla-gui
	
clean:

distclean:

reinstall: uninstall install
