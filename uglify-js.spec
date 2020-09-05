%{?nodejs_find_provides_and_requires}
%global enable_tests 1
%global installdir  %{_jsdir}
Name:                uglify-js
Version:             2.8.22
Release:             1
Summary:             JavaScript parser, mangler/compressor and beautifier toolkit
License:             BSD
URL:                 https://github.com/mishoo/UglifyJS2
Source0:             https://github.com/mishoo/UglifyJS2/archive/v%{version}/uglify-js-%{version}.tar.gz
Patch0:              uglify-js-esfuzz.patch
BuildArch:           noarch
ExclusiveArch:       %{nodejs_arches} noarch
Provides:            nodejs-uglify-js = %{version}-%{release}
BuildRequires:       nodejs-packaging
BuildRequires:       web-assets-devel
%if 0%{?enable_tests}
BuildRequires:       npm(acorn) npm(async) npm(mocha) npm(optimist) npm(source-map)
%endif
Requires:            js-uglify = %{version}-%{release}
%description
JavaScript parser, mangler/compressor and beautifier toolkit.
This package ships the uglifyjs command-line tool and a library suitable for
use within Node.js.

%package -n js-uglify
Summary:             JavaScript parser, mangler/compressor and beautifier toolkit - core library
Obsoletes:           uglify-js-common < 2.2.5-4
Provides:            uglify-js-common = %{version}-%{release}
%if 0%{?fedora}
Requires:            web-assets-filesystem
%endif
%description -n js-uglify
JavaScript parser, mangler/compressor and beautifier toolkit.
This package ships a JavaScript library suitable for use by any JavaScript
runtime.

%prep
%autosetup -p 1 -n UglifyJS2-%{version}
%nodejs_fixdep async "^1.5.0"
%nodejs_fixdep yargs "^3.2.1"

%build

%install
rm -rf %buildroot
mkdir -p %{buildroot}%{installdir}/%{name}-2
cp -pr lib/* %{buildroot}%{installdir}/%{name}-2
ln -sf %{name}-2 %{buildroot}%{installdir}/%{name}
mkdir -p %{buildroot}%{_datadir}
ln -sf javascript/%{name} %{buildroot}%{_datadir}/%{name}
mkdir -p %{buildroot}%{nodejs_sitelib}/uglify-js@2
cp -pr bin tools package.json %{buildroot}%{nodejs_sitelib}/uglify-js@2
ln -sf %{installdir}/%{name} %{buildroot}%{nodejs_sitelib}/uglify-js@2/lib
sed -i -e 's|^#! */usr/bin/env node|#!/usr/bin/node|' \
  %{buildroot}%{nodejs_sitelib}/uglify-js@2/bin/*
mkdir -p %{buildroot}%{_bindir}
ln -sf ../lib/node_modules/uglify-js@2/bin/uglifyjs %{buildroot}%{_bindir}/uglifyjs
%nodejs_symlink_deps
ln -sf uglify-js@2 %{buildroot}%{nodejs_sitelib}/uglify-js

%check
%nodejs_symlink_deps --check
%{__nodejs} -e 'require("./")'
%if 0%{?enable_tests}
sed -i '/timeout/ s/5000/10000/' test/mocha/cli.js
sed -i '/timeout/ s/10000/20000/' test/mocha/let.js
sed -i '/timeout/ s/20000/40000/' test/mocha/spidermonkey.js
%__nodejs test/run-tests.js
%endif

%pretrans -p <lua>
st = posix.stat("%{nodejs_sitelib}/uglify-js")
if st and st.type == "directory" then
  os.execute("rm -rf %{nodejs_sitelib}/uglify-js")
end

%pretrans -n js-uglify -p <lua>
st = posix.stat("%{_datadir}/%{name}")
if st and st.type == "directory" then
  os.execute("rm -rf %{_datadir}/%{name}")
end

%files
%{nodejs_sitelib}/uglify-js
%{nodejs_sitelib}/uglify-js@2
%{_bindir}/uglifyjs

%files -n js-uglify
%{installdir}/%{name}-2
%{installdir}/%{name}
%{_datadir}/%{name}
%doc README.md
%license LICENSE

%changelog
* Mon Aug 24 2020 wangyue <wangyue92@huawei.com> - 2.8.22-1
- package init
