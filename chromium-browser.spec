%define svn_revision 32802

Name: chromium-browser
Version: 4.0.249.0.r%{svn_revision}
Release: %mkrel 5
Summary: A fast webkit-based web browser
Group: Networking/WWW
License: BSD, LGPL
Source0: chromium-%{version}.tar.xz
Source1: chromium-wrapper
Source2: chromium-browser.desktop
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, libexpat-devel, gperf
BuildRequires: libnspr-devel, libnss-devel, libGConf2-devel, libalsa-devel
BuildRequires: libglib2-devel
ExclusiveArch: i586 x86_64 arm

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is an unstable development version of the Chromium browser. It may
contain bugs or partially implemented features.

%prep
%setup -q -n chromium-%{svn_revision}
echo %{svn_revision} > build/LASTCHANGE.in

%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_libdir}/chromium-browser/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_libdir}/chromium-browser/chrome

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
install -m 644 out/Release/chromium-browser.1 %{buildroot}%{_mandir}/man1/chromium-browser.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_libdir}/chromium-browser/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_libdir}/chromium-browser/
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/chromium-browser/locales
install -m 644 out/Release/xdg-settings %{buildroot}%{_libdir}/chromium-browser/
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
%{_libdir}/chromium-browser/resources
%{_libdir}/chromium-browser/themes
%{_libdir}/chromium-browser/xdg-settings
%{_mandir}/man1/chromium-browser*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

