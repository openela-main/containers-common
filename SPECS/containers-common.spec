# Below definitions are used to deliver config files from a particular branch
# of c/image, c/storage  and c/shortnames vendored in all of Buildah, Podman and Skopeo.
# These vendored components must have the same version. If it is not the case,
# pick the oldest version on c/image, c/storage and c/shortnames vendored in
# Buildah/Podman/Skopeo.

# Packit will automatically update the image and storage versions on Fedora and
# CentOS Stream dist-git PRs.
%global skopeo_branch main
%global image_branch v5.36.0
%global storage_branch v1.59.0
%global shortnames_branch main
%global common_branch v0.64.0

%global common_version %(v=%{common_branch}; echo ${v:1})

Name: containers-common
Epoch: 5
Version: %{common_version}
Release: 4%{?dist}
License: Apache-2.0
BuildArch: noarch
# for BuildRequires: go-md2man
ExclusiveArch: %{golang_arches} noarch
Summary: Common configuration and documentation for containers
BuildRequires: git-core
BuildRequires: go-md2man
Provides: skopeo-containers = %{epoch}:%{version}-%{release}
Requires: (container-selinux >= 2:2.162.1 if selinux-policy)
Requires: netavark
Obsoletes: containernetworking-plugins < 2
Suggests: fuse-overlayfs
%if 0%{?rhel}
Requires: /etc/pki/sigstore/REKOR-signing-key
Requires: /etc/pki/sigstore/SIGSTORE-redhat-release3
%endif
URL: https://github.com/containers/common
Source1: https://raw.githubusercontent.com/containers/storage/%{storage_branch}/storage.conf
Source2: https://raw.githubusercontent.com/containers/storage/%{storage_branch}/docs/containers-storage.conf.5.md
Source3: mounts.conf
Source4: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.conf.5.md
Source5: https://raw.githubusercontent.com/containers/image/%{image_branch}/registries.conf
Source6: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-policy.json.5.md
Source7: https://raw.githubusercontent.com/containers/common/%{common_branch}/pkg/seccomp/seccomp.json
Source8: https://raw.githubusercontent.com/containers/common/%{common_branch}/docs/containers-mounts.conf.5.md
Source9: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-signature.5.md
Source10: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-transports.5.md
Source11: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-certs.d.5.md
Source12: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.d.5.md
Source13: https://raw.githubusercontent.com/containers/common/%{common_branch}/pkg/config/containers.conf
Source14: https://raw.githubusercontent.com/containers/common/%{common_branch}/docs/containers.conf.5.md
Source15: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-auth.json.5.md
Source16: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.conf.d.5.md
Source17: https://raw.githubusercontent.com/containers/shortnames/%{shortnames_branch}/shortnames.conf
Source18: https://raw.githubusercontent.com/containers/common/refs/heads/main/pkg/hooks/docs/oci-hooks.5.md
Source19: 001-rhel-shortnames-pyxis.conf
Source20: 002-rhel-shortnames-overrides.conf
Source22: registry.access.redhat.com.yaml
Source23: registry.redhat.io.yaml
#Source24: https://raw.githubusercontent.com/containers/skopeo/%%{skopeo_branch}/default-policy.json
Source24: default-policy.json
Source25: https://raw.githubusercontent.com/containers/skopeo/%{skopeo_branch}/default.yaml
# FIXME: fix the branch once these are available via regular c/common branch
Source26: https://raw.githubusercontent.com/containers/common/main/docs/Containerfile.5.md
Source27: https://raw.githubusercontent.com/containers/common/main/docs/containerignore.5.md
Source29: REKOR-signing-key
Source30: SIGSTORE-redhat-release3

# scripts used for synchronization with upstream and shortname generation
Source100: update.sh
Source101: update-vendored.sh
Source102: pyxis.sh

%description
This package contains common configuration files and documentation for container
tools ecosystem, such as Podman, Buildah and Skopeo.

It is required because the most of configuration files and docs come from projects
which are vendored into Podman, Buildah, Skopeo, etc. but they are not packaged
separately.

%package extra
Summary: Extra dependencies for Podman and Buildah
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: container-network-stack
Requires: oci-runtime
Requires: nftables
Requires: passt

