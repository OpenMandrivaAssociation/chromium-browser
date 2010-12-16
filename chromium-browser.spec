%define svn_revision 66965

Name: chromium-browser
Version: 9.0.592.0.r%{svn_revision}
Release: %mkrel 2
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
Source0: chromium-%{version}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
Source100: scoped_nsautorelease_pool.h
Patch0: chromium-66965-typecast.patch
Patch1: chromium-66422-skip-builder-tests.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, libexpat-devel, gperf
BuildRequires: libnspr-devel, libnss-devel, libGConf2-devel, libalsa-devel
BuildRequires: libglib2-devel, libbzip2-devel, libz-devel, libpng-devel
BuildRequires: libjpeg-devel, libmesagl-devel, libmesaglu-devel
BuildRequires: libxscrnsaver-devel, libdbus-glib-devel, libcups-devel
BuildRequires: libgnome-keyring-devel libvpx-devel libxtst-devel
#BuildRequires: libicu-devel >= 4.6
ExclusiveArch: i586 x86_64 arm

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is an unstable development version of the Chromium browser. It may
contain bugs or partially implemented features.

%prep
%setup -q -n chromium-%{svn_revision}
%patch0 -p1 -b .typecast
%patch1 -p1 -b .skip-builder-tests
echo "%{svn_revision}-%{release}" > build/LASTCHANGE.in

install -D %{_sourcedir}/scoped_nsautorelease_pool.h base/mac/scoped_nsautorelease_pool.h

# Temporary fix for libvpx
mkdir third_party/libvpx/include
ln -s /usr/include/vpx third_party/libvpx/include


%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_libdir}/chromium-browser/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_libdir}/chromium-browser/chrome \
	-D linux_link_gnome_keyring=0 \
%ifarch i586
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i586"
%endif

%make chrome chrome_sandbox BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/chromium-browser
mkdir -p %{buildroot}%{_libdir}/chromium-browser/locales
mkdir -p %{buildroot}%{_libdir}/chromium-browser/themes
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_sourcedir}/chromium-wrapper %{buildroot}%{_libdir}/chromium-browser/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/chromium-browser/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_libdir}/chromium-browser/chrome-sandbox
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_libdir}/chromium-browser/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_libdir}/chromium-browser/
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/chromium-browser/locales
install -m 644 out/Release/xdg-settings %{buildroot}%{_libdir}/chromium-browser/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/chromium-browser/
ln -s %{_libdir}/chromium-browser/chromium-wrapper %{buildroot}%{_bindir}/chromium-browser

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_libdir}/chromium-browser/

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{_sourcedir}/%{name}.desktop %{buildroot}%{_datadir}/applications/

# icon
for i in 16 32 48 256; do
	mkdir -p %{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_iconsdir}/hicolor/${i}x${i}/apps/%{name}.png
done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_bindir}/chromium-browser
%{_libdir}/chromium-browser/chromium-wrapper
%{_libdir}/chromium-browser/chrome
%{_libdir}/chromium-browser/chrome-sandbox
%{_libdir}/chromium-browser/chrome.pak
%{_libdir}/chromium-browser/libffmpegsumo.so
%{_libdir}/chromium-browser/locales
%{_libdir}/chromium-browser/resources.pak
%{_libdir}/chromium-browser/resources
%{_libdir}/chromium-browser/themes
%{_libdir}/chromium-browser/xdg-settings
%{_mandir}/man1/chromium-browser*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png
