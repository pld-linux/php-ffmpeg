#
# TODO: doesn't pass all tests
#
# Conditional build:
%bcond_with	tests		# build without tests

%define		modname	ffmpeg
Summary:	Extension to manipulate movie in PHP
Summary(pl.UTF-8):	Rozszerzenie do obróbki filmów w PHP
Name:		php-%{modname}
Version:	0.6.3
Release:	6
License:	GPL
Group:		Development/Languages/PHP
Source0:	http://downloads.sourceforge.net/ffmpeg-php/ffmpeg-php-0.6.0.tbz2
# Source0-md5:	f779c0dbffda9dac54729d60c0e04c05
Patch100:	branch.diff
Patch1:		avcodec_find_decoder-warn.patch
Patch4:		ffmpeg-0.6.patch
Patch6:		allow_persistent_on_persistentMovie.phpt.patch
Patch7:		test_fixes.patch
Patch8:		tests-frame_md5.patch
Patch9:		tests-metadata-api.patch
Patch10:	%{name}-ffmpeg08.patch
URL:		http://ffmpeg-php.sourceforge.net/
%if %{with tests}
BuildRequires:	/usr/bin/php
BuildRequires:	php-devel >= 4:5.3.2-5
BuildRequires:	php-pcre
%else
BuildRequires:	php-devel >= 3:5.0.0
%endif
BuildRequires:	ffmpeg-devel >= 0.7.1
BuildRequires:	php-gd
BuildRequires:	rpm >= 4.4.9-56
BuildRequires:	rpmbuild(macros) >= 1.344
Requires:	php(core) >= 5.0.4
Requires:	php-gd
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
php-ffmpeg is an extension for PHP that adds an easy to use,
object-oriented API for accessing and retrieving information from
video and audio files. It has methods for returning frames from movie
files as images that can be manipulated using PHP's image functions.
This works well for automatically creating thumbnail images from
movies. ffmpeg-php is also useful for reporting the duration and
bitrate of audio files (mp3, wma...). ffmpeg-php can access many of
the video formats supported by ffmpeg (mov, avi, mpg, wmv...).

%description -l pl.UTF-8
php-ffmpeg to rozszerzenie PHP dodające łatwe w użyciu, zorientowane
obiektowo API pozwalające na odtwarzanie informacji z plików filmów i
dźwiękowych. Zawiera metody zwracające ramki filmów jako obrazy, które
można obrabiać funkcjami PHP. Pozwala to automatycznie tworzyć
miniaturki obrazów z filmów. ffmpeg-php jest przydatne także do
uzyskiwania informacji o czasie trwania i paśmie plików dźwiękowych
(mp3, wma...). ffmpeg-php pozwala na dostęp do wielu formatów filmów
obsługiwanych przez ffmpeg (mov, avi, mpg, wmv...).

%prep
%setup -q -n ffmpeg-php-0.6.0
%patch100 -p0
%patch1 -p1
%if "%{pld_release}" != "ac"
%patch4 -p1
%endif
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1

# empty file
rm tests/getFramesBackwards.phpt

%build
phpize
CPPFLAGS="%{rpmcppflags}"
%configure
%{__make}

%if %{with tests}
cat <<'EOF' > run-tests.sh
#!/bin/sh
%{__make} test \
	PHP_TEST_SHARED_SYSTEM_EXTENSIONS+="gd" \
	RUN_TESTS_SETTINGS="-q $*"
EOF
chmod +x run-tests.sh
./run-tests.sh -w failed.log
test -f failed.log -a ! -s failed.log
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

# install config file
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so

; --- options for %{modname}
;ffmpeg.allow_persistent = 0
;ffmpeg.show_warnings = 0
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc ChangeLog CREDITS EXPERIMENTAL LICENSE TODO test_ffmpeg.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
