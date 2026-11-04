#!/bin/sh
# Build the .ipk package: ./build.sh
set -e
cd "$(dirname "$0")"
VERSION=$(sed -n 's/^VERSION = "\(.*\)"/\1/p' src/SimpleSwapManager/plugin.py)
PKG=enigma2-plugin-systemplugins-simpleswapmanager
BUILD=$(mktemp -d)
trap 'rm -rf "$BUILD"' EXIT
DEST="$BUILD/data/usr/lib/enigma2/python/Plugins/SystemPlugins/SimpleSwapManager"
mkdir -p "$DEST" "$BUILD/control" dist

cp src/SimpleSwapManager/*.py src/SimpleSwapManager/plugin.png "$DEST/"
for po in po/*.po; do
	lang=$(basename "$po" .po)
	mkdir -p "$DEST/locale/$lang/LC_MESSAGES"
	msgfmt -o "$DEST/locale/$lang/LC_MESSAGES/SimpleSwapManager.mo" "$po"
done

sed "s/@VERSION@/$VERSION/" CONTROL/control > "$BUILD/control/control"
# package scripts: insert the shared part (texts, output helpers) at "# @COMMON@"
for s in preinst postinst prerm postrm; do
	cat CONTROL/i18n/*.sh CONTROL/common.sh > "$BUILD/common.sh"
	awk -v common="$BUILD/common.sh" '
		/^# @COMMON@$/ { while ((getline line < common) > 0) print line; next }
		{ print }' "CONTROL/$s" | sed "s/@VERSION@/$VERSION/g" > "$BUILD/control/$s"
	chmod 755 "$BUILD/control/$s"
	sh -n "$BUILD/control/$s"
done

echo "2.0" > "$BUILD/debian-binary"
( cd "$BUILD/data" && tar --owner=0 --group=0 --mode="u+rwX,go+rX,go-w" -czf ../data.tar.gz . )

# ar archive: debian-binary, control.tar.gz, data.tar.gz - in exactly this order
pack() {  # <output file>
	rm -f "$1"
	( cd "$BUILD" && tar --owner=0 --group=0 -C control -czf control.tar.gz . \
		&& ar -r "$OLDPWD/$1" debian-binary control.tar.gz data.tar.gz 2>/dev/null )
	echo "Built $1"
}

# .ipk - openATV, OpenPLi, OpenViX, OpenBH, Egami, VTi, ... (opkg)
pack "dist/${PKG}_${VERSION}_all.ipk"

# .deb - DreamOS (Dreambox DM900/DM920/One/Two, dpkg/apt). EXPERIMENTAL, untested.
# dpkg verifies installed files with md5sums, opkg does not need them.
( cd "$BUILD/data" && find . -type f | sed 's|^\./||' | sort | xargs md5sum ) > "$BUILD/control/md5sums"
sed -i 's/^Description: \(.*\)$/Description: \1 (experimental DreamOS build)/' "$BUILD/control/control"
pack "dist/${PKG}_${VERSION}_all_experimental.deb"
rm -f "$BUILD/control/md5sums"
if command -v dpkg-deb >/dev/null 2>&1; then
	dpkg-deb --info "dist/${PKG}_${VERSION}_all_experimental.deb" >/dev/null && echo "  dpkg-deb: package structure ok"
fi

# Checksums for the release page: verify with "sha256sum -c SHA256SUMS"
( cd dist && sha256sum "${PKG}_${VERSION}_all.ipk" "${PKG}_${VERSION}_all_experimental.deb" > SHA256SUMS )
echo "Built dist/SHA256SUMS"
