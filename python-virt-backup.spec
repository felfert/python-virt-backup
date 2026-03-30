# -*- rpm-spec -*-

# Upstream name and name of the command (both clash with old virt-backup (written in perl)
%global shortname virt-backup

Summary: A %{shortname}, written in python
Name:    python-%{shortname}
Version: 0.5.7
Release: 1%{?dist}
License: BSD-2-Clause

%global  forgeurl        https://github.com/aruhier/%{shortname}
%global  tag             v%{version}

%forgemeta -a

Source0: %{forgesource0}
URL:     %{forgeurl0}

# The binary name clashes with the same name from the package virt-backup (written in perl).
# Therefore, we provide an alternatives setup.
Requires(post): %{_bindir}/update-alternatives
Requires(postun): %{_bindir}/update-alternatives
Requires(preun): %{_bindir}/update-alternatives

# Until the old virt-backup package is changed to honor an alternatives setup,
# the following prevents accidents from happening.
Conflicts: virt-backup

BuildArch:     noarch
BuildRequires: python3-devel

%global desc %{expand:
This package provides external backup of your KVM guests, managed by libvirt, using the BlockCommit feature. The main goal is to have a modest alternative to the Proxmox VE backup system (without their vma system) to automatically backup your disks (with optional compression) and easily restore ones. Guests are configured by groups, and can be matched via regex.}

%description %desc

%package -n python3-%{shortname}
Summary:        %{summary}

%description -n python3-%{shortname} %desc

%prep
%autosetup -n %{shortname}-%{version}

%generate_buildrequires
%pyproject_buildrequires -t -p

%build
%pyproject_wheel

%install
%pyproject_install
# rename files for alternative usage.
mv %{buildroot}%{_bindir}/virt-backup %{buildroot}%{_bindir}/virt-backup.python
touch %{buildroot}%{_bindir}/virt-backup

%pyproject_save_files -l virt_backup
# Remove build-time-only artifacts.
rm -rf %{buildroot}/%{python3_sitelib}/{docs,tests}

%check
%tox

%files -n python3-%{shortname} -f %{pyproject_files}
%doc README.mkd LICENSE.mkd example/
%ghost %{_bindir}/virt-backup
%{_bindir}/virt-backup.python

%post -n  python3-%{shortname}
update-alternatives --install %{_bindir}/virt-backup \
  virt-backup %{_bindir}/virt-backup.python 90

%postun -n  python3-%{shortname}
if [ $1 -eq 0 ] ; then
  update-alternatives --remove virt-backup %{_bindir}/virt-backup.python
fi

%changelog
* Fri Mar 27 2026 Fritz Elfert <fritz@fritz-elfert.de> - 0.5.7-1
- Initial packaging for Fedora and EPEL
