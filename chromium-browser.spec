%define revision 190148

Summary:	A fast webkit-based web browser
Name:		chromium
Version:	26.0.1410.46
Release:	1
Group:		Applications/Internet
License:	BSD, LGPL
URL:		http://www.chromium.org/

Source0:	http://download.rfremix.ru/storage/chromium/%{version}/%{name}-%{version}.tar.xz
Source1:	chromium-wrapper
Source2:	chromium-browser.desktop
Source30:	master_preferences
Source31:	default_bookmarks.html

Patch0:		chromium-26.0.1410.46-master-prefs-path.patch
# fix http://code.google.com/p/chromium/issues/detail?id=136023
Patch3:		chromium-20.0.1132.47-glibc216.patch
# (cjw) fix "Uncaught exception" in 2 calls to webkitTransform (hack, need to test if this is still needed)
# http://code.google.com/p/chromium/issues/detail?id=152407
Patch5:		chromium-25-webkitTransform-exception.patch

# PATCH-FIX-OPENSUSE patches in system glew library
Patch13:	chromium-25.0.1364.172-system-glew.patch
# PATCH-FIX-OPENSUSE removes build part for courgette
Patch14:	chromium-25.0.1364.172-no-courgette.patch
# PATCH-FIX-OPENSUSE Compile the sandbox with -fPIE settings
Patch15:	chromium-25.0.1364.172-sandbox-pie.patch

BuildRequires:	alsa-oss-devel
BuildRequires:	pkgconfig(atk)
BuildRequires:	bison
BuildRequires:	bzip2-devel
BuildRequires:	cups-devel
BuildRequires:	dbus-glib-devel
BuildRequires:	elfutils-devel
BuildRequires:	expat-devel
BuildRequires:	flac-devel
BuildRequires:	flex
BuildRequires:	glib2-devel
BuildRequires:	gperf
BuildRequires:	gtk+2.0-devel
BuildRequires:	pkgconfig(xscrnsaver)
BuildRequires:	pkgconfig(xt)
BuildRequires:	pkgconfig(xtst)
BuildRequires:	pkgconfig(libevent)
BuildRequires:	jpeg-devel
#BuildRequires:	libpng-devel
BuildRequires:	pkgconfig(udev)
BuildRequires:	pkgconfig(vpx)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(libxslt)
BuildRequires:	pkgconfig(gl)
BuildRequires:	mesaglu-devel
BuildRequires:	nspr-devel
BuildRequires:	nss-devel
BuildRequires:	openssl-devel
BuildRequires:	perl(Switch)
BuildRequires:	perl(Digest::MD5)
BuildRequires:	pulseaudio-devel
BuildRequires:	speex-devel
BuildRequires:	subversion
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(libusb-1.0)
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(libexif)
BuildRequires:	pkgconfig(opus)
BuildRequires:	speech_tools-devel
BuildRequires:	gpsd-devel
BuildRequires:	srtp-devel
BuildRequires:	pkgconfig(libmtp)
BuildRequires:	webp-devel
BuildRequires:	harfbuzz-devel
BuildRequires:	icu-devel
BuildRequires:	minizip-devel
BuildRequires:	yasm-devel
BuildRequires:	pciutils-devel
BuildRequires:	v8-devel

BuildRequires:	pkgconfig(gnome-keyring-1)

# NaCl needs these
%ifarch x86_64
BuildRequires:	/lib/libc.so.6
BuildRequires:	/lib/libz.so.1
BuildRequires:	/lib/libgcc_s.so.1
%endif

Requires:	hicolor-icon-theme

Obsoletes:	chromium-ffmpeg

ExclusiveArch: i686 x86_64 armv7l

%description
Chromium is a browser that combines a minimal design with sophisticated
technology to make the web faster, safer, and easier.

This is the stable channel Chromium browser. It offers a rock solid
browser which is updated with features and fixes once they have been
thoroughly tested. If you want the latest features, install the
chromium-browser-unstable package instead.

Note: If you are reverting from unstable to stable or beta channel, you may
experience tab crashes on startup. This crash only affects tabs restored
during the first launch due to a change in how tab state is stored.
See http://bugs.chromium.org/34688. It's always a good idea to back up
your profile before changing channels.


%package -n chromedriver
Summary:	WebDriver for Google Chrome/Chromium
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}


%description -n chromedriver
WebDriver is an open source tool for automated testing of webapps across many
browsers. It provides capabilities for navigating to web pages, user input,
JavaScript execution, and more. ChromeDriver is a standalone server which
implements WebDriver's wire protocol for Chromium. It is being developed by
members of the Chromium and WebDriver teams.


%prep
%setup -q
%patch0 -p1 -b .master-prefs
%patch3 -p1 -b .glibc216
%patch5 -p2 -b .webkitTransform-exception

# openSUSE patches
%patch13 -p1
%patch14 -p1
%patch15 -p1

echo "%{revision}" > build/LASTCHANGE.in

# Hard code extra version
FILE=chrome/common/chrome_version_info_posix.cc
sed -i.orig -e 's/getenv("CHROME_VERSION_EXTRA")/"Russian Fedora"/' $FILE
cmp $FILE $FILE.orig && exit 1

%ifarch x86_64
sed -i "s#/lib/#/lib64/#g" %{SOURCE2}
%endif

%ifarch i686
sed -i "s#/lib64/#/lib/#g" %{SOURCE2}
%endif

