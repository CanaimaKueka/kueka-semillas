# Makefile

SHELL = sh -e

# Datos del Proyecto
AUTHOR = Luis Alejandro Martínez Faneyth
EMAIL = luis@huntingbears.com.ve
MAILIST = desarrolladores@canaima.softwarelibre.gob.ve
PACKAGE = CanaimaSemilla
CHARSET = UTF-8
VERSION = $(shell cat VERSION | grep "VERSION" | sed 's/VERSION = //g;s/+.*//g')
YEAR = $(shell date +%Y)

# Datos de traducción
LANGTEAM = Equipo de Traducción de Canaima Semilla <desarrolladores@canaima.softwarelibre.gob.ve>
POTLIST = locale/pot/canaima-semilla/POTFILES.in
POTFILE = locale/pot/canaima-semilla/messages.pot
POTITLE = Plantilla de Traducción para Canaima Semilla
POTEAM = Equipo de Traducción de Canaima Semilla
PODATE = $(shell date +%F\ %R%z)

# Listas de Archivos
SCRIPTS = $(shell find ./scripts -type f -iname "*.sh")
IMAGES = $(shell ls documentation/rest/images/ | grep "\.svg" | sed 's/\.svg//g')
LOCALES = $(shell find locale -mindepth 1 -maxdepth 1 -type d | sed 's|locale/pot||g;s|locale/||g')

# Dependencias de Construcción
# Tareas de Construcción
# gen-img: genera imágenes png a partir de svg. Usa CONVERT, LIBSVG e ICOTOOL.
# gen-mo: genera archivos mo a partir de archivos po. Usa MSGFMT.
# gen-doc: construye toda la documentación
#       - gen-man: genera una página de manual (man). Usa RST2MAN.
#       - gen-wiki: genera código wiki para github y googlecode a partir de fuentes rest. Usa PYTHON.
#       - gen-html: genera el manual HTML a partir de las fuentes rest. Usa SPHINX.
PYTHON = $(shell which python)
SHELLBIN = $(shell which sh)
RST2MAN = $(shell which rst2man)
SPHINX = $(shell which sphinx-build)
MSGFMT = $(shell which msgfmt)
CONVERT = $(shell which convert)
ICOTOOL = $(shell which icotool)
LIBSVG = $(shell find /usr/lib/ -maxdepth 1 -type d -iname "imagemagick-*")/modules-Q16/coders/svg.so

# Dependencias de Instalación
# Tareas de Instalación
# install: instala canaima-semilla. Necesita LIVEBUILD.
LIVEBUILD = $(shell which live-build)

# Dependencias de tareas de mantenimiento
# generatepot: generates POT template from php sources. Uses XGETTEXT.
# updatepos: updates PO files from POT files. Uses MSGMERGE.
# snapshot: makes a new development snapshot. Uses SHELLBIN and GIT.
# release: makes a new release. Uses SHELLBIN, GIT, PYTHON, MD5SUM, TAR and GBP.
PYTHON = $(shell which python)
SHELLBIN = $(shell which sh)
GIT = $(shell which git)
MSGMERGE = $(shell which msgmerge)
XGETTEXT = $(shell which xgettext)
DEVSCRIPTS = $(shell which debuild)
DPKGDEV = $(shell which dpkg-buildpackage)
DEBHELPER = $(shell which dh)
GBP = $(shell which git-buildpackage)
LINTIAN = $(shell which lintian)
GNUPG = $(shell which gpg)
MD5SUM = $(shell which md5sum)
TAR = $(shell which tar)
TRANSIFEX = $(shell which tx)
BASHISMS = $(shell which checkbashisms)

all: build

build: gen-img gen-mo gen-doc

gen-doc: gen-wiki gen-html gen-man

gen-predoc: clean-predoc

	@echo "Preprocesando documentación ..."
	@$(SHELLBIN) tools/predoc.sh build

