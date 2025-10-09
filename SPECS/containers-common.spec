# Bellow definitions are used to deliver config files from a particular branch
# of c/image, c/common, c/storage vendored in all podman, skopeo, buildah.
# These vendored components must have the same version. If it is not the case,
# pick the oldest version on c/image, c/common, c/storage vendored in
# podman/skopeo/podman.
%global skopeo_branch main
%global image_branch v5.19.1
%global common_branch v0.47.4
%global storage_branch v1.38.2
%global shortnames_branch main

Epoch: 2
Name: containers-common
Version: 1
Release: 38%{?dist}
Summary: Common configuration and documentation for containers
License: ASL 2.0
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

# scripts used for synchronization with upstream and shortname generation
Source100: update.sh
Source101: update-vendored.sh
Source102: pyxis.sh

%global aardvark_dns_version v1.0.3
#%%global aardvark_dns_branch v1.0.1-rhel
%global aardvark_dns_commit0 a92337b08fbd88c9eb10c1a5ebce2bf61aa59a7b
%global aardvark_dns_shortcommit0 %(c=%{aardvark_dns_commit0}; echo ${c:0:7})
%if 0%{?aardvark_dns_branch:1}
Source200: https://github.com/containers/aardvark-dns/tarball/%{aardvark_dns_commit0}/%{aardvark_dns_branch}-%{aardvark_dns_shortcommit0}.tar.gz
%else
Source200: https://github.com/containers/aardvark-dns/archive/%{aardvark_dns_commit0}/aardvark-dns-%{aardvark_dns_version}-%{aardvark_dns_shortcommit0}.tar.gz
%endif
Source201: https://github.com/containers/aardvark-dns/releases/download/%{aardvark_dns_version}/aardvark-dns-%{aardvark_dns_version}-vendor.tar.gz

%global netavark_version v1.0.3
#%%global netavark_branch v1.0.1-rhel
%global netavark_commit0 ec7efb85ef90db4a14c07cb003b65491f7eb4edf
%global netavark_shortcommit0 %(c=%{netavark_commit0}; echo ${c:0:7})
%if 0%{?netavark_branch:1}
Source300: https://github.com/containers/netavark/tarball/%{netavark_commit0}/%{netavark_branch}-%{netavark_shortcommit0}.tar.gz
%else
Source300: https://github.com/containers/netavark/archive/%{netavark_commit0}/netavark-%{netavark_version}-%{netavark_shortcommit0}.tar.gz
%endif
Source301: https://github.com/containers/netavark/releases/download/%{netavark_version}/netavark-%{netavark_version}-vendor.tar.gz

%description
This package contains common configuration files and documentation for container
tools ecosystem, such as Podman, Buildah and Skopeo.

It is required because the most of configuration files and docs come from projects
which are vendored into Podman, Buildah, Skopeo, etc. but they are not packaged
separately.

%package -n aardvark-dns
Version: 1.0.1
Release: 38%{?dist}
URL: https://github.com/containers/aardvark-dns
Summary: Authoritative DNS server for A/AAAA container records
License: ASL 2.0 and BSD and MIT
BuildRequires: cargo
BuildRequires: git-core
BuildRequires: make
BuildRequires: rust-srpm-macros
BuildRequires: rust-toolset
#ExclusiveArch: %%{rust_arches}
ExclusiveArch: aarch64 ppc64le s390x x86_64

%description -n aardvark-dns
%{summary}

Forwards other request to configured resolvers.
Read more about configuration in `src/backend/mod.rs`.

%package -n netavark
Version: 1.0.1
Release: 38%{?dist}
URL: https://github.com/containers/netavark
Summary: OCI network stack
License: ASL 2.0 and BSD and MIT
BuildRequires: cargo
BuildRequires: make
BuildRequires: rust-srpm-macros
BuildRequires: git-core
BuildRequires: /usr/bin/go-md2man
Recommends: aardvark-dns
Provides: container-network-stack = 2
BuildRequires: rust-toolset
#ExclusiveArch: #%%{rust_arches}
ExclusiveArch: aarch64 ppc64le s390x x86_64

%description -n netavark
%{summary}

Netavark is a rust based network stack for containers. It is being
designed to work with Podman but is also applicable for other OCI
container management applications.

Netavark is a tool for configuring networking for Linux containers.
Its features include:
* Configuration of container networks via JSON configuration file
* Creation and management of required network interfaces,
    including MACVLAN networks
* All required firewall configuration to perform NAT and port
    forwarding as required for containers
* Support for iptables and firewalld at present, with support
    for nftables planned in a future release
* Support for rootless containers
* Support for IPv4 and IPv6
* Support for container DNS resolution via aardvark-dns.

%prep
tar fx %{SOURCE200}
pushd aardvark-dns-%{aardvark_dns_commit0}
tar fx %{SOURCE201}
mkdir -p .cargo
cat >.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
popd
tar fx %{SOURCE300}
pushd netavark-%{netavark_commit0}
tar fx %{SOURCE301}
mkdir -p .cargo
cat >.cargo/config << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF
popd

%build
%if 0%{?build_rustflags:1}
export RUSTFLAGS="%{build_rustflags}"
%endif

pushd aardvark-dns-%{aardvark_dns_commit0}
%__scm_setup_git -q
%make_build build
popd

pushd netavark-%{netavark_commit0}
%__scm_setup_git -q
%make_build build
pushd docs
go-md2man -in netavark.1.md -out netavark.1
popd
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
popd

%install
pushd aardvark-dns-%{aardvark_dns_commit0}
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
popd