%build
export GYP_GENERATORS=make
build/gyp_chromium --depth=. \
	-D linux_sandbox_path=%{_libdir}/%{name}/chrome-sandbox \
	-D linux_sandbox_chrome_path=%{_libdir}/%{name}/chrome \
	-D linux_link_gnome_keyring=0 \
	-D use_gconf=0 \
	-D werror='' \
	-D use_system_sqlite=0 \
	-D use_system_libxml=0 \
	-D use_system_zlib=0 \
	-D use_system_bzip2=1 \
	-D use_system_libbz2=1 \
	-D use_system_libpng=0 \
	-D use_system_libjpeg=1 \
	-D use_system_libevent=1 \
	-D use_system_flac=1 \
	-D use_system_vpx=1 \
	-D use_system_speex=1 \
	-D use_system_libusb=1 \
	-D use_system_libexif=1 \
	-D use_system_libsrtp=1 \
	-D use_system_libmtp=1 \
	-D use_system_opus=1 \
	-D use_system_libwebp=1 \
	-D use_system_harfbuzz=1 \
	-D use_system_minizip=1 \
	-D use_system_yasm=1 \
	-D use_system_xdg_utils=1 \
	-D build_ffmpegsumo=1 \
	-D use_system_ffmpeg=0 \
	-D use_pulseaudio=1 \
	-D use_system_v8=1 \
	-D linux_link_libpci=1 \
	-D linux_link_gsettings=1 \
	-D linux_link_libspeechd=1 \
	-D linux_link_kerberos=1 \
	-D linux_link_libgps=1 \
	-D use_system_icu=1 \
%ifarch i686
	-D disable_sse2=1 \
	-D release_extra_cflags="-march=i686"
%endif
%ifarch armv7l
	-D target_arch=arm \
	-D linux_use_tcmalloc=0 \
	-D disable_nacl=1 \
	-D armv7=1 \
	-D release_extra_cflags="-marm"
%endif

# Note: DON'T use system sqlite (3.7.3) -- it breaks history search

%make chrome chrome_sandbox chromedriver BUILDTYPE=Release

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}/%{name}/locales
mkdir -p %{buildroot}%{_libdir}/%{name}/themes
mkdir -p %{buildroot}%{_libdir}/%{name}/default_apps
mkdir -p %{buildroot}%{_mandir}/man1
install -m 755 %{SOURCE1} %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/chrome %{buildroot}%{_libdir}/%{name}/
install -m 4755 out/Release/chrome_sandbox %{buildroot}%{_libdir}/%{name}/chrome-sandbox
cp -a out/Release/chromedriver %{buildroot}%{_libdir}/%{name}/chromedriver
install -m 644 out/Release/chrome.1 %{buildroot}%{_mandir}/man1/%{name}.1
install -m 644 out/Release/chrome.pak %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/libffmpegsumo.so %{buildroot}%{_libdir}/%{name}/
%ifnarch armv7l
install -m 755 out/Release/libppGoogleNaClPluginChrome.so %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/nacl_helper_bootstrap %{buildroot}%{_libdir}/%{name}/
install -m 755 out/Release/nacl_helper %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/nacl_irt_*.nexe %{buildroot}%{_libdir}/%{name}/
%endif
install -m 644 out/Release/locales/*.pak %{buildroot}%{_libdir}/%{name}/locales/
#install -m 755 out/Release/xdg-mime %{buildroot}%{_libdir}/%{name}/
#install -m 755 out/Release/xdg-settings %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/chrome_100_percent.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/content_resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 out/Release/resources.pak %{buildroot}%{_libdir}/%{name}/
install -m 644 chrome/browser/resources/default_apps/* %{buildroot}%{_libdir}/%{name}/default_apps/
ln -s %{_libdir}/%{name}/chromium-wrapper %{buildroot}%{_bindir}/%{name}
ln -s %{_libdir}/%{name}/chromedriver %{buildroot}%{_bindir}/chromedriver

find out/Release/resources/ -name "*.d" -exec rm {} \;
cp -r out/Release/resources %{buildroot}%{_libdir}/%{name}

# desktop file
mkdir -p %{buildroot}%{_datadir}/applications
install -m 644 %{SOURCE2} %{buildroot}%{_datadir}/applications/

# icon
for i in 22 24 48 64 128 256; do
	mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps
	install -m 644 chrome/app/theme/chromium/product_logo_$i.png \
		%{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

# Install the master_preferences file
mkdir -p %{buildroot}%{_sysconfdir}/%{name}
install -m 0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/%{name}/
install -m 0644 %{SOURCE31} %{buildroot}%{_sysconfdir}/%{name}/

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%doc LICENSE AUTHORS
%config %{_sysconfdir}/%{name}
%{_bindir}/%{name}
%{_libdir}/%{name}/chromium-wrapper
%{_libdir}/%{name}/chrome
%{_libdir}/%{name}/chrome-sandbox
%{_libdir}/%{name}/chrome.pak
%{_libdir}/%{name}/libffmpegsumo.so
%ifnarch armv7l
%{_libdir}/%{name}/libppGoogleNaClPluginChrome.so
%{_libdir}/%{name}/nacl_helper_bootstrap
%{_libdir}/%{name}/nacl_helper
%{_libdir}/%{name}/nacl_irt_*.nexe
%endif
%{_libdir}/%{name}/locales
%{_libdir}/%{name}/chrome_100_percent.pak
%{_libdir}/%{name}/content_resources.pak
%{_libdir}/%{name}/resources.pak
%{_libdir}/%{name}/resources
%{_libdir}/%{name}/themes
%{_libdir}/%{name}/default_apps
#%{_libdir}/%{name}/xdg-mime
#%{_libdir}/%{name}/xdg-settings
%{_mandir}/man1/%{name}*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png


%files -n chromedriver
%doc LICENSE AUTHORS
%{_bindir}/chromedriver
%{_libdir}/%{name}/chromedriver
