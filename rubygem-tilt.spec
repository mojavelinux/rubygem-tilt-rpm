%global gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null)
%global gemname tilt
%global geminstdir %{gemdir}/gems/%{gemname}-%{version}
%global rubyabi 1.8

Summary: Generic interface to multiple Ruby template engines
Name: rubygem-%{gemname}
Version: 1.2.2
Release: 3%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/rtomayko/%{gemname}
Source0: http://rubygems.org/gems/%{gemname}-%{version}.gem
# Fixes rhbz#715713
# https://github.com/rtomayko/tilt/issues/93
Patch0: Fix-compilesite-test-for-multiple-threads.patch
Requires: ruby(abi) = %{rubyabi}
Requires: rubygems
Requires: ruby
BuildRequires: rubygems
BuildRequires: ruby
BuildArch: noarch
Provides: rubygem(%{gemname}) = %{version}

%description
Generic interface to multiple Ruby template engines


%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%prep
%setup -q -c -T
mkdir -p .%{gemdir}
gem install --local --install-dir .%{gemdir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}

pushd .%{geminstdir}
%patch0 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gemdir}
cp -a .%{gemdir}/* \
        %{buildroot}%{gemdir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{geminstdir}/bin -type f | xargs chmod a+x

%check
pushd %{buildroot}%{geminstdir}
RUBYOPT="Ilib" testrb test/*_test.rb

%files
%defattr(-, root, root, -)
%{_bindir}/%{gemname}
%{geminstdir}/bin
%{geminstdir}/lib
%doc %{geminstdir}/COPYING
%doc %{geminstdir}/README.md
%doc %{geminstdir}/TEMPLATES.md
%{gemdir}/cache/%{gemname}-%{version}.gem
%{gemdir}/specifications/%{gemname}-%{version}.gemspec

%files doc
%defattr(-, root, root, -)
%{geminstdir}/Rakefile
%{geminstdir}/%{gemname}.gemspec
%doc %{gemdir}/doc/%{gemname}-%{version}
%{geminstdir}/test


%changelog
* Fri Jun 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-3
- Fixes FTBFS (rhbz#715713).

* Thu Feb 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Test moved to doc subpackage
- %{gemname} macro used whenever possible.

* Mon Feb 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Initial package
