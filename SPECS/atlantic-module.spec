%define module_dir extra

Summary: Driver for Atlantic aQuantia AQtion aQuantia Multi-Gigabit PCI Express Family of Ethernet Adapters
Name: atlantic-module-alt
Version: 2.5.6
Release: 1%{?dist}
License: GPL

#Source taken from https://www.marvel.com/content/dam/marvell/en/drivers/marvel_linux_2.5.6.zip
Source: %{name}-%{version}.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
Driver for Atlantic aQuantia AQtion aQuantia Multi-Gigabit PCI Express Family of Ethernet Adapters

%prep
%autosetup -n %{name}-%{version}

%build
%{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) modules

%install
%{__make} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# remove extra files modules_install copies in
rm -f %{buildroot}/lib/modules/%{kernel_version}/modules.*

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%changelog
* Sat Aug 16 2023 Andrew Lindh <andrew@netplex.net> - 2.5.6-1
- Update vendor version of driver 2.5.6

* Fri Feb 17 2023 Andrew Lindh <andrew@netplex.net> - 2.5.5-1
- Release test version of driver 2.5.5
