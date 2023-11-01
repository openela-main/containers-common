# Bellow definitions are used to deliver config files from a particular branch
# of c/image, c/common, c/storage vendored in all podman, skopeo, buildah.
# These vendored components must have the same version. If it is not the case,
# pick the oldest version on c/image, c/common, c/storage vendored in
# podman/skopeo/podman.
%global skopeo_branch main
%global image_branch v5.24.1
%global common_branch v0.51.0
%global storage_branch v1.45.3
%global shortnames_branch main

Epoch: 2
Name: containers-common
Version: 1
Release: 52%{?dist}
Summary: Common configuration and documentation for containers
License: ASL 2.0
ExclusiveArch: %{go_arches}
BuildRequires: /usr/bin/go-md2man
Provides: skopeo-containers = %{epoch}:%{version}-%{release}
Conflicts: %{name} <= 2:1-22
Obsoletes: %{name} <= 2:1-22
Requires: (container-selinux >= 2:2.162.1 if selinux-policy)
Requires: oci-runtime
%if 0%{?rhel} >= 9 || 0%{?fedora}
Requires: crun >= 0.19
%else
Requires: runc
%endif
Requires: system-release
Suggests: subscription-manager
Recommends: fuse-overlayfs
Recommends: slirp4netns
Source1: https://raw.githubusercontent.com/containers/storage/%{storage_branch}/storage.conf
Source2: https://raw.githubusercontent.com/containers/storage/%{storage_branch}/docs/containers-storage.conf.5.md
Source3: mounts.conf
Source4: https://raw.githubusercontent.com/containers/image/%{image_branch}/docs/containers-registries.conf.5.md
#Source5: https://raw.githubusercontent.com/containers/image/%%{image_branch}/registries.conf
Source5: registries.conf
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
Source19: 001-rhel-shortnames-pyxis.conf
Source20: 002-rhel-shortnames-overrides.conf
Source21: RPM-GPG-KEY-redhat-release
Source22: registry.access.redhat.com.yaml
Source23: registry.redhat.io.yaml
#Source24: https://raw.githubusercontent.com/containers/skopeo/%%{skopeo_branch}/default-policy.json
Source24: default-policy.json
Source25: https://raw.githubusercontent.com/containers/skopeo/%{skopeo_branch}/default.yaml
# FIXME: fix the branch once these are available via regular c/common branch
Source26: https://raw.githubusercontent.com/containers/common/main/docs/Containerfile.5.md
Source27: https://raw.githubusercontent.com/containers/common/main/docs/containerignore.5.md
Source28: RPM-GPG-KEY-redhat-beta

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

%prep

%build

%install
install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d,systemd,registries.d,registries.conf.d}
install -dp %{buildroot}%{_datadir}/containers/systemd
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/storage.conf
install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containers/registries.conf
install -m0644 %{SOURCE17} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
install -m0644 %{SOURCE19} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/001-rhel-shortnames.conf
install -m0644 %{SOURCE20} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/002-rhel-shortnames-overrides.conf

# for signature verification
%if !0%{?rhel} || 0%{?centos}
install -dp %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m0644 %{SOURCE21} %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m0644 %{SOURCE28} %{buildroot}%{_sysconfdir}/pki/rpm-gpg
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
go-md2man -in %{SOURCE26} -out %{buildroot}%{_mandir}/man5/Containerfile.5
go-md2man -in %{SOURCE27} -out %{buildroot}%{_mandir}/man5/containerignore.5

install -dp %{buildroot}%{_datadir}/containers
install -m0644 %{SOURCE3} %{buildroot}%{_datadir}/containers/mounts.conf
install -m0644 %{SOURCE7} %{buildroot}%{_datadir}/containers/seccomp.json
install -m0644 %{SOURCE13} %{buildroot}%{_datadir}/containers/containers.conf

# install secrets patch directory
install -d -p -m 755 %{buildroot}/%{_datadir}/rhel/secrets
# rhbz#1110876 - update symlinks for subscription management
ln -s %{_sysconfdir}/pki/entitlement %{buildroot}%{_datadir}/rhel/secrets/etc-pki-entitlement
ln -s %{_sysconfdir}/rhsm %{buildroot}%{_datadir}/rhel/secrets/rhsm
ln -s %{_sysconfdir}/yum.repos.d/redhat.repo %{buildroot}%{_datadir}/rhel/secrets/redhat.repo

