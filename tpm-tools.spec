%global name         tpm-tools
%global version      1.3.4
%global tarballrev   -1
%global release      2

Name: %{name}
Summary: Management tools for the TPM hardware
Version: %{version}
Release: %{release}%{?dist}
License: CPL
Group: Applications/System
URL: http://trousers.sourceforge.net
Source0: http://downloads.sourceforge.net/trousers/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: trousers-devel openssl-devel opencryptoki-devel chrpath

%description
tpm-tools is a group of tools to manage and utilize the Trusted Computing
Group's TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's
software state using cryptographic hashes and more.

%package pkcs11
Summary: Management tools using PKCS#11 for the TPM hardware
Group: Applications/System
# opencryptoki is dlopen'd, the Requires won't get picked up automatically
Requires: opencryptoki-libs%{?_isa}

%description pkcs11
tpm-tools-pkcs11 is a group of tools that use the TPM PKCS#11 token. All data
contained in the PKCS#11 data store is protected by the TPM (keys,
certificates, etc.). You can import keys and certificates, list out the
objects in the data store, and protect data.

%package devel
Summary: Files to use the library routines supplied with tpm-tools
Group: Development/Libraries
Requires: %{name} = %{version}-%{release} 

%description devel
tpm-tools-devel is a package that contains the libraries and headers necessary
for developing tpm-tools applications.

%prep
%setup -q

%build
%configure --disable-rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}

%install
mkdir -p ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
rm -f $RPM_BUILD_ROOT/%{_libdir}/libtpm_unseal.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libtpm_unseal.a
chrpath -d %{buildroot}%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc LICENSE README
%attr(755, root, root) %{_bindir}/tpm_*
%attr(755, root, root) %{_sbindir}/tpm_*
%attr(755, root, root) %{_libdir}/libtpm_unseal.so.?.?.?
%{_libdir}/libtpm_unseal.so.?
%{_mandir}/man1/tpm_*
%{_mandir}/man8/tpm_*

%files pkcs11
%defattr(-,root,root,-)
%attr(755, root, root) %{_bindir}/tpmtoken_*
%{_mandir}/man1/tpmtoken_*

%files devel
%defattr(-,root,root,-)
%{_libdir}/libtpm_unseal.so
%{_includedir}/tpm_tools/
%{_mandir}/man3/tpmUnseal*

%changelog
* Fri Jan 29 2010 Steve Grubb <sgrubb@redhat.com> - 1.3.4-2
- Initial package for RHEL6

* Fri Dec 11 2009 Dennis Gregorovic <dgregor@redhat.com> - 1.3.3-2.1
- Rebuilt for RHEL 6

