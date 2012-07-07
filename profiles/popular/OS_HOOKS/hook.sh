#!/bin/bash -e

BORRAR_LENGUAJES="af am an ang ar ara as ast az az_IR bal be be@latin bem bg bn bn_IN br bs byn ca ca@valencia ckb co crh cs csb currency cy da de de_AT dv dz el en_AU en@boldquot en_CA en_GB en_NZ en@quot en@shaw en_US@piglatin eo es_CL es_CO es_CR es_DO es_EC es_GT es_HN es_MX es_NI es_PA es_PE es_PR es_SV es_UY et et_EE eu fa fi fil fo fr frp fur fy ga gez gl gn gu gv ha haw he he_IL hi hr hu hy ia id ig io is it it_IT ja jv ka kk km kn ko kok ks ku ky l10n la lb lg li lo lt lv mai mg mi mk ml mn mr ms ms_MY mt my my_MM nb nb_NO nds ne nl nn no nso oc or pa pl ps  pt_PT qu rm ro ru ru_RU rw sc si sk sl so sq sr sr@ije sr@latin sr@Latn sv sw ta te tet tg th ti tig tk tl tr tr_TR tt ug uk uk_UA ur urd ur_PK uz uz@cyrillic ve vi wa wal wo xh yi yo zh zh_CN zh_HK zh_TW zu"

apt-get clean
apt-get autoclean

[ -e /var/cache/apt/pkgcache.bin ] && rm -rf /var/cache/apt/pkgcache.bin
[ -e /var/cache/apt/srcpkgcache.bin ] && rm -rf /var/cache/apt/srcpkgcache.bin

rm -rf /var/lib/apt/lists/repositorio*
rm -rf /var/lib/apt/lists/seguridad*
rm -rf /var/lib/apt/lists/universo*

for lenguaje in ${BORRAR_LENGUAJES}; do
	rm -rf /usr/share/locale/${lenguaje}
done




