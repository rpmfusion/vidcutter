%global unique_name com.ozmartians

Name:           vidcutter
Version:        5.5.0
Release:        2%{?dist}
Summary:        The simplest + fastest video cutter & joiner
License:        GPLv3+
Url:            http://vidcutter.ozmartians.com
Source0:        https://github.com/ozmartian/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  mpv-libs-devel
BuildRequires:  desktop-file-utils
BuildRequires:  libappstream-glib

Requires:       python3-qt5
Requires:       ffmpeg
Requires:       python3-pyopengl
Requires:       mediainfo
Requires:       hicolor-icon-theme
Requires:       mpv-libs

%description
The simplest & sexiest tool for cutting and joining your videos without the
need for re-encoding or a diploma in multimedia. VidCutter focuses on getting
the job done using tried and true tech in its arsenal via mpv and FFmpeg.

%prep
%setup -q
sed -i "s/pypi/rpm/" vidcutter/__init__.py
# Fix error: Empty %%files file debugsourcefiles.list
sed -i "s/-g0/-g/" setup.py

# E: wrong-script-interpreter
sed -i -e 's|#!/usr/bin/env python3|#!/usr/bin/python3|g' vidcutter/*.py
sed -i -e 's|#!/usr/bin/env python3|#!/usr/bin/python3|g' vidcutter/libs/*.py

%build
%py3_build

%install
%py3_install
# E: non-executable-script
for file in %{buildroot}%{python3_sitearch}/vidcutter/{__init__,__main__,about,graphicseffects,mediainfo,mediastream,settings,updater,videoconsole,videocutter,videolist,videoslider,videosliderwidget,videostyle,libs/config,libs/mpvwidget,libs/munch,libs/notifications,libs/singleapplication,libs/taskbarprogress,libs/videoservice,libs/widgets}.py; do
    chmod a+x $file
done

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/{appdata,metainfo}/*.appdata.xml

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{python3_sitearch}/%{name}
%{python3_sitearch}/vidcutter-*-py?.?.egg-info
%{_datadir}/applications/%{unique_name}.%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.png
%{_datadir}/icons/hicolor/scalable/apps/%{name}.svg
%{_datadir}/mime/packages/x-vidcutter.xml
%{_datadir}/mime/packages/wtv.xml
%{_datadir}/appdata/%{unique_name}.%{name}.appdata.xml
%{_datadir}/metainfo/%{unique_name}.%{name}.appdata.xml
%{_datadir}/pixmaps/%{name}.svg

%changelog
* Sun Feb 11 2018 Leigh Scott <leigh123linux@googlemail.com> - 5.5.0-2
- Vailidate appdata
- Remove scriptlets

* Tue Feb 06 2018 Martin Gansser <martinkg@fedoraproject.org> - 5.5.0-1
- Update to 5.5.0
- Dropped OpenGL_fix.patch

* Thu Feb 01 2018 Martin Gansser <martinkg@fedoraproject.org> - 5.0.5-3
- Add OpenGL_fix.patch fixes (rfbz#4777).

* Mon Jan 29 2018 Martin Gansser <martinkg@fedoraproject.org> - 5.0.5-2
- Add RR mpv-libs

* Sun Dec 03 2017 Martin Gansser <martinkg@fedoraproject.org> - 5.0.5-1
- Update to 5.0.5

* Sun Nov 05 2017 Leigh Scott <leigh123linux@googlemail.com> - 4.0.5-2
- Remove mime scriptlets as they are obsolete in f25 and greater

* Sat Nov 04 2017 Martin Gansser <martinkg@fedoraproject.org> - 4.0.5-1
- Update to 4.0.5
- Set extra_compile_args= to -g to fix: Empty %%files file debugsourcefiles.list

* Mon Aug 07 2017 Martin Gansser <martinkg@fedoraproject.org> - 4.0.0-2
- Add BR desktop-file-utils
- Add RR hicolor-icon-theme

* Mon Aug 07 2017 Martin Gansser <martinkg@fedoraproject.org> - 4.0.0-1
- Initial build