pushd netavark-%{netavark_commit0}
%{__make} DESTDIR=%{buildroot} PREFIX=%{_prefix} install
popd

install -dp %{buildroot}%{_sysconfdir}/containers/{certs.d,oci/hooks.d,registries.d,registries.conf.d}
install -m0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/containers/storage.conf
install -m0644 %{SOURCE5} %{buildroot}%{_sysconfdir}/containers/registries.conf
install -m0644 %{SOURCE17} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/000-shortnames.conf
install -m0644 %{SOURCE19} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/001-rhel-shortnames.conf
install -m0644 %{SOURCE20} %{buildroot}%{_sysconfdir}/containers/registries.conf.d/002-rhel-shortnames-overrides.conf

# for signature verification
%if !0%{?rhel} || 0%{?centos}
install -dp %{buildroot}%{_sysconfdir}/pki/rpm-gpg
install -m0644 %{SOURCE21} %{buildroot}%{_sysconfdir}/pki/rpm-gpg
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
%{_sysconfdir}/containers/registries.d/registry.redhat.io.yaml
%{_sysconfdir}/containers/registries.d/registry.access.redhat.com.yaml
%dir %{_sysconfdir}/containers/oci
%dir %{_sysconfdir}/containers/oci/hooks.d
%dir %{_sysconfdir}/containers/registries.conf.d
%if !0%{?rhel} || 0%{?centos}
%{_sysconfdir}/pki/rpm-gpg/RPM-GPG-KEY-redhat-release
%endif
%config(noreplace) %{_sysconfdir}/containers/policy.json
%config(noreplace) %{_sysconfdir}/containers/registries.d/default.yaml
%config(noreplace) %{_sysconfdir}/containers/storage.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf
%config(noreplace) %{_sysconfdir}/containers/registries.conf.d/*.conf
%config(noreplace) %{_sysconfdir}/containers/registries.d/*.yaml
%ghost %{_sysconfdir}/containers/containers.conf
%dir %{_sharedstatedir}/containers/sigstore
%{_mandir}/man5/*
%dir %{_datadir}/containers
%{_datadir}/containers/mounts.conf
%{_datadir}/containers/seccomp.json
%{_datadir}/containers/containers.conf
%dir %{_datadir}/rhel/secrets
%{_datadir}/rhel/secrets/*

%files -n aardvark-dns
%license aardvark-dns-%{aardvark_dns_commit0}/LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/aardvark-dns

%files -n netavark
%license netavark-%{netavark_commit0}/LICENSE
%dir %{_libexecdir}/podman
%{_libexecdir}/podman/netavark
%{_mandir}/man1/netavark.1*

%changelog
* Tue Mar 14 2023 Jindrich Novy <jnovy@redhat.com> - 2:1-38
- update vendored components and configuration files
- Related: #2176055

* Tue Oct 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-36
- update vendored components and configuration files
- Related: #2129766

* Wed Jul 13 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-35
- update vendored components and configuration files
- Related: #2061390

* Mon Jun 27 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-34
- update shortnames and be sure to remove rhel-els
- Related: #2061390

* Thu Jun 09 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-33
- additional fix for unqualified registries
- Related: #2061390

* Wed May 11 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-26
- update vendored components and configuration files
- Related: #2061390

* Fri Apr 01 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-25
- update vendored components and configuration files
- Related: #2061390

* Mon Feb 28 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-23
- update to netavark and aardvark-dns 1.0.1
- Related: #2001445

* Wed Feb 23 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-22
- build rust packages with RUSTFLAGS set to make ExecShield happy
- bump release tag by 3 for easier cherry-picking from rhel8 stream
- Related: #2001445

* Mon Feb 21 2022 Lokesh Mandvekar <lsm5@redhat.com> - 2:1-19
- do not specify infra_image in containers.conf
- needed to resolve gating test failures
- Related: #2001445

* Fri Feb 18 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-18
- update to netavark-1.0.0 and aardvark-dns-1.0.0
- Related: #2001445

* Thu Feb 10 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-17
- update vendored components and configuration files
- Related: #2001445

* Thu Feb 10 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-16
- sync vendored components
- Related: #2001445

* Thu Feb 10 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-15
- update vendored components and configuration files
- Related: #2001445

* Fri Feb 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-14
- sync vendored components
- Related: #2001445

* Fri Feb 04 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-13
- sync vendored components
- Related: #2001445

* Fri Jan 21 2022 Jindrich Novy <jnovy@redhat.com> - 2:1-12
- update shortnames from Pyxis
- Related: #2001445

* Fri Dec 10 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-11
- do not allow broken content from Pyxis to land in shortnames.conf
- Related: #2001445

* Wed Dec 08 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-10
- sync vendored components
- update shortnames from Pyxis
- Related: #2001445

* Wed Dec 01 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-9
- use log_driver = "journald" and events_logger = "journald" for RHEL9
- Related: #2001445

* Tue Nov 16 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-8
- consume seccomp.json from the oldest vendored version of c/common,
  not main branch
- Related: #2001445

* Mon Nov 15 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-7
- update vendored components
- Related: #2001445

* Wed Oct 13 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-6
- sync vendored components
- Related: #2001445

* Wed Sep 29 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-5
- update to the new vendored components
- Related: #2001445

* Fri Sep 24 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-4
- update to the new vendored components
- Related: #2001445

* Fri Sep 10 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-3
- update to the new vendored components
- Related: #2001445

* Wed Aug 11 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-2
- synchronize config files for RHEL-8.5
- Related: #1934415

* Wed Aug 11 2021 Jindrich Novy <jnovy@redhat.com> - 2:1-1
- initial import
- Related: #1934415
