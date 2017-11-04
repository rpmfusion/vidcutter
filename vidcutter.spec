%define debug_package %{nil}

Name:           vidcutter
Version:        4.0.5
Release:        1%{?dist}
Summary:        The simplest + fastest video cutter & joiner
License:        GPLv3+
Url:            http://vidcutter.ozmartians.com
Source0:        https://github.com/ozmartian/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  mpv-libs-devel
BuildRequires:  desktop-file-utils
Requires:       python3-qt5
Requires:       ffmpeg
Requires:       python3-pyopengl
Requires:       mediainfo
Requires:       hicolor-icon-theme

%description
The simplest & sexiest tool for cutting and joining your videos without the
need for re-encoding or a diploma in multimedia. VidCutter focuses on getting
the job done using tried and true tech in its arsenal via mpv and FFmpeg.

%prep
%setup -q
sed -i "s/pypi/rpm/" vidcutter/__init__.py

# E: wrong-script-interpreter
sed -i -e 's|#!/usr/bin/env python3|#!/usr/bin/python3|g' vidcutter/*.py
sed -i -e 's|#!/usr/bin/env python3|#!/usr/bin/python3|g' vidcutter/libs/*.py

%build
%py3_build

%install
%py3_install
# E: non-executable-script
for file in %{buildroot}%{python3_sitearch}/vidcutter/{__init__,__main__,about,settings,updater,videoconsole,videocutter,videoinfo,videolist,videoslider,videostyle,videotoolbar,libs/mpvwidget,libs/notifications,libs/taskbarprogress,libs/videoservice,libs/widgets}.py; do
    chmod a+x $file
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop

%post
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
/sbin/ldconfig
if [ $1 -eq 0 ] ; then
  touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitearch}/%{name}
%{python3_sitearch}/vidcutter-*-py?.?.egg-info
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/x-vidcutter.xml
%{_datadir}/pixmaps/%{name}.svg

%changelog
* Sat Nov 04 2017 Martin Gansser <martinkg@fedoraproject.org> - 4.0.5-1
- Update to 4.0.5
- Add %%define debug_package %%{nil} for f27 build

* Mon Aug 07 2017 Martin Gansser <martinkg@fedoraproject.org> - 4.0.0-2
- Add BR desktop-file-utils
- Add RR hicolor-icon-theme
- Remove mime scriptlets as they are obsolete in f25 and greater

* Mon Aug 07 2017 Martin Gansser <martinkg@fedoraproject.org> - 4.0.0-1
- Initial build
