%define		_modname	ffmpeg
Summary:	Extension to manipulate movie in PHP
Summary(pl.UTF-8):	Rozszerzenie do obróbki filmów w PHP
Name:		php-%{_modname}
Version:	0.6.0
Release:	2
License:	GPL
Group:		Development/Languages/PHP
Source0:	http://dl.sourceforge.net/ffmpeg-php/ffmpeg-php-%{version}.tbz2
# Source0-md5:	f779c0dbffda9dac54729d60c0e04c05
URL:		http://ffmpeg-php.sourceforge.net/
BuildRequires:	ffmpeg-devel >= 0.4.9
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	php-gd
BuildRequires:	rpmbuild(macros) >= 1.344
Requires:	php-common >= 4:5.0.4
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
%setup -q -n ffmpeg-php-%{version}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT \
	EXTENSION_DIR=%{php_extensiondir}

# install config file
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc ChangeLog CREDITS EXPERIMENTAL LICENSE TODO test_ffmpeg.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
