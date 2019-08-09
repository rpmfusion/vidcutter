%global unique_name com.ozmartians
%global rname VidCutter

Name:           vidcutter
Version:        6.0.0
Release:        6%{?dist}
Summary:        The simplest + fastest video cutter & joiner
License:        GPLv3+
Url:            http://vidcutter.ozmartians.com
Source0:        https://github.com/ozmartian/%{name}/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz

BuildRequires:  gcc
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
for file in %{buildroot}%{python3_sitearch}/vidcutter/{__init__,__main__,about,changelog,mediainfo,mediastream,settings,updater,videoconsole,videocutter,videolist,videoslider,videosliderwidget,videostyle,libs/ffmetadata,libs/graphicseffects,libs/config,libs/mpvwidget,libs/munch,libs/notifications,libs/singleapplication,libs/taskbarprogress,libs/videoservice,libs/widgets}.py; do
    chmod a+x $file
done

rm -f %{buildroot}%{_datadir}/doc/vidcutter/LICENSE

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/*.desktop
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/metainfo/*.appdata.xml

%files
%license LICENSE
%doc README.md CHANGELOG
%{_bindir}/%{name}
%{python3_sitearch}/%{name}
%{python3_sitearch}/vidcutter-*-py?.?.egg-info
%{_datadir}/applications/%{unique_name}.%{rname}.desktop
%{_datadir}/icons/hicolor/*/apps/%{unique_name}.%{rname}.png
%{_datadir}/icons/hicolor/scalable/apps/%{unique_name}.%{rname}.svg
%{_datadir}/metainfo/%{unique_name}.%{rname}.appdata.xml
%{_datadir}/mime/packages/%{unique_name}.%{rname}.xml

%changelog
* Fri Aug 09 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 Leigh Scott <leigh123linux@googlemail.com> - 6.0.0-4
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 6.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jul 10 2018 Miro Hrončok <mhroncok@redhat.com> - 6.0.0-2
- Rebuilt for Python 3.7

* Fri Jun 29 2018 Martin Gansser <martinkg@fedoraproject.org> - 6.0.0-1
- Update to 6.0.0

* Thu Mar 01 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 5.5.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

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