%description extra
This subpackage will handle dependencies common to Podman and Buildah which are
not required by Skopeo.

%prep

%build

%install
install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d,systemd,registries.d,registries.conf.d}
install -dp %{buildroot}%{_datadir}/containers/systemd
install -dp %{buildroot}%{_sharedstatedir}/containers/sigstore
install -dp %{buildroot}%{_prefix}/lib/containers/storage
install -dp -m 700 %{buildroot}%{_prefix}/lib/containers/storage/overlay-images
touch %{buildroot}%{_prefix}/lib/containers/storage/overlay-images/images.lock
install -dp -m 700 %{buildroot}%{_prefix}/lib/containers/storage/overlay-layers
touch %{buildroot}%{_prefix}/lib/containers/storage/overlay-layers/layers.lock

install -m0644 %{SOURCE1} %{buildroot}%{_datadir}/containers/storage.conf
install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containers/registries.conf
install -m0644 %{SOURCE17} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
%if 0%{?fedora} == 0 && 0%{?centos} == 0
    install -m0644 %{SOURCE19} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/001-rhel-shortnames.conf
    install -m0644 %{SOURCE20} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/002-rhel-shortnames-overrides.conf
%endif

install -dp %{buildroot}%{_sysconfdir}/containers/registries.d
install -m0644 %{SOURCE22} %{buildroot}%{_sysconfdir}/containers/registries.d
install -m0644 %{SOURCE23} %{buildroot}%{_sysconfdir}/containers/registries.d
install -m0644 %{SOURCE24} %{buildroot}%{_sysconfdir}/containers/policy.json
install -dp %{buildroot}%{_sharedstatedir}/containers/sigstore
install -m0644 %{SOURCE25} %{buildroot}%{_sysconfdir}/containers/registries.d/default.yaml

# for containers-common
install -dp %{buildroot}%{_mandir}/man5
go-md2man -in %{SOURCE2} -out %{buildroot}%{_mandir}/man5/containers-storage.conf.5
go-md2man -in %{SOURCE4} -out %{buildroot}%{_mandir}/man5/containers-registries.conf.5
go-md2man -in %{SOURCE6} -out %{buildroot}%{_mandir}/man5/containers-policy.json.5
go-md2man -in %{SOURCE8} -out %{buildroot}%{_mandir}/man5/containers-mounts.conf.5
go-md2man -in %{SOURCE9} -out %{buildroot}%{_mandir}/man5/containers-signature.5
go-md2man -in %{SOURCE10} -out %{buildroot}%{_mandir}/man5/containers-transports.5
go-md2man -in %{SOURCE11} -out %{buildroot}%{_mandir}/man5/containers-certs.d.5
go-md2man -in %{SOURCE12} -out %{buildroot}%{_mandir}/man5/containers-registries.d.5
go-md2man -in %{SOURCE14} -out %{buildroot}%{_mandir}/man5/containers.conf.5
go-md2man -in %{SOURCE15} -out %{buildroot}%{_mandir}/man5/containers-auth.json.5
go-md2man -in %{SOURCE16} -out %{buildroot}%{_mandir}/man5/containers-registries.conf.d.5
go-md2man -in %{SOURCE18} -out %{buildroot}%{_mandir}/man5/oci-hooks.5
go-md2man -in %{SOURCE26} -out %{buildroot}%{_mandir}/man5/Containerfile.5
go-md2man -in %{SOURCE27} -out %{buildroot}%{_mandir}/man5/containerignore.5
ln -s containerignore.5 %{buildroot}%{_mandir}/man5/.containerignore.5

install -dp %{buildroot}%{_datadir}/containers
install -m0644 %{SOURCE3} %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 %{SOURCE7} %{buildroot}%{_datadir}/containers/seccomp.json
install -m0644 %{SOURCE13} %{buildroot}%{_datadir}/containers/containers.conf

