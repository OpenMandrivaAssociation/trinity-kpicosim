%bcond clang 1

# TDE variables
%define tde_epoch 2
%if "%{?tde_version}" == ""
%define tde_version 14.1.5
%endif
%define pkg_rel 2

%define tde_pkg kpicosim
%define tde_prefix /opt/trinity


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


Source0:		https://mirror.ppa.trinitydesktop.org/trinity/releases/R%{tde_version}/main/applications/development/%{tarball_name}-%{tde_version}%{?preversion:~%{preversion}}.tar.xz

BuildSystem:    cmake

BuildOption:    -DCMAKE_BUILD_TYPE="RelWithDebInfo"
BuildOption:    -DCMAKE_INSTALL_PREFIX=%{tde_prefix}
BuildOption:    -DSHARE_INSTALL_PREFIX=%{tde_prefix}/share
BuildOption:    -DBUILD_ALL=ON
BuildOption:    -DWITH_GCC_VISIBILITY=%{!?with_clang:ON}%{?with_clang:OFF}


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
export PATH="%{tde_prefix}/bin:${PATH}"


%install -a
%find_lang %{tde_pkg}

# Move desktop icon to XDG directory
if [ -d "%{buildroot}%{tde_prefix}/share/applnk" ]; then
  %__mkdir_p %{buildroot}%{tde_prefix}/share/applications/tde
  %__mv "%{buildroot}%{tde_prefix}/share/applnk/Development/kpicosim.desktop" "%{buildroot}%{tde_prefix}/share/applications/tde/%{tde_pkg}.desktop"
  %__rm -r "%{buildroot}%{tde_prefix}/share/applnk"
fi


%files -f %{tde_pkg}.lang
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING README.md
%{tde_prefix}/bin/kpicosim
%{tde_prefix}/share/applications/tde/kpicosim.desktop
%{tde_prefix}/share/apps/katepart/syntax/psm.xml
%{tde_prefix}/share/apps/kpicosim
%{tde_prefix}/share/doc/tde/HTML/en/kpicosim
%{tde_prefix}/share/icons/hicolor/*/apps/kpicosim.png
%{tde_prefix}/share/man/man*/kpicosim.*

