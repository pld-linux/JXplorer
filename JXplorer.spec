%include	/usr/lib/rpm/macros.java
Summary:	LDAP browser
Summary(pl.UTF-8):	Przeglądarka LDAP
Name:		JXplorer
Version:	3.2
Release:	1
License:	Computer Associates Open Source Software License
Group:		Applications/Databases/Interfaces
Source0:	http://dl.sourceforge.net/jxplorer/JXv%{version}deploy.tar.bz2
# Source0-md5:	5cd9766391995736164b17a30354d72e
Source1:	http://dl.sourceforge.net/jxplorer/JXv%{version}src.tar.bz2
# Source1-md5:	7773a4de17a935db2aaaf3984772fcb1
Source2:	%{name}.sh
Source3:	%{name}.jxconfig.txt
Source4:	%{name}.desktop
Patch0:		%{name}-NoInstallAnywhere.patch
URL:		http://www.jxplorer.org/
BuildRequires:	ant
BuildRequires:	icoutils
BuildRequires:	jar
BuildRequires:	jpackage-utils
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
BuildRequires:	sed >= 4.0
Requires:	java-help
Requires:	jpackage-utils
Requires:	jre-X11
Requires:	junit
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
JXplorer is a standards compliant general purpose LDAP browser that
can be used to read and search any LDAP directory, or any X.500
directory with an LDAP interface. It is available for immediate free
download under a standard OSI-style open source licence.

%description -l pl.UTF-8
JXplorer jest zgodną ze standardami przeglądarką LDAP ogólnego
przeznaczenia. Programu tego można używać do przeglądania i
modyfikowania dowolnego katalogu LDAP, lub dowolnego katalogu zgodnego
z X.500 posiadającego interfejs LDAP.

%prep
%setup -q -b 1 -n jxplorer

%{__sed} -i -e 's,\r$,,' build.xml

icotool -x -o jxplorer.png jxplorer.ico

%patch0 -p0

install %{SOURCE2} jxplorer.sh
install %{SOURCE3} jxconfig.txt
%{__sed} -i -e 's~==DATADIR==~%{_datadir}/%{name}~g' jxconfig.txt

echo 'JX_JAVADIR=%{_javadir}/%{name}' > jxplorer.sysconfig
echo 'JX_DATADIR=%{_datadir}/%{name}' >> jxplorer.sysconfig

%build
export JAVA_HOME="%{java_home}"

export LC_ALL=en_US # source code not US-ASCII

%ant clean
%ant
%ant jar

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/sysconfig
install jxplorer.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/jxplorer
install -d $RPM_BUILD_ROOT%{_bindir}
install jxplorer.sh $RPM_BUILD_ROOT%{_bindir}/jxplorer

install -d $RPM_BUILD_ROOT%{_javadir}/%{name}
install jxplorer.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jxplorer-%{version}.jar
install jars/help.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/help-%{version}.jar
ln -s jxplorer-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/jxplorer.jar
ln -s help-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/help.jar

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/{htmldocs,icons,images,language,security,conftemplate}
install htmldocs/* $RPM_BUILD_ROOT%{_datadir}/%{name}/htmldocs
install icons/* $RPM_BUILD_ROOT%{_datadir}/%{name}/icons
install images/* $RPM_BUILD_ROOT%{_datadir}/%{name}/images
install language/* $RPM_BUILD_ROOT%{_datadir}/%{name}/language
install security/* $RPM_BUILD_ROOT%{_datadir}/%{name}/security
install connections.txt $RPM_BUILD_ROOT%{_datadir}/%{name}/conftemplate

install -d $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/{country,images,inetOrgPerson,locality,newPilotPerson,organization,organizationalPerson,organizationalUnit,person,schema}
install templates/country/*              $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/country
install templates/images/*               $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/images
install templates/inetOrgPerson/*        $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/inetOrgPerson
install templates/locality/*             $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/locality
install templates/newPilotPerson/*       $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/newPilotPerson
install templates/organization/*         $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/organization
install templates/organizationalPerson/* $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/organizationalPerson
install templates/organizationalUnit/*   $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/organizationalUnit
install templates/person/*               $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/person
install templates/schema/*               $RPM_BUILD_ROOT%{_datadir}/%{name}/templates/schema
install templates/*.*			 $RPM_BUILD_ROOT%{_datadir}/%{name}/templates

install -d $RPM_BUILD_ROOT%{_sysconfdir}/%{name}
install log4j.xml $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/log4j.xml
install jxconfig.txt $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/jxconfig.txt
install connections.txt $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/connections.txt

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir}}
install %{SOURCE4} $RPM_BUILD_ROOT%{_desktopdir}/jxplorer.desktop
install jxplorer.png $RPM_BUILD_ROOT%{_pixmapsdir}/jxplorer.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc RELEASE.TXT example.ldif licence.txt
%attr(755,root,root) %{_bindir}/jxplorer
%{_javadir}/%{name}
%{_datadir}/%{name}
%{_pixmapsdir}/jxplorer.png
%{_desktopdir}/jxplorer.desktop
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/connections.txt
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/log4j.xml
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/jxconfig.txt
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/jxplorer
