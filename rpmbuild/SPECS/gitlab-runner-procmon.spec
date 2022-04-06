Name:         gitlab-runner-procmon
Version:      0.2.0
Release:      1%{?dist}
Summary:      Terminates orphaned Packer instances in GitLab CI jobs

License:      GPLv3+
BuildArch:    noarch
SOURCE0:      gitlab-runner-procmon.py

%if "%{dist}" == ".el7"
Requires:     python3
Requires:     python36-psutil
%endif

%if "%{dist}" == ".el8"
%undefine     __brp_mangle_shebangs
Requires:     python3
Requires:     python3-psutil
%endif

%description
Terminates orphaned Packer instances spawned from GitLab CI jobs

%prep
cd %{_topdir}/BUILD
cp %{SOURCE0} ./gitlab-runner-procmon.py

%build

%install
TOOLS_DIR=%{buildroot}%{_bindir}
install -d -m 0755 %TOOLS_DIR
install -m 0755 gitlab-runner-procmon.py $TOOLS_DIR/gitlab-runner-procmon

%post

%files
%{_bindir}/%{name}

%changelog
* Tue Apr 5 2022 hakirot  hackirot@proton.me - 0.1.0-1
- Create project
