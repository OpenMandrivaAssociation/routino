%define	major 0
%define	libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	Router for OpenStreetMap Data
Name:		routino
Version:	3.3.3
Release:	1
License:	AGPLv3+
URL:		http://www.routino.org/
Source0:	http://www.routino.org/download/routino-%{version}.tgz
# https://github.com/sharkcz/routino/commits/fedora
Patch0:		routino-3.3-fedora.patch
BuildRequires:	pkgconfig(bzip2)
BuildRequires:	pkgconfig(liblzma)
BuildRequires:	pkgconfig(zlib)

Requires:	%{name}-libs = %{version}-%{release}

%description
Routino is a command-line application for finding a route between two points
using the dataset of topographical information collected by OpenStreetMap. It
can be used as a routing tool in Marble.

%files
%{_bindir}/%{name}-*

#--------------------------------------------------------------------

%package %{libname}
Summary:	Routing library for OpenStreetMap Data
Requires:	%{name}-data = %{version}-%{release}

%description %{libname}
The Routino library is a library for finding a route between two points using
the dataset of topographical information collected by OpenStreetMap. It can be
used by applications to embed Routino, as long as the application's license is
compatible with the AGPLv3.

%files %{libname}
%{_libdir}/lib%{name}*.so.*

#--------------------------------------------------------------------

%package data
Summary:	Data files for %{name} and %{name}-libs
BuildArch:	noarch

%description data
This package contains the architecture-independent data files used by %{name}
and %{name}-libs.

%files data
%license agpl-3.0.txt
%{_datadir}/%{name}/

#--------------------------------------------------------------------

%package %{develname}
Summary:	Development files for %{name}-libs
Requires:	%{name}-libs = %{version}-%{release}

%description %{develname}
This package contains the files required to compile applications that use
%{name}-libs.

%files %{develname}
%{_includedir}/%{name}.h
%{_libdir}/lib%{name}*.so

#--------------------------------------------------------------------

%prep
%autosetup -p1

# Get rid of installation documentation which is not applicable to the RPM
rm -f INSTALL*.txt doc/INSTALL*.txt doc/html/installation.html
# The web stuff needs more work to be packaged. The makefiles will copy things
# into the web directory if it's present, so get rid of it now.
rm -rf web
# Upstream builds but does not install extras. Don't waste build time, nor
# bother fixing the parallel make breakage there.
rm -rf extras

#--------------------------------------------------------------------

%package doc
Summary:	Documentation files for %{name} and %{name}-libs
BuildArch:	noarch
Requires:	%{name}-libs = %{version}-%{release}

%description doc
This package contains the architecture-independent documentation files for
%{name} and %{name}-libs.

%files doc
%{_docdir}/%{name}/

#--------------------------------------------------------------------

%build
%set_build_flags
%make_build libdir=%{_libdir} CLANG=1


%install
%make_install libdir=%{_libdir}

