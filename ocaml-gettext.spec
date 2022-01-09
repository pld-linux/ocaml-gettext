#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} %{arm} aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

Summary:	OCaml gettext library
Summary(pl.UTF-8):	Biblioteka gettext dla OCamla
Name:		ocaml-gettext
Version:	0.4.2
Release:	3
License:	LGPL v2 with linking exception
Group:		Libraries
#Source0Download: https://github.com/gildor478/ocaml-gettext/releases
Source0:	https://github.com/gildor478/ocaml-gettext/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	d277c08ceab22404f01fbdbc74d5c747
URL:		https://github.com/gildor478/ocaml-gettext
BuildRequires:	cppo >= 1.4.0
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	ocaml >= 1:4.03.0
BuildRequires:	ocaml-camomile-devel
BuildRequires:	ocaml-dune-devel >= 1.11.0
BuildRequires:	ocaml-fileutils-devel
BuildRequires:	ocaml-findlib
%requires_eq	ocaml-runtime
Requires:	ocaml-camomile
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{without ocaml_opt}
%define		no_install_post_strip	1
# no opt means no native binary, stripping bytecode breaks such programs
%define		_enable_debug_packages	0
%endif

%description
This library is a wrapper around gettext, it also provides a pure
OCaml implementation based on camomile.

This package contains files needed to run bytecode executables using
gettext library.

%description -l pl.UTF-8
Ta biblioteka jest obudowaniem gettexta; zawiera także czysto ocamlową
implementację opartą na camomile.

Pakiet ten zawiera binaria potrzebne do uruchamiania programów
używających biblioteki gettext.

%package devel
Summary:	OCaml gettext library - development part
Summary(pl.UTF-8):	Biblioteka gettext dla OCamla - część programistyczna
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
%requires_eq	ocaml

%description devel
This package contains files needed to develop OCaml programs using
gettext library.

%description devel -l pl.UTF-8
Pakiet ten zawiera pliki niezbędne do tworzenia programów w OCamlu
używających biblioteki gettext.

%prep
%setup -q

%build
dune build --verbose

%install
rm -rf $RPM_BUILD_ROOT

dune install --destdir=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# sources
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext/{base,extension}/*.ml
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext-{camomile,stub}/*.ml
# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_prefix}/doc/{gettext,gettext-camomile,gettext-stub}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CHANGES.md LICENSE.txt README.md THANKS TODO.md
%dir %{_libdir}/ocaml/gettext
%{_libdir}/ocaml/gettext/META
%{_libdir}/ocaml/gettext/*.cma
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllgettextStub_stubs.so
%dir %{_libdir}/ocaml/gettext-camomile
%{_libdir}/ocaml/gettext-camomile/META
%{_libdir}/ocaml/gettext-camomile/*.cma
%dir %{_libdir}/ocaml/gettext-stub
%{_libdir}/ocaml/gettext-stub/META
%{_libdir}/ocaml/gettext-stub/*.cma
%dir %{_libdir}/ocaml/gettext/base
%{_libdir}/ocaml/gettext/base/*.cma
%dir %{_libdir}/ocaml/gettext/extension
%{_libdir}/ocaml/gettext/extension/*.cma
%if %{with ocaml_opt}
%attr(755,root,root) %{_libdir}/ocaml/gettext/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/gettext/base/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/gettext/extension/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/gettext-camomile/*.cmxs
%attr(755,root,root) %{_libdir}/ocaml/gettext-stub/*.cmxs
%endif

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/ocaml-gettext
%attr(755,root,root) %{_bindir}/ocaml-xgettext
%{_libdir}/ocaml/gettext/base/*.cmi
%{_libdir}/ocaml/gettext/base/*.cmt
%{_libdir}/ocaml/gettext/base/*.cmti
%{_libdir}/ocaml/gettext/base/*.mli
%{_libdir}/ocaml/gettext/base/.private
%{_libdir}/ocaml/gettext/extension/*.cmi
%{_libdir}/ocaml/gettext/extension/*.cmt
%{_libdir}/ocaml/gettext/extension/*.mli
%{_libdir}/ocaml/gettext/extension/.private
%{_libdir}/ocaml/gettext-camomile/*.cmi
%{_libdir}/ocaml/gettext-camomile/*.cmt
%{_libdir}/ocaml/gettext-camomile/*.cmti
%{_libdir}/ocaml/gettext-camomile/*.mli
%{_libdir}/ocaml/gettext-camomile/dune-package
%{_libdir}/ocaml/gettext-camomile/opam
%{_libdir}/ocaml/gettext-stub/*.cmt
%{_libdir}/ocaml/gettext-stub/dune-package
%{_libdir}/ocaml/gettext-stub/opam
%dir %{_libdir}/ocaml/gettext-stub
%{_libdir}/ocaml/gettext-stub/*.cmi
%{_libdir}/ocaml/gettext-stub/libgettextStub_stubs.a
%if %{with ocaml_opt}
%{_libdir}/ocaml/gettext/base/*.a
%{_libdir}/ocaml/gettext/base/*.cmx
%{_libdir}/ocaml/gettext/base/*.cmxa
%{_libdir}/ocaml/gettext-camomile/*.a
%{_libdir}/ocaml/gettext-camomile/*.cmx
%{_libdir}/ocaml/gettext-camomile/*.cmxa
%{_libdir}/ocaml/gettext/*.cmxa
%{_libdir}/ocaml/gettext/extension/*.a
%{_libdir}/ocaml/gettext/extension/*.cmx
%{_libdir}/ocaml/gettext/extension/*.cmxa
%{_libdir}/ocaml/gettext-stub/gettextStub.a
%{_libdir}/ocaml/gettext-stub/*.cmx
%{_libdir}/ocaml/gettext-stub/*.cmxa
%endif
%{_libdir}/ocaml/gettext/dune-package
%{_libdir}/ocaml/gettext/opam
%{_examplesdir}/%{name}-%{version}
%{_mandir}/man1/ocaml-gettext.1*
%{_mandir}/man1/ocaml-xgettext.1*
%{_mandir}/man5/ocaml-gettext.5*
