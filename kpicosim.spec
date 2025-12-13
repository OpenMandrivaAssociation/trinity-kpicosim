%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kpicosim
%define tde_prefix /opt/trinity
%define tde_bindir %{tde_prefix}/bin
%define tde_datadir %{tde_prefix}/share
%define tde_docdir %{tde_datadir}/doc
%define tde_includedir %{tde_prefix}/include
%define tde_libdir %{tde_prefix}/%{_lib}
%define tde_mandir %{tde_datadir}/man
%define tde_tdeappdir %{tde_datadir}/applications/tde
%define tde_tdedocdir %{tde_docdir}/tde
%define tde_tdeincludedir %{tde_includedir}/tde
%define tde_tdelibdir %{tde_libdir}/trinity

%undefine __brp_remove_la_files
%define dont_remove_libtool_files 1
%define _disable_rebuild_configure 1

# fixes error: Empty %files file …/debugsourcefiles.list
%define _debugsource_template %{nil}

%define tarball_name %{tde_pkg}-trinity


Name:		trinity-%{tde_pkg}
Epoch:		%{tde_epoch}
Version:	0.6a
Release:	%{?tde_version}_%{?!preversion:%{pkg_rel}}%{?preversion:0_%{preversion}}%{?dist}
Summary:	IDE and simulator for the Xilinx PicoBlaze-3 [Trinity]
Group:		Applications/Utilities
URL:		http://www.trinitydesktop.org

License:	GPLv2+

#Vendor:		Trinity Desktop
#Packager:	Francois Andriot <francois.andriot@free.fr>

Prefix:		%{tde_prefix}

Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/development/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake
BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_SKIP_RPATH=OFF
BuildOption:    -DCMAKE_SKIP_INSTALL_RPATH=OFF
BuildOption:    -DCMAKE_BUILD_WITH_INSTALL_RPATH=ON
BuildOption:    -DCMAKE_INSTALL_RPATH="%{tde_libdir}"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_datadir}
BuildOption:    -DBUILD_ALL=ON


BuildRequires:	trinity-tdelibs-devel >= %{tde_version}
BuildRequires:	trinity-tdebase-devel >= %{tde_version}
BuildRequires:	desktop-file-utils
BuildRequires:	gettext

BuildRequires:	trinity-tde-cmake >= %{tde_version}

%{!?with_clang:BuildRequires:	gcc-c++}

BuildRequires:	pkgconfig
BuildRequires:	fdupes

# IDN support
BuildRequires:	pkgconfig(libidn)

# ACL support
BuildRequires:  pkgconfig(libacl)

# OPENSSL support
BuildRequires:  pkgconfig(openssl)

BuildRequires:  pkgconfig(xrender)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(sm)


%description
kpicosim is a development environment for the Xilinx
PicoBlaze-3 soft-core processor for the TDE Desktop (Linux).
The environment has an editor with syntax highlighting, compiler,
simulator and export functions to VHDL, HEX and MEM files.


%conf -p
unset QTDIR QTINC QTLIB
export PATH="%{tde_bindir}:${PATH}"


%install -a
%find_lang %{tde_pkg}

# Move desktop icon to XDG directory
if [ -d "%{buildroot}%{tde_datadir}/applnk" ]; then
  %__mkdir_p %{buildroot}%{tde_tdeappdir}
  %__mv "%{buildroot}%{tde_datadir}/applnk/Development/kpicosim.desktop" "%{buildroot}%{tde_tdeappdir}/%{tde_pkg}.desktop"
  %__rm -r "%{buildroot}%{tde_datadir}/applnk"
fi


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md
%{tde_bindir}/kpicosim
%{tde_tdeappdir}/kpicosim.desktop
%{tde_datadir}/apps/katepart/syntax/psm.xml
%{tde_datadir}/apps/kpicosim
%{tde_tdedocdir}/HTML/en/kpicosim
%{tde_datadir}/icons/hicolor/*/apps/kpicosim.png
%{tde_mandir}/man*/kpicosim.*

