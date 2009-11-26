Name: chromium-browser
Version: 2.0.249.0.r32802
Release: %mkrel 2
Summary: A fast webkit-based web browser
Group:Applications/Internet
License: BSD, LGPL
Source0: chromium-%{version}.tar.bz2
Source1: chromium-wrapper
Source2: chromium-browser.desktop
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires: bison, flex, gtk2-devel, atk-devel, libexpat1-devel, gperf
BuildRequires: libnspr-devel, libnss-devel, libGConf2-devel, libalsa2-devel

%description
Google Chrome is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

%prep
%setup -q -n chromium-%{version}

%build
%make chrome BUILDTYPE=Release

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/chromium-browser
mkdir -p %{buildroot}%{_libdir}/chromium-browser/locales
mkdir -p %{buildroot}%{_libdir}/chromium-browser/themes
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{_sourcedir}/chromium-wrapper %{buildroot}%{_libdir}/chromium-browser/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/chromium-browser/
install -m 644 out/Release/chromium-browser.1 %{buildroot}%{_mandir}/man1/
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
%{_libdir}/chromium-browser/chrome.pak
%{_libdir}/chromium-browser/libffmpegsumo.so
%{_libdir}/chromium-browser/locales
%{_libdir}/chromium-browser/resources
%{_libdir}/chromium-browser/themes
%{_libdir}/chromium-browser/xdg-settings
%{_mandir}/man1/chromium-browser*
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/*/apps/%{name}.png

