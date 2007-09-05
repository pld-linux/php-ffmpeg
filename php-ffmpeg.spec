%define		_modname	ffmpeg
Summary:	Extension to manipulate movie in PHP
Name:		php-%{_modname}
Version:	0.5.1
Release:	0.1
License:	GPL
Group:		Development/Languages/PHP
URL:		http://ffmpeg-php.sourceforge.net/
Source0:	http://dl.sourceforge.net/ffmpeg-php/ffmpeg-php-%{version}.tbz2
# Source0-md5:	705e306c0687cf3fb4743c2a7e847c2f
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

%prep
%setup -q -n ffmpeg-php-%{version}
#%{__sed} -i -e 's@/lib@/%{_lib}@' config.m4

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
