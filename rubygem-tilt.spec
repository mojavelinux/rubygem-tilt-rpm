%global gem_name tilt

%global rubyabi 1.9.1
%global bootstrap 0

Summary: Generic interface to multiple Ruby template engines
Name: rubygem-%{gem_name}
Version: 1.3.3
Release: 6%{?dist}
Group: Development/Languages
License: MIT
URL: http://github.com/rtomayko/%{gem_name}
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# Fixes RDoc >= 3.10 compatibility.
# https://github.com/rtomayko/tilt/commit/ecdf14893b40cc1bc21aaedca9578d36d264f89e
Patch0: tilt-1.3.3-rdoc-3.10-autoloads-everything-so-you-_have_-to-requ.patch
# https://github.com/rtomayko/tilt/commit/ff097e8722056dfef6ac4523d406bdbca6eae87d
Patch1: tilt-1.3.3-adjusted-specs-to-RDoc-3.10-which-outputs-header-ids.patch

# Fix for redcarpet test failures.
# https://github.com/rtomayko/tilt/commit/87f0358d7e9968c55a28356e2a221d938fc51775
Patch2: tilt-1.3.3-Redcarpet2-as-default.patch

# coffee-script test fixes.
# https://github.com/rtomayko/tilt/commit/173ade03fb72ade7f3aed948e104e26de043f6cf
Patch3: tilt-1.3.3-ensure-coffee-script-test-examples-force-a-closure.patch

Requires: ruby(abi) = %{rubyabi}
Requires: ruby(rubygems)
Requires: ruby
BuildRequires: ruby(abi) = %{rubyabi}
BuildRequires: rubygems-devel
BuildRequires: ruby
%if 0%{bootstrap} < 1
BuildRequires: rubygem(rdoc)
BuildRequires: rubygem(minitest)
BuildRequires: rubygem(nokogiri)
BuildRequires: rubygem(erubis)
BuildRequires: rubygem(haml)
BuildRequires: rubygem(builder)
BuildRequires: rubygem(RedCloth)
BuildRequires: rubygem(redcarpet)
BuildRequires: rubygem(coffee-script)
BuildRequires: rubygem(therubyracer)

# Markaby test fails. It is probably due to rather old version found in Fedora.
# https://github.com/rtomayko/tilt/issues/96
# BuildRequires: rubygem(markaby)

# RDiscount test fails. Is it due to old version in Fedora?
# BuildRequires: rubygem(rdiscount)
%endif

BuildArch: noarch
Provides: rubygem(%{gem_name}) = %{version}

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
mkdir -p .%{gem_dir}
gem install --local --install-dir .%{gem_dir} \
            --bindir .%{_bindir} \
            --force %{SOURCE0}

pushd .%{gem_instdir}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
popd

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}%{_bindir}
cp -a .%{_bindir}/* \
        %{buildroot}%{_bindir}/

find %{buildroot}%{gem_instdir}/bin -type f | xargs chmod a+x

%check
%if 0%{bootstrap} < 1
pushd %{buildroot}%{gem_instdir}
LANG=en_US.utf8 testrb -Ilib test/*_test.rb
popd
%endif

%files
%{_bindir}/%{gem_name}
%exclude %{gem_instdir}/%{gem_name}.gemspec
%if "%{bootstrap}" == "0"
%exclude %{gem_instdir}/.sass-cache
%exclude %{gem_instdir}/.yardoc
%endif
%exclude %{gem_instdir}/Gemfile
%{gem_instdir}/bin
%{gem_libdir}
%doc %{gem_instdir}/COPYING
%doc %{gem_instdir}/README.md
%doc %{gem_instdir}/TEMPLATES.md
%{gem_cache}
%{gem_spec}

%files doc
%{gem_instdir}/Rakefile
%doc %{gem_docdir}
%{gem_instdir}/test


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Jul 23 2012 Vít Ondruch <vondruch@redhat.com> - 1.3.3-5
- Fixes RDoc >= 3.10 compatibility.
- Enabled coffee-script and redcarpet tests.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 03 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-3
- Allowed running the tests.

* Tue Jan 24 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-2
- Rebuilt for Ruby 1.9.3.
- Introduced %%bootstrap macro to deal with dependency loop for BuildRequires.

* Mon Jan 16 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.3.3-1
- Updated to tilt 1.3.3.
- Removed patch that fixed BZ #715713, as it is a part of this version.
- Excluded unnecessary files.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Vít Ondruch <vondruch@redhat.com> - 1.3.2-1
- Updated to the tilt 1.3.2.
- Test suite for erubis, haml, builder and RedCloth template engines enabled.

* Fri Jun 24 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-3
- Fixes FTBFS (rhbz#715713).

* Thu Feb 10 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-2
- Test moved to doc subpackage
- %%{gem_name} macro used whenever possible.

* Mon Feb 07 2011 Vít Ondruch <vondruch@redhat.com> - 1.2.2-1
- Initial package