# ship preconfigured /etc/containers/registries.d/ files with containers-common - #1903813
cat <<EOF > %{buildroot}%{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
docker:
     registry.access.redhat.com:
         sigstore: https://access.redhat.com/webassets/docker/content/sigstore
EOF

cat <<EOF > %{buildroot}%{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
docker:
     registry.redhat.io:
         sigstore: https://registry.redhat.io/containers/sigstore
EOF

%files
%dir %{_sysconfdir}/containers
%dir %{_sysconfdir}/containers/certs.d
%dir %{_sysconfdir}/containers/registries.d
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%dir %{_sysconfdir}/containers/systemd
%dir %{_datadir}/containers/systemd
%if !0%{?rhel} || 0%{?centos}
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-redhat-beta
%endif
%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/storage.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/*.conf
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%config(noreplace) %{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
%config(noreplace) %{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%{_mandir}/man5/*
%dir %{_datadir}/containers
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%{_datadir}/containers/containers.conf
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%changelog
* Wed Apr 05 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-52
- fix shortnames contained UBI9 links pointing to auth-only registries
- Resolves: #2182314

* Fri Mar 31 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-51
- update vendored components and configuration files
- Resolves: #2182492

* Wed Feb 22 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-50
- improve shortnames generation
- Related: #2124478

* Tue Jan 31 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-49
- add missing systemd directories
- Related: #2124478

* Mon Jan 30 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-48
- update vendored components and configuration files
- Related: #2124478

* Thu Jan 05 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-47
- update vendored components, regenerate pyxis
- Related: #2124478

* Thu Nov 10 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-46
- The NET_RAW capability was required in RHEL8 but no longer required in RHEL9
- Resolves: #2141531

* Fri Oct 21 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-45
- add beta GPG key
- Related: #2124478

* Tue Aug 23 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-44
- exclude non-go arches because of go-md2man
- Related: #2061316

* Tue Aug 23 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-43
- add beta keys to default-policy.json
- Related: #2061316

* Mon Aug 08 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-42
- update shortnames
- Related: #2061316

* Wed Aug 03 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-41
- drop aardvark-dns and netavark - packaged separately
- update vendored components
- Related: #2061316

* Mon Jun 27 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-40
- remove rhel-els and update shortnames
- Related: #2061316

* Tue Jun 14 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-39
- update shortnames
- Related: #2061316

* Thu Jun 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-38
- fix unqualified registries in registries.conf generation code
- Related: #2088139

* Mon May 23 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-37
- update unqualified registries list
- Related: #2088139

* Mon May 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-36
- update aardvark-dns and netavark to 1.0.3
- update vendored components
- Related: #2061316

* Wed Apr 20 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-35
- add missing man pages from Fedora
- Related: #2061316

* Wed Apr 06 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-34
- update to netavark and aardvark-dns 1.0.2
- update vendored components
- Related: #2061316

* Mon Mar 21 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-33
- allow consuming aardvark-dns and netavark from upstream branches
- Related: #2061316

* Mon Feb 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-32
- build rust packages with RUSTFLAGS set to make ExecShield happy (Lokesh Mandvekar)
- Related: #2000051

* Mon Feb 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-31
- update to netavark and aardvark-dns 1.0.1
- Related: #2000051

* Wed Feb 23 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-30
- archful package should conflict with older noarch package
- Related: #2000051

* Tue Feb 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-29
- consistent release tags for all packages
- Related: #2000051

* Tue Feb 22 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-28
- main package should obsolete noarch versions upto 2:1-22
- Related: #2000051

* Mon Feb 21 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-27
- do not specify infra_image in containers.conf
- needed to resolve gating test failures
- Related: #2000051

* Sat Feb 19 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-26
- aardvark-dns built for same arches as netavark
- Related: #2000051

* Sat Feb 19 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-25
- build netavark only for podman's arches
- i686 can't find go-md2man which causes the build to fail otherwise
- Related: #2000051

* Fri Feb 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-24
- update to netavark-1.0.0 and aardvark-dns-1.0.0
- Related: #2000051

* Thu Feb 17 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-23
- package aarvark-dns and netavark as part of the containers-common
- Related: #2000051

* Thu Feb 17 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-22
- update shortnames and vendored components
- Related: #2000051

* Wed Feb 16 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-21
- containers.conf should contain network_backend = "cni" in RHEL8.6
- Related: #2000051

* Wed Feb 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-20
- update shortname aliases from upstream
- Related: #2000051

* Fri Feb 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-19
- sync vendored components
- Related: #2000051

* Fri Feb 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-18
- sync vendored components
- Related: #2000051

* Mon Jan 17 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-17
- sync shortname aliases via Pyxis
- Related: #2000051

* Fri Dec 10 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-16
- do not hardcode log_driver = "journald" and events_logger = "journald"
  for RHEL9 and leave the rootful/rootless behaviour change based on
  internal logic
- Related: #2000051

* Thu Dec 09 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-15
- do not allow broken content from Pyxis to land in shortnames.conf
- Related: #2000051

* Wed Dec 08 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-14
- update vendored component versions
- sync shortname aliases via Pyxis
- Related: #2000051

* Tue Nov 30 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-13
- use log_driver = "journald" and events_logger = "journald" for RHEL9
- Related: #2000051

* Tue Nov 16 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-12
- consume seccomp.json from the oldest vendored version of c/common,
  not main branch
- Related: #2000051

* Fri Nov 12 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-11
- use ubi8/pause as ubi9/pause is not available yet
- Related: #2000051

* Wed Nov 10 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-10
- update vendored components
- Related: #2000051

* Tue Nov 02 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-9
- make log_driver = "k8s-file" default in containers.conf
- Related: #2000051

* Fri Oct 01 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-8
- perform only sanity/installability tests for now
- Related: #2000051

* Wed Sep 29 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-7
- update to the new vendored components
- Related: #2000051

* Wed Sep 29 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-6
- add gating.yaml
- Related: #2000051

* Fri Sep 24 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-5
- update to the new vendored components
- Related: #2000051

* Fri Sep 10 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-4
- fix updating scripts
- Related: #2000051

* Thu Sep 09 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-3
- update to the new vendored components
- Related: #2000051

* Fri Aug 20 2021 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1-2
- bump configs to latest versions
- replace ubi9 references with ubi8
- Related: #1970747

* Wed Aug 11 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-1
- initial import
- Related: #1970747
