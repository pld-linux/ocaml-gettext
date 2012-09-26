# $Revision: 1.5 $, $Date: 2011/07/23 06:35:45 $
Summary:	OCaml gettext library
Summary(pl.UTF-8):	Biblioteka gettext dla OCamla
Name:		ocaml-gettext
Version:	0.3.4
Release:	1
License:	LGPL v2 with linking exception
Group:		Libraries
Source0:	http://forge.ocamlcore.org/frs/download.php/676/%{name}-%{version}.tar.gz
# Source0-md5:	2c588ba92e9a809f2885ecacc48069a9
URL:		http://forge.ocamlcore.org/projects/ocaml-gettext
BuildRequires:	docbook-dtd43-xml
BuildRequires:	docbook-style-xsl
BuildRequires:	libxml2-progs
BuildRequires:	libxslt-progs
BuildRequires:	ocaml >= 3.04-7
BuildRequires:	ocaml-camlp4
BuildRequires:	ocaml-camomile-devel
BuildRequires:	ocaml-fileutils
BuildRequires:	ocaml-ounit
%requires_eq	ocaml-runtime
Requires:	ocaml-camomile
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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
Summary(pl.UTF-8):	Biblioteka gettext dla OCamla - cześć programistyczna
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
%configure \
	--with-docbook-stylesheet=/usr/share/sgml/docbook/xsl-stylesheets

# build is racy
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/{site-lib/{gettext,gettext-camomile,gettext-stub},stublibs}

%{__make} -j1 install \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	DOCDIR=$(pwd)/built-docs \
	MANDIR=$RPM_BUILD_ROOT%{_mandir} \
	OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml \
	PODIR=$RPM_BUILD_ROOT%{_localedir}

#mv -f $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext-stub/dll*.so $RPM_BUILD_ROOT%{_libdir}/ocaml/stublibs
mv -f $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gettext
mv -f $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext-camomile/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gettext-camomile
mv -f $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext-stub/META $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gettext-stub
cat >>$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gettext/META <<EOF
directory="+gettext"
EOF
cat >>$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gettext-camomile/META <<EOF
directory="+gettext-camomile"
EOF
cat >>$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/gettext-stub/META <<EOF
directory="+gettext-stub"
EOF

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -r examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

# packaged as %doc
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext*/*.mli
# why installed?
%{__rm} $RPM_BUILD_ROOT%{_libdir}/ocaml/gettext*/*.ml

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc CHANGELOG README THANKS TODO
%attr(755,root,root) %{_libdir}/ocaml/stublibs/dllgettextStub.so
%{_libdir}/ocaml/stublibs/dllgettextStub.so.owner

%files devel
%defattr(644,root,root,755)
%doc libgettext-ocaml/{gettext,gettextCompat}.mli libgettext-camomile-ocaml/gettextCamomile.mli built-docs/html/*
%attr(755,root,root) %{_bindir}/ocaml-gettext
%attr(755,root,root) %{_bindir}/ocaml-xgettext
%dir %{_libdir}/ocaml/gettext
%{_libdir}/ocaml/gettext/gettextBase.a
%{_libdir}/ocaml/gettext/gettextExtension.a
%{_libdir}/ocaml/gettext/gettext*.cm[ixa]*
%{_libdir}/ocaml/gettext/pr_gettext.cmo
%dir %{_libdir}/ocaml/gettext-camomile
%{_libdir}/ocaml/gettext-camomile/gettextCamomile.a
%{_libdir}/ocaml/gettext-camomile/gettextCamomile.cm[ixa]*
%dir %{_libdir}/ocaml/gettext-stub
%{_libdir}/ocaml/gettext-stub/gettextStub.a
%{_libdir}/ocaml/gettext-stub/gettextStub*.cm[ixa]*
%{_libdir}/ocaml/gettext-stub/gettextStubCompat_stubs.o
%{_libdir}/ocaml/gettext-stub/libgettextStub.a
%{_libdir}/ocaml/site-lib/gettext
%{_libdir}/ocaml/site-lib/gettext-camomile
%{_libdir}/ocaml/site-lib/gettext-stub
%{_examplesdir}/%{name}-%{version}
%{_mandir}/man1/ocaml-gettext.1*
%{_mandir}/man1/ocaml-xgettext.1*
%{_mandir}/man5/ocaml-gettext.5*
