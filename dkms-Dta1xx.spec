%define modname Dta1xx
%define version 2.8.0.142
%define release %mkrel 3
%define modversion %{version}-%{release}

Name:     dkms-%{modname}
Version:  %{version}
Release:  %{release}
Summary:  Kernel driver for Dektec Dta1xx
# Actually it's a very permissive license, but it tells the kernel it is GPL
# so let's distribute it as GPLv2
License:  GPLv2
# Extracted from http://www.dektec.com/Products/SDK/LinuxSDK/Downloads/LinuxSDK.zip
# which contains several drivers and some non free libraries
Source0:  %{modname}.tar.gz
Url:      http://www.dektec.com/downloads/Drivers.asp
Group:    Development/Kernel
Requires(post):  dkms
Requires(preun): dkms
Buildroot:  %{_tmppath}/%{modname}-%{version}-%{release}-buildroot
BuildArch: noarch

%description
The Dta1xx driver is a char driver for DekTec's DTA-1XX series of PCI cards.
Currently the driver provides support for the following cards:
 - DTA-100   (DVB-ASI Output Adapter for PCI Bus)
 - DTA-102   (DVB-SPI Output Adapter for PCI Bus)
 - DTA-105   (DVB-ASI Output Adapter for PCI Bus)
 - DTA-107   (QPSK Modulator / Upconverter for PCI Bus)
 - DTA-110   (QAM Modulator / UHF Upconverter for PCI Bus)
 - DTA-110T  (OFDM Modulator / UHF Upconverter for PCI Bus)
 - DTA-112   (QAM Modulator / VHF&UHF Upconverter for PCI Bus)
 - DTA-115   (Multi-Standard Modulator for PCI Bus)
 - DTA-116   (Multi-Standard Modulator with IF and Digital Output for PCI Bus)
 - DTA-120   (DVB-ASI Input Adapter for PCI Bus)
 - DTA-122   (DVB-SPI Input Adapter for PCI Bus)
 - DTA-124   (QUAD ASI/SDI Input Adapter for PCI Bus)
 - DTA-140   (DVB-ASI Input/Output Adapter for PCI Bus)
 - DTA-145   (Multi-Purpose ASI/SDI Adapter for PCI Bus)
 - DTA-160   (Gigabit Ethernet + 3x ASI for PCI Bus)
 - DTA-545   (DVB-ASI  Input/Output Adapter for PC104+)
 - DTA-2144  (Quad ASI/SDI Input/Output Adapter for PCI Express)
 - DTA-2145  (Multi-Purpose ASI/SDI Adapter for PCI Express)
 - DTA-2160  (Gigabit Ethernet + 3x ASI for PCI Express)


 NOTE: The DTA-110T is not supported on 64-bit Linux.


%prep
%setup -q -n %{modname}

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usrsrc}/%{modname}-%{modversion}
cp -a * %{buildroot}%{_usrsrc}/%{modname}-%{modversion}/
cat > %{buildroot}%{_usrsrc}/%{modname}-%{modversion}/dkms.conf <<EOF

PACKAGE_VERSION="%{modversion}"

# Items below here should not have to change with each driver version
PACKAGE_NAME="%{modname}"
CLEAN="make clean"
BUILT_MODULE_NAME[0]="%{modname}"
DEST_MODULE_LOCATION[0]="/kernel/drivers/misc/dektec"
REMAKE_INITRD="no"
AUTOINSTALL="yes"
EOF

%post
dkms add -m %{modname} -v %{modversion} --rpm_safe_upgrade \
&& dkms build -m %{modname} -v %{modversion} --rpm_safe_upgrade \
&& dkms install -m %{modname} -v %{modversion} --rpm_safe_upgrade --force

%preun
dkms remove -m %{modname} -v %{modversion} --rpm_safe_upgrade --all

%clean
rm -rf %buildroot

%files
%defattr(-,root,root)
%doc Readme
/usr/src/%{modname}-%{modversion}