gen-wiki: check-buildep gen-img gen-predoc clean-wiki

	@echo "Generando documentación desde las fuentes [RST > WIKI]"
	@cp documentation/githubwiki.index documentation/rest/Home.md
	@cp documentation/rest/*.md documentation/rest/*.rest documentation/githubwiki/
	@rm -rf documentation/rest/Home.md
	@cp documentation/googlewiki.index documentation/rest/index.rest
	@echo "" >> documentation/rest/index.rest
	@cat documentation/rest/contents.rest >> documentation/rest/index.rest
	@mv documentation/rest/contents.rest documentation/rest/contents.tmp
	@$(PYTHON) -B tools/googlecode-wiki.py
	@mv documentation/rest/contents.tmp documentation/rest/contents.rest
	@rm -rf documentation/rest/index.rest

gen-html: check-buildep gen-img gen-predoc clean-html

	@echo "Generando documentación desde las fuentes [RST > HTML]"
	@cp documentation/sphinx.index documentation/rest/index.rest
	@$(SPHINX) -E -Q -b html -d documentation/html/doctrees documentation/rest documentation/html
	@rm -rf documentation/rest/index.rest documentation/html/doctrees documentation/html/objects.inv

gen-man: check-buildep gen-predoc clean-man

	@echo "Generando documentación desde las fuentes [RST > MAN]"
	@$(RST2MAN) --language="es" --title="CANAIMA SEMILLA" documentation/man/canaima-semilla.rest documentation/man/canaima-semilla.1

gen-img: check-buildep clean-img

	@printf "Generando imágenes desde las fuentes [SVG > JPG,ICO] ["
	@for IMAGE in $(IMAGES); do \
		$(CONVERT) -background None documentation/rest/images/$${IMAGE}.svg \
			documentation/rest/images/$${IMAGE}.png; \
		$(CONVERT) -background None documentation/rest/images/$${IMAGE}.png \
			documentation/rest/images/$${IMAGE}.jpg; \
		printf "."; \
	done;
	@$(ICOTOOL) -c -o documentation/rest/images/favicon.ico \
		documentation/rest/images/favicon.png
	@printf "]\n"

gen-mo: check-buildep clean-mo

	@printf "Generando mensajes de traducción desde las fuentes [PO > MO] ["
	@for LOCALE in $(LOCALES); do \
		$(MSGFMT) locale/$${LOCALE}/LC_MESSAGES/messages.po \
			-o locale/$${LOCALE}/LC_MESSAGES/messages.mo; \
		printf "."; \
	done
	@printf "]\n"

# INSTALL TASKS ------------------------------------------------------------------------------

install:

	mkdir -p $(DESTDIR)/usr/bin/
	mkdir -p $(DESTDIR)/usr/lib/canaima-semilla/
	mkdir -p $(DESTDIR)/usr/share/canaima-semilla/semillero/
	mkdir -p $(DESTDIR)/usr/share/canaima-semilla/scripts/
	mkdir -p $(DESTDIR)/usr/share/applications/
	cp -r desktop/manual-canaima-semilla.desktop $(DESTDIR)/usr/share/applications/
	cp -r scripts/canaima-semilla.sh $(DESTDIR)/usr/bin/canaima-semilla
	ln -s /usr/bin/canaima-semilla $(DESTDIR)/usr/bin/c-s
	cp -r scripts/manual-canaima-semilla.sh $(DESTDIR)/usr/bin/manual-canaima-semilla
	cp -r scripts/funciones-semilla.sh $(DESTDIR)/usr/share/canaima-semilla/scripts/
	cp -r scripts/canaima-semilla-construir.sh $(DESTDIR)/usr/share/canaima-semilla/scripts/
	cp -r perfiles $(DESTDIR)/usr/share/canaima-semilla/
	cp -r conf/variables.conf $(DESTDIR)/usr/share/canaima-semilla/

uninstall:

	rm -rf $(DESTDIR)/usr/share/canaima-semilla
	rm -rf $(DESTDIR)/usr/bin/canaima-semilla
	rm -rf $(DESTDIR)/usr/bin/c-s
	rm -rf $(DESTDIR)/usr/bin/manual-semilla
	rm -rf $(DESTDIR)/etc/skel/.config/canaima-semilla/
	rm -rf $(DESTDIR)/usr/share/applications/manual-semilla.desktop

# MAINTAINER TASKS ---------------------------------------------------------------------------------

prepare: check-maintdep

	@git submodule init
	@git submodule update
	@cd documentation/githubwiki/ && git checkout development && git pull origin development
	@cd documentation/googlewiki/ && git checkout development && git pull origin development

pull-po: check-maintdep

	@tx pull -a

push-po: check-maintdep

	@tx push --source --translations

gen-po: check-maintdep gen-pot

	@echo "Actualizando archivos de traducción desde plantilla ["
	@for LOCALE in $(LOCALES); do \
		$(MSGMERGE) --no-wrap -s -U locale/$${LOCALE}/LC_MESSAGES/messages.po $(POTFILE); \
		sed -i -e ':a;N;$$!ba;s|#, fuzzy\n||g' locale/$${LOCALE}/LC_MESSAGES/messages.po; \
		rm -rf locale/$${LOCALE}/LC_MESSAGES/messages.po~; \
	done
	@echo "]"

gen-pot: check-maintdep

	@echo "Actualizando plantilla de traducción ..."
	@rm $(POTLIST)
	@for FILE in $(SCRIPTS); do \
		echo "../../.$${FILE}" >> $(POTLIST); \
	done
	@cd locale/pot/canaima-semilla/ && $(XGETTEXT) --msgid-bugs-address="$(MAILIST)" \
		--package-version="$(VERSION)" --package-name="$(PACKAGE)" \
		--copyright-holder="$(AUTHOR)" --no-wrap --from-code=utf-8 \
		--language=Shell -kERROR -kADVERTENCIA -kEXITO -s -j -o messages.pot -f POTFILES.in
	@sed -i -e 's/# SOME DESCRIPTIVE TITLE./# $(POTITLE)./' \
		-e 's/# Copyright (C) YEAR Luis Alejandro Martínez Faneyth/# Copyright (C) $(YEAR) $(AUTHOR)/' \
		-e 's/same license as the PACKAGE package./same license as the $(PACKAGE) package./' \
		-e 's/# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR./#\n# Translators:\n# $(AUTHOR) <$(EMAIL)>, $(YEAR)/' \
		-e 's/"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"/"PO-Revision-Date: $(PODATE)\\n"/' \
		-e 's/"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"/"Last-Translator: $(AUTHOR) <$(EMAIL)>\\n"/' \
		-e 's/"Language-Team: LANGUAGE <LL@li.org>\\n"/"Language-Team: $(POTEAM) <$(MAILIST)>\\n"/' \
		-e 's/"Language: \\n"/"Language: English\\n"/g' $(POTFILE)
	@sed -i -e ':a;N;$$!ba;s|#, fuzzy\n||g' $(POTFILE)

gen-test:

	@printf "Buscando errores de sintaxis en shell scripts ["
	@for SCRIPT in $(SCRIPTS); \
	do \
		printf "." \
		$(SHELLBIN) -n $${SCRIPT}; \
		$(BASHISMS) -f -x $${SCRIPT} || true; \
	done
	@printf "]\n"

snapshot: check-maintdep prepare gen-html gen-wiki gen-po clean

	@$(MAKE) clean
	@$(SHELLBIN) tools/snapshot.sh

release: check-maintdep

	@$(SHELLBIN) tools/release.sh

deb-test-snapshot: check-maintdep

	@$(SHELLBIN) tools/buildpackage.sh test-snapshot

deb-test-release: check-maintdep

	@$(SHELLBIN) tools/buildpackage.sh test-release

deb-final-release: check-maintdep

	@$(SHELLBIN) tools/buildpackage.sh final-release

# CLEAN TASKS ------------------------------------------------------------------------------

clean: clean-img clean-mo clean-man clean-predoc

clean-all: clean-img clean-mo clean-html clean-wiki clean-man clean-predoc

clean-predoc:

	@echo "Cleaning preprocessed documentation files ..."
	@$(SHELLBIN) tools/predoc.sh clean
	@rm -rf documentation/rest/index.rest

clean-img:

	@printf "Cleaning generated images [JPG,ICO] ["
	@for IMAGE in $(IMAGES); do \
		rm -rf documentation/rest/images/$${IMAGE}.jpg; \
		rm -rf documentation/rest/images/$${IMAGE}.png; \
		printf "."; \
	done
	@rm -rf documentation/rest/images/favicon.ico
	@printf "]\n"

clean-mo:

	@printf "Cleaning generated localization ["
	@for LOCALE in $(LOCALES); do \
		rm -rf locale/$${LOCALE}/LC_MESSAGES/messages.mo; \
		printf "."; \
	done
	@printf "]\n"

clean-html:

	@echo "Cleaning generated html ..."
	@rm -rf documentation/html/*
	@rm -rf documentation/html/.buildinfo

clean-wiki:

	@echo "Cleaning generated wiki pages ..."
	@rm -rf documentation/googlewiki/*
	@rm -rf documentation/githubwiki/*

clean-man:

	@echo "Cleaning generated man pages ..."
	@rm -rf documentation/man/canaima-semilla.1

# CHECK DEPENDENCIES ---------------------------------------------------------------------------------------------

check-instdep:

	@printf "Checking if we have Live Build ... "
	@if [ -z $(LIVEBUILD) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"live-build\" package."; \
		exit 1; \
	fi
	@echo

check-maintdep:

	@printf "Checking if we have python ... "
	@if [ -z $(PYTHON) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have a shell ... "
	@if [ -z $(SHELLBIN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"bash\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have git... "
	@if [ -z $(GIT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"git-core\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have xgettext ... "
	@if [ -z $(XGETTEXT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gettext\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have msgmerge ... "
	@if [ -z $(MSGMERGE) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gettext\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have debhelper ... "
	@if [ -z $(DEBHELPER) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"debhelper\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have devscripts ... "
	@if [ -z $(DEVSCRIPTS) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"devscripts\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have dpkg-dev ... "
	@if [ -z $(DPKGDEV) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"dpkg-dev\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have git-buildpackage ... "
	@if [ -z $(GBP) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"git-buildpackage\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have lintian ... "
	@if [ -z $(LINTIAN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"lintian\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have gnupg ... "
	@if [ -z $(GNUPG) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gnupg\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have md5sum ... "
	@if [ -z $(MD5SUM) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"coreutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have tar ... "
	@if [ -z $(TAR) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"tar\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have tx ... "
	@if [ -z $(TRANSIFEX) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"transifex-client\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have checkbashisms ... "
	@if [ -z $(BASHISMS) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"devscripts\" package."; \
		exit 1; \
	fi
	@echo

check-buildep:

	@printf "Checking if we have python ... "
	@if [ -z $(PYTHON) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have a shell... "
	@if [ -z $(SHELLBIN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"bash\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have sphinx-build ... "
	@if [ -z $(SPHINX) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python-sphinx\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have convert ... "
	@if [ -z $(CONVERT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"imagemagick\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have rst2man ... "
	@if [ -z $(RST2MAN) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"python-docutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have msgfmt ... "
	@if [ -z $(MSGFMT) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"gettext\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have icotool ... "
	@if [ -z $(ICOTOOL) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"icoutils\" package."; \
		exit 1; \
	fi
	@echo

	@printf "Checking if we have imagemagick svg support ... "
	@if [ -z $(LIBSVG) ]; then \
		echo "[ABSENT]"; \
		echo "If you are using Debian, Ubuntu or Canaima, please install the \"libmagickcore-extra\" package."; \
		exit 1; \
	fi
	@echo
