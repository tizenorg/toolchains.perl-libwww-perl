Name:       perl-libwww-perl
Summary:    A Perl interface to the World-Wide Web
Version:    5.836
Release:    1
Group:      Development/Libraries
License:    GPL+ or Artistic
BuildArch:  noarch
URL:        http://search.cpan.org/dist/libwww-perl/
Source0:    %{name}-%{version}.tar.bz2
Requires:   perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:   perl(Compress::Zlib)
Requires:   perl-HTML-Parser >= 3.33
BuildRequires:  perl(HTML::Entities)
BuildRequires:  perl(URI)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(Compress::Zlib)

%description
The libwww-perl collection is a set of Perl modules which provides a
simple and consistent application programming interface to the
World-Wide Web.  The main focus of the library is to provide classes
and functions that allow you to write WWW clients. The library also
contain modules that are of more general use and even classes that
help you implement simple HTTP servers.

%prep
%setup

# Filter the automatically generated dependencies.
%{?filter_setup:
%filter_from_requires /^perl(Win32)/d
%filter_from_requires /^perl(Authen::NTLM)/d
%filter_from_requires /^perl(HTTP::GHTTP)/d
%?perl_default_filter
}

%build

if test -f Makefile.PL; then
%{__perl} Makefile.PL INSTALLDIRS=vendor
#####make %{?jobs:-j%jobs}
make
else
%{__perl} Build.PL  --installdirs vendor
./Build
fi

%install
rm -rf %{buildroot}

# Use system wide MIME types (link also to blib/... for "make test").  Doing
if test -f Makefile.PL; then
make pure_install PERL_INSTALL_ROOT=%{buildroot}
else
./Build install --installdirs vendor
fi
find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
%{_fixperms} %{buildroot}/*

chmod -R u+w $RPM_BUILD_ROOT/*
for file in AUTHORS README Changes; do
iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
mv -f "${file}_" "$file"
done
# but a copy of /etc/mime.types.
for file in {blib/lib,$RPM_BUILD_ROOT%{perl_vendorlib}}/LWP/media.types ; do
[ ! -f $file ] && echo ERROR && exit 1
ln -sf /etc/mime.types $file
done

%check
#make test

%files
%defattr(-,root,root,-)
%doc AUTHORS Changes README*
%{_bindir}/*
%{perl_vendorlib}/lwp*.pod
%{perl_vendorlib}/LWP.pm
%{perl_vendorlib}/Bundle/*
%{perl_vendorlib}/File/*
%{perl_vendorlib}/HTML/*
%{perl_vendorlib}/HTTP/*
%{perl_vendorlib}/LWP/*
%{perl_vendorlib}/Net/*
%{perl_vendorlib}/WWW/*
#%doc %{_mandir}/man1/*.1*
#%doc %{_mandir}/man3/*.3*
