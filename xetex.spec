Summary:	An extension of TeX (and LaTeX/ConTeXt) with Unicode and OpenType support
Summary(pl.UTF-8):	Rozszerzenie TeXa (i LaTeXa/ConTeXtu) wspierające Unicode i OpenType
Name:		xetex
Version:	0.996
Release:	1
License:	X11 license
Group:		Applications/Publishing/TeX
Source0:	http://scripts.sil.org/svn-view/xetex/TAGS/%{name}-%{version}.tar.gz
# Source0-md5:	2f1f09337e22e0fb42d9caed225d6052
URL:		http://scripts.sil.org/xetex
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	fontconfig-devel >= 1:2.3
BuildRequires:	tetex >= 1:3.0-5
Requires(post,preun,postun):	tetex
Requires:	fontconfig
%requires_eq	tetex
%requires_eq	tetex-latex
Requires:	tetex-fonts-opentype-lmodern
Requires:	xdvipdfmx
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	texmf		%{_datadir}/texmf
%define	texmfvar	/var/lib/texmf

%description
XeTeX extends the TeX typesetting system (and macro packages such as
LaTeX and ConTeXt) to have native support for the Unicode character
set, including complex Asian scripts, and for OpenType and TrueType
fonts.

%description -l pl.UTF-8
XeTeX rozszerza system składu TeX (i systemy makr, takie jak LaTeX
i ConTeXt) o natywne wsparcie zestawu znaków Unicode, w tym alfabety
azjatyckie wymagające specjalnego traktowania, i o fonty OpenType
i TrueType.

%prep
%setup -q

%build
sh ./build-xetex

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_bindir}
install Work/texk/web2c/xetex $RPM_BUILD_ROOT%{_bindir}
ln -s xetex $RPM_BUILD_ROOT%{_bindir}/xelatex

install -d $RPM_BUILD_ROOT%{_datadir}
cp -a texmf $RPM_BUILD_ROOT%{_datadir}

# tetex has a newer version of xkeyval
rm -rf $RPM_BUILD_ROOT%{texmf}/doc/latex/xkeyval
rm -rf $RPM_BUILD_ROOT%{texmf}/tex/xelatex/xkeyval

install -d $RPM_BUILD_ROOT%{texmf}/web2c
install Work/texk/web2c/xetex.pool $RPM_BUILD_ROOT%{texmf}/web2c

cat >fmtutil.cnf <<EOF
xetex	xetex	-	*xetex.ini
xelatex	xetex	language.dat	*xelatex.ini
EOF
cat >language.dat <<EOF
american	ushyph1.tex
=english
ngerman		dehyphn.tex
=naustrian
german		dehypht.tex
=austrian
croatian	hrhyph.tex
% czech		czhyph.tex
danish		dkhyphen.tex
irish		gahyph.tex
magyar		huhyph.tex
polish		plhyph.tex
romanian	rohyphen.tex
russian		ruhyphen.tex
% slovak	skhyph.tex
slovene		sihyph23.tex
turkish		trhyph.tex
% ukrainian	ukrhyph.tex
EOF
PATH=$RPM_BUILD_ROOT%{_bindir}:$PATH \
TEXMFHOME=$RPM_BUILD_ROOT%{texmf} \
TEXMFSYSVAR=$RPM_BUILD_ROOT%{texmfvar} \
TEXMFSYSCONFIG=$RPM_BUILD_ROOT%{texmf} \
fmtutil-sys --cnffile fmtutil.cnf --all

%post
texhash

fmtutil_cnf=`kpsewhich --format="web2c files" fmtutil.cnf`
if ! grep -q xetex $fmtutil_cnf; then
	cat >>$fmtutil_cnf <<-EOF

	# XeTeX formats
	xetex	xetex	-	*xetex.ini
	xelatex	xetex	language.dat	*xelatex.ini

	EOF
fi

for f in xetex xelatex; do
	fmtutil-sys --enablefmt $f
done

%preun
for f in xetex xelatex; do
	[ ! -x %{_bindir}/fmtutil-sys ] || fmtutil-sys --disablefmt $f
done

%postun
[ ! -x %{_bindir}/texhash ] || %{_bindir}/texhash

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/xe*tex
%{texmf}/doc/generic/ifxetex
%{texmf}/doc/xe*tex
%{texmf}/fonts/misc
%{texmf}/scripts/xetex
# tetex doesn't include texmfsrc: %{texmf}/source/xelatex
# conflicts with tetex: %{texmf}/tex/generic/hyphen/*
%{texmf}/tex/generic/ifxetex
%{texmf}/tex/generic/xetex
%{texmf}/tex/xe*tex
%{texmf}/web2c/xetex.pool
%config(noreplace) %verify(not md5 mtime size) %{texmfvar}/web2c/xe*tex.fmt
