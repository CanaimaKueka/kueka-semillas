#!/bin/bash

# Disable Lock Screen
gsettings set org.gnome.desktop.lockdown disable-lock-screen true >> .disabler

# Disable automount for Canaima Instalador
gsettings set org.gnome.desktop.media-handling automount false >> .disabler
gsettings set org.gnome.desktop.media-handling automount-open false >> .disabler
gsettings set org.gnome.desktop.media-handling autorun-never true >> .disabler