# for signature verification
%if 0%{?fedora} || 0%{?centos}
install -dp %{buildroot}%{_sysconfdir}/pki/sigstore
install -m0644 %{SOURCE29} %{buildroot}%{_sysconfdir}/pki/sigstore
install -m0644 %{SOURCE30} %{buildroot}%{_sysconfdir}/pki/sigstore
%endif

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s ../../../..%{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s ../../../..%{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s ../../../..%{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/redhat.repo

# Placeholder check to silence rpmlint
%check

%files
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%dir %{_sysconfdir}/containers/registries.d
%dir %{_sysconfdir}/containers/systemd
%dir %{_prefix}/lib/containers
%dir %{_prefix}/lib/containers/storage
%dir %{_prefix}/lib/containers/storage/overlay-images
%dir %{_prefix}/lib/containers/storage/overlay-layers
%{_prefix}/lib/containers/storage/overlay-images/images.lock
%{_prefix}/lib/containers/storage/overlay-layers/layers.lock

%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/*.conf
%if 0%{?fedora} || 0%{?centos}
%{_sysconfdir}/pki/sigstore/REKOR-signing-key
%{_sysconfdir}/pki/sigstore/SIGSTORE-redhat-release3
%endif
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%config(noreplace) %{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
%config(noreplace) %{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
%ghost %{_sysconfdir}/containers/storage.conf
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%{_mandir}/man5/.*.5.gz
%{_mandir}/man5/*.5.gz
%dir %{_datadir}/containers
%dir %{_datadir}/containers/systemd
%{_datadir}/containers/storage.conf
%{_datadir}/containers/containers.conf
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%dir %{_datadir}/rhel
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%files extra

%changelog
* Mon Aug 18 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.64.0-4
- update vendored components for 10.1
- Related: RHEL-80817

* Tue Aug 12 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.63.1-3
- remove the ugly installation hack in tests
- Related: RHEL-80817

* Mon Aug 11 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.63.1-2
- update shortnames from Pyxis
- Related: RHEL-80817

* Wed Jun 11 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.63.0-1
- update vendored components
- Related: RHEL-80817

* Sun Jun 08 2025 Lokesh Mandvekar <lsm5@redhat.com> - 5:0.62.0-2
- fetch TMT podman revdep tests from podman dist-git
- needs at least podman 5.4.0-7.el10
- Related: RHEL-80817

* Thu Feb 13 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.62.0-1
- update vendored components
- Related: RHEL-58990

* Thu Feb 06 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.61.0-5
- Be sure log-driver is the podman default, not k8s-file
- Resolves: RHEL-78154

* Thu Feb 06 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.61.0-4
- Update shortnames from Pyxis
- Resolves: RHEL-66760

* Tue Jan 28 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.61.0-3
- ship RHEL shortnames only in RHEL (thanks to Dennis Gilmore)
- Resolves: RHEL-75943

* Wed Jan 15 2025 Jindrich Novy <jnovy@redhat.com> - 5:0.61.0-2
- Add missing oci-hooks.5 man page
- Related: RHEL-58990

* Mon Dec 16 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.61.0-1
- make spec file compatible with RHEL
- update vendored components
- Resolves: RHEL-69842

* Tue Nov 26 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-13
- update vendored components
- Related: RHEL-58990

* Mon Nov 25 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-12
- Use proper log_driver: k8s-file
- Resolves: RHEL-68081

* Thu Oct 31 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-11
- Install shortnames from Pyxis and overrides
- Resolves: RHEL-34940

* Wed Oct 30 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-10
- don't use registry yaml files from upstream but RHEL10 dedicated ones
- Resolves: RHEL-65203

* Wed Oct 30 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-9
- ensure required configurations for RHEL10 is present
- Resolves: RHEL-58990

* Tue Oct 29 2024 Troy Dawson <tdawson@redhat.com> - 5:0.60.2-8
- Bump release for October 2024 mass rebuild:
  Resolves: RHEL-64018

* Tue Oct 29 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-7
- Enable sigstore support
- Resolves: RUN-2164

* Tue Sep 10 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-6
- package GPG keys only on Fedora and CentOS
- Related: RHEL-39410

* Mon Sep 09 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-5
- include relevant GPG keys
- Resolves: RHEL-57720

* Thu Sep 05 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-4
- update update.sh script and set logdriver to file
- Resolves: RHEL-57101

* Wed Aug 28 2024 Jindrich Novy <jnovy@redhat.com> - 5:0.60.2-3
- Obsolete containernetworking-plugins
- Resolves: RHEL-39410
