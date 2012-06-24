#
# todo:
# - for modularized xorg use /usr/bin/xauth
#
# Conditional build:
%bcond_without	chroot		# without chrooted user environment support
%bcond_with	gnome		# with gnome-askpass (GNOME 1.x) utility
%bcond_without	gtk		# without GTK+ (2.x)
%bcond_with	ldap		# with ldap support
%bcond_without	libedit		# without libedit (editline/history support in sftp client)
%bcond_without	kerberos5	# without kerberos5 support
%bcond_without	selinux		# build without SELinux support
%bcond_with	sshagentsh	# with system-wide script for starting ssh-agent
%bcond_with	hpn		# with High Performance SSH/SCP - HPN-SSH (see patch comment)
%bcond_with	hpn_none	# with hpn (above) and '-z' none cipher option
#
%if %{with hpn_none}
%undefine       with_hpn
%endif
# gtk2-based gnome-askpass means no gnome1-based
%{?with_gtk:%undefine with_gnome}
Summary:	OpenSSH free Secure Shell (SSH) implementation
Summary(de):	OpenSSH - freie Implementation der Secure Shell (SSH)
Summary(es):	Implementaci�n libre de SSH
Summary(fr):	Impl�mentation libre du shell s�curis� OpenSSH (SSH)
Summary(it):	Implementazione gratuita OpenSSH della Secure Shell
Summary(pl):	Publicznie dost�pna implementacja bezpiecznego shella (SSH)
Summary(pt):	Implementa��o livre OpenSSH do protocolo 'Secure Shell' (SSH)
Summary(pt_BR):	Implementa��o livre do SSH
Summary(ru):	OpenSSH - ��������� ���������� ��������� Secure Shell (SSH)
Summary(uk):	OpenSSH - צ���� ���̦��æ� ��������� Secure Shell (SSH)
Name:		openssh
Version:	4.2p1
Release:	5%{?with_hpn:hpn}%{?with_hpn_none:hpn_none}
Epoch:		2
License:	BSD
Group:		Applications/Networking
Source0:	ftp://ftp.ca.openbsd.org/pub/OpenBSD/OpenSSH/portable/%{name}-%{version}.tar.gz
# Source0-md5:	df899194a340c933944b193477c628fa
Source1:	%{name}d.conf
Source2:	%{name}.conf
Source3:	%{name}d.init
Source4:	%{name}d.pamd
Source5:	%{name}.sysconfig
Source6:	passwd.pamd
Source7:	http://www.mif.pg.gda.pl/homepages/ankry/man-PLD/openssh-non-english-man-pages.tar.bz2
# Source7-md5:	66943d481cc422512b537bcc2c7400d1
Source9:	http://www.taiyo.co.jp/~gotoh/ssh/connect.c
# NoSource9-md5:	e1c3cbed88f08ea778d90813d48cd428
Source10:	http://www.taiyo.co.jp/~gotoh/ssh/connect.html
# NoSource10-md5:	ec74f3e3b2ea3a7dc84c7988235b6fcf
Source11:	ssh-agent.sh
Source12:	ssh-agent.conf
Patch0:		%{name}-no_libnsl.patch
Patch2:		%{name}-linux-ipv6.patch
Patch3:		%{name}-pam_misc.patch
Patch4:		%{name}-sigpipe.patch
# http://www.opendarwin.org/projects/openssh-lpk/
Patch5:		%{name}-lpk-4.0p1-0.3.patch
Patch6:		%{name}-heimdal.patch
Patch7:		%{name}-pam-conv.patch
# http://chrootssh.sourceforge.net/download/osshChroot-3.7.1p2.diff
Patch8:		%{name}-chroot.patch
Patch9:		%{name}-selinux.patch
Patch10:	%{name}-selinux-pld.patch
# High Performance SSH/SCP - HPN-SSH - http://www.psc.edu/networking/projects/hpn-ssh/ 
# http://www.psc.edu/networking/projects/hpn-ssh/openssh-4.2p1-hpn11.diff
Patch11:	%{name}-4.2p1-hpn11.patch
# Adds HPN (see p11) and an undocumented -z none cipher flag
# http://www.psc.edu/networking/projects/hpn-ssh/openssh-4.2p1-hpn11-none.diff
Patch12:	%{name}-4.2p1-hpn11-none.patch
Patch13:	%{name}-include.patch
URL:		http://www.openssh.com/
BuildRequires:	autoconf
BuildRequires:	automake
%{?with_gnome:BuildRequires:	gnome-libs-devel}
%{?with_gtk:BuildRequires:	gtk+2-devel}
%{?with_kerberos5:BuildRequires:	heimdal-devel >= 0.7}
%{?with_libedit:BuildRequires:	libedit-devel}
%{?with_selinux:BuildRequires:	libselinux-devel}
BuildRequires:	libwrap-devel
%{?with_ldap:BuildRequires:	openldap-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pam-devel
BuildRequires:	%{__perl}
%{?with_gtk:BuildRequires:	pkgconfig}
BuildRequires:	rpmbuild(macros) >= 1.202
BuildRequires:	zlib-devel
Requires:	FHS >= 2.1-24
Requires:	pam >= 0.79.0
Obsoletes:	ssh
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir	/etc/ssh
%define		_libexecdir	%{_libdir}/%{name}
%define		_privsepdir	/usr/share/empty

%description
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine. It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to seperate libraries (OpenSSL).

This package includes the core files necessary for both the OpenSSH
client and server. To make this package useful, you should also
install openssh-clients, openssh-server, or both.
%if %{with hpn} || %{with hpn_none}
This release includes High Performance SSH/SCP patches from 
http://www.psc.edu/networking/projects/hpn-ssh/ which are supposed 
to increase throughput on fast connections with high RTT (20-150 msec).
See the website for '-w' values for your connection and /proc/sys TCP
values. BTW. in a LAN you have got generally RTT < 1 msec.
%endif
%if %{with hpn_none}
It also includes an undocumented '-z' option which switches
the cipher to none after authentication is completed. Data is 
still secured from tampering and corruption in transit through 
the use of the Message Authentication Code (MAC).
This option will significantly reduce the number of cpu cycles used 
by the SSH/SCP process. This may allow some users to see significant 
improvement in (sniffable) data tranfer rates. 
%endif

%description -l de
OpenSSH (Secure Shell) stellt den Zugang zu anderen Rechnern her. Es
ersetzt telnet, rlogin, rexec und rsh und stellt eine sichere,
verschl�sselte Verbindung zwischen zwei nicht vertrauensw�rdigen Hosts
�ber eine unsicheres Netzwerk her. X11 Verbindungen und beliebige
andere TCP/IP Ports k�nnen ebenso �ber den sicheren Channel
weitergeleitet werden.

%description -l es
SSH es un programa para accesar y ejecutar �rdenes en computadores
remotos. Sustituye rlogin y rsh, y suministra un canal de comunicaci�n
seguro entre dos servidores en una red insegura. Conexiones X11 y
puertas TCP/IP arbitr�rias tambi�n pueden ser usadas por el canal
seguro.

OpenSSH es el resultado del trabajo del equipo de OpenBSD para
continuar la �ltima versi�n gratuita de SSH, actualiz�ndolo en
t�rminos de seguridad y recursos,as� tambi�n eliminando todos los
algoritmos patentados y coloc�ndolos en bibliotecas separadas
(OpenSSL).

Este paquete contiene "port" para Linux de OpenSSH. Se debe instalar
tambi�n el paquete openssh-clients u openssh-server o ambos.

%description -l fr
OpenSSH (Secure Shell) fournit un acc�s � un syst�me distant. Il
remplace telnet, rlogin, rexec et rsh, tout en assurant des
communications crypt�es securis�es entre deux h�tes non fiabilis�s sur
un r�seau non s�curis�. Des connexions X11 et des ports TCP/IP
arbitraires peuvent �galement �tre transmis sur le canal s�curis�.

%description -l it
OpenSSH (Secure Shell) fornisce l'accesso ad un sistema remoto.
Sostituisce telnet, rlogin, rexec, e rsh, e fornisce comunicazioni
sicure e crittate tra due host non fidati su una rete non sicura. Le
connessioni X11 ad una porta TCP/IP arbitraria possono essere
inoltrate attraverso un canale sicuro.

%description -l pl
Ssh (Secure Shell) to program s�u��cy do logowania si� na zdaln�
maszyn� i uruchamiania na niej aplikacji. W zamierzeniu openssh ma
zast�pi� rlogin, rsh i dostarczy� bezpieczne, szyfrowane po��czenie
pomi�dzy dwoma hostami.

Ten pakiet zawiera podstawowe pliki potrzebne zar�wno po stronie
klienta jak i serwera OpenSSH. Aby by� u�yteczny, trzeba zainstalowa�
co najmniej jeden z pakiet�w: openssh-clients lub openssh-server.
%if %{with hpn} || %{with hpn_none}
Ta wersja zawiera �aty z projektu High Performance SSH/SCP 
http://www.psc.edu/networking/projects/hpn-ssh/, kt�re maj� na celu
zwi�kszenie przepustowo�ci transmisji dla szybkich po��cze� 
z du�ym RTT (20-150 msec). Na stronie projektu znale�� mo�na 
odpowednie dla danego po��czenia warto�ci parametru '-w' oraz 
opcje /proc/sys dla TCP. Nawiasem m�wi�c w sieciach LAN RTT < 1 msec.  
%endif
%if %{with hpn_none}
Obs�ugiwana jest r�wnie� nieudokumentowana opcja '-z' odpowiedzialna
za wy��czenie szyfrowania danych po zako�czeniu procesu uwierzytelniania.
Dane s� zabezpieczone przed modyfikacj� lub uszkodzeniem przez 
stosowanie Message Authentication Code (MAC).
Opcja ta znacznie redukuje liczb� cykli procesora zu�ywanych przez 
procesy SSH/SCP. W wybranych zastosowaniach mo�e ona wp�yn�� 
na wyra�ne przyspieszenie (pods�uchiwalnej) transmisji danych. 
%endif

%description -l pt
OpenSSH (Secure Shell) fornece acesso a um sistema remoto. Substitui o
telnet, rlogin, rexec, e o rsh e fornece comunica��es seguras e
cifradas entre duas m�quinas sem confian�a m�tua sobre uma rede
insegura. Liga��es X11 e portos TCP/IP arbitr�rios tamb�m poder ser
reenviados pelo canal seguro.

%description -l pt_BR
SSH � um programa para acessar e executar comandos em m�quinas
remotas. Ele substitui rlogin e rsh, e provem um canal de comunica��o
seguro entre dois hosts em uma rede insegura. Conex�es X11 e portas
TCP/IP arbitr�rias tamb�m podem ser usadas pelo canal seguro.

OpenSSH � o resultado do trabalho da equipe do OpenBSD em continuar a
�ltima vers�o gratuita do SSH, atualizando-o em termos de seguran�a e
recursos, assim como removendo todos os algoritmos patenteados e
colocando-os em bibliotecas separadas (OpenSSL).

Esse pacote cont�m o "port" pra Linux do OpenSSH. Voc� deve instalar
tamb�m ou o pacote openssh-clients, ou o openssh-server, ou ambos.

%description -l ru
Ssh (Secure Shell) - ��� ��������� ��� "������" (login) �� ���������
������ � ��� ���������� ������ �� ��������� ������. ��� �������������
��� ������ rlogin � rsh � ������������ ���������� �����������
������������ ����� ����� ������� � ����, ���������� ������������.
���������� X11 � ����� ����� TCP/IP ����� ����� ���� ��������� �����
���������� �����.

OpenSSH - ��� ��������� �������� ������������� OpenBSD ���������
��������� ������ SSH, ���������� �� ������������ ��������� � ��������
������ ������������ � �������������� ������������. ��� �������������
��������� �������� � ��������� ���������� (OpenSSL).

���� ����� �������� �����, ����������� ��� ��� �������, ��� � ���
������� OpenSSH. ��� ����� ����� ���������� ��� openssh-clients,
openssh-server, ��� ��� ������.

%description -l uk
Ssh (Secure Shell) - �� �������� ��� "������" (login) �� צ������ϧ
������ �� ��� ��������� ������ �� צ�����Φ� ����Φ. ���� ����������
��� ��ͦ�� rlogin �� rsh � ��������դ �������� ��������� ����Φ��æ�
ͦ� ����� ������� � ����֦, ��� �� � ���������. �'������� X11 ��
��צ��Φ ����� TCP/IP ������ ����� ���� �������Φ ����� ���������
�����.

OpenSSH - �� ��������� �������� ��������˦� OpenBSD �������ϧ צ���ϧ
���Ӧ� SSH, �������� �� ��������� ����� � ���ͦ��� Ҧ��� ������� ��
Ц����������� �����������. �Ӧ ���������Φ ��������� ������Φ ��
������� ¦�̦���� (OpenSSL).

��� ����� ͦ����� �����, ����Ȧ�Φ �� ��� �̦����, ��� � ��� �������
OpenSSH. ��� ���Ҧ��� ���� �� ���������� openssh-clients,
openssh-server, �� ������ ������.

%package clients
Summary:	OpenSSH Secure Shell protocol clients
Summary(es):	Clientes de OpenSSH
Summary(pl):	Klienci protoko�u Secure Shell
Summary(pt_BR):	Clientes do OpenSSH
Summary(ru):	OpenSSH - ������� ��������� Secure Shell
Summary(uk):	OpenSSH - �̦���� ��������� Secure Shell
Group:		Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}
%{?with_sshagentsh:Requires:	xinitrc}
Provides:	ssh-clients
Obsoletes:	ssh-clients

%description clients
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine. It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to seperate libraries (OpenSSL).

This package includes the clients necessary to make encrypted
connections to SSH servers.

%description clients -l es
Este paquete incluye los clientes que se necesitan para hacer
conexiones codificadas con servidores SSH.

%description clients -l pl
Ssh (Secure Shell) to program s�u��cy do logowania si� na zdaln�
maszyn� i uruchamiania na niej aplikacji. W zamierzeniu openssh ma
zast�pi� rlogin, rsh i dostarczy� bezpieczne, szyfrowane po��czenie
pomi�dzy dwoma hostami.

Ten pakiet zawiera klient�w s�u��cych do ��czenia si� z serwerami SSH.

%description clients -l pt_BR
Esse pacote inclui os clientes necess�rios para fazer conex�es
encriptadas com servidores SSH.

%description clients -l ru
Ssh (Secure Shell) - ��� ��������� ��� "������" (login) �� ���������
������ � ��� ���������� ������ �� ��������� ������.

���� ����� �������� ���������-�������, ����������� ��� ������������
������������� ���������� � ��������� SSH.

%description clients -l uk
Ssh (Secure Shell) - �� �������� ��� "������" (login) �� צ������ϧ
������ �� ��� ��������� ������ �� צ�����Φ� ����Φ.

��� ����� ͦ����� ��������-�̦����, ����Ȧ�Φ ��� ������������
������������ �'������ � ��������� SSH.

%package server
Summary:	OpenSSH Secure Shell protocol server (sshd)
Summary(de):	OpenSSH Secure Shell Protocol-Server (sshd)
Summary(es):	Servidor OpenSSH para comunicaciones codificadas
Summary(fr):	Serveur de protocole du shell s�curis� OpenSSH (sshd)
Summary(it):	Server OpenSSH per il protocollo Secure Shell (sshd)
Summary(pl):	Serwer protoko�u Secure Shell (sshd)
Summary(pt):	Servidor do protocolo 'Secure Shell' OpenSSH (sshd)
Summary(pt_BR):	Servidor OpenSSH para comunica��es encriptadas
Summary(ru):	OpenSSH - ������ ��������� Secure Shell (sshd)
Summary(uk):	OpenSSH - ������ ��������� Secure Shell (sshd)
Group:		Networking/Daemons
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	rc-scripts >= 0.4.0.18
Requires(pre):	/bin/id
Requires(pre):	/usr/sbin/useradd
Requires(post,preun):	/sbin/chkconfig
Requires(post):	chkconfig >= 0.9
Requires(post):	grep
Requires(postun):	/usr/sbin/userdel
Requires:	/bin/login
Requires:	util-linux
Requires:	pam >= 0.77.3
Provides:	user(sshd)
Provides:	ssh-server

%description server
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine. It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to seperate libraries (OpenSSL).

This package contains the secure shell daemon. The sshd is the server
part of the secure shell protocol and allows ssh clients to connect to
your host.

%description server -l de
Dieses Paket installiert den sshd, den Server-Teil der OpenSSH.

%description server -l es
Este paquete contiene el servidor SSH. sshd es la parte servidor del
protocolo secure shell y permite que clientes ssh se conecten a su
servidor.

%description server -l fr
Ce paquetage installe le 'sshd', partie serveur de OpenSSH.

%description server -l it
Questo pacchetto installa sshd, il server di OpenSSH.

%description server -l pl
Ssh (Secure Shell) to program s�u��cy do logowania si� na zdaln�
maszyn� i uruchamiania na niej aplikacji. W zamierzeniu openssh ma
zast�pi� rlogin, rsh i dostarczy� bezpieczne, szyfrowane po��czenie
pomi�dzy dwoma hostami.

Ten pakiet zawiera serwer sshd (do kt�rego mog� ��czy� si� klienci
ssh).

%description server -l pt
Este pacote intala o sshd, o servidor do OpenSSH.

%description server -l pt_BR
Esse pacote cont�m o servidor SSH. O sshd � a parte servidor do
protocolo secure shell e permite que clientes ssh se conectem ao seu
host.

%description server -l ru
Ssh (Secure Shell) - ��� ��������� ��� "������" (login) �� ���������
������ � ��� ���������� ������ �� ��������� ������.

���� ����� �������� sshd - "�����" Secure Shell. sshd - ��� ���������
����� ��������� Secure Shell, ����������� �������� ssh ����������� �
����� ������.

%description server -l uk
Ssh (Secure Shell) - �� �������� ��� "������" (login) �� צ������ϧ
������ �� ��� ��������� ������ �� צ�����Φ� ����Φ.

��� ����� ͦ����� sshd - "�����" Secure Shell. sshd - �� ��������
������� ��������� Secure Shell, ��� ������Ѥ �̦����� ssh ��'���������
� ����� ������.

%package gnome-askpass
Summary:	OpenSSH GNOME passphrase dialog
Summary(de):	OpenSSH GNOME Passwort-Dialog
Summary(es):	Di�logo para introducci�n de passphrase para GNOME
Summary(fr):	Dialogue pass-phrase GNOME d'OpenSSH
Summary(it):	Finestra di dialogo GNOME per la frase segreta di OpenSSH
Summary(pl):	Odpytywacz has�a OpenSSH dla GNOME
Summary(pt):	Di�logo de pedido de senha para GNOME do OpenSSH
Summary(pt_BR):	Di�logo para entrada de passphrase para GNOME
Summary(ru):	OpenSSH - ������ ����� �������� ����� (passphrase) ��� GNOME
Summary(uk):	OpenSSH - Ħ���� ����� ������ϧ ����� (passphrase) ��� GNOME
Group:		Applications/Networking
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	ssh-extras
Obsoletes:	ssh-askpass
Obsoletes:	openssh-askpass

%description gnome-askpass
Ssh (Secure Shell) a program for logging into a remote machine and for
executing commands in a remote machine. It is intended to replace
rlogin and rsh, and provide secure encrypted communications between
two untrusted hosts over an insecure network. X11 connections and
arbitrary TCP/IP ports can also be forwarded over the secure channel.

OpenSSH is OpenBSD's rework of the last free version of SSH, bringing
it up to date in terms of security and features, as well as removing
all patented algorithms to seperate libraries (OpenSSL).

This package contains the GNOME passphrase dialog.

%description gnome-askpass -l es
Este paquete contiene un programa que abre una caja de di�logo para
entrada de passphrase en GNOME.

%description gnome-askpass -l pl
Ssh (Secure Shell) to program s�u��cy do logowania si� na zdaln�
maszyn� i uruchamiania na niej aplikacji. W zamierzeniu openssh ma
zast�pi� rlogin, rsh i dostarczy� bezpieczne, szyfrowane po��czenie
pomi�dzy dwoma hostami.

Ten pakiet zawiera ,,odpytywacz has�a'' dla GNOME.

%description gnome-askpass -l pt_BR
Esse pacote cont�m um programa que abre uma caixa de di�logo para
entrada de passphrase no GNOME.

%description gnome-askpass -l ru
Ssh (Secure Shell) - ��� ��������� ��� "������" (login) �� ���������
������ � ��� ���������� ������ �� ��������� ������.

���� ����� �������� ������ ����� �������� ����� ��� ������������� ���
GNOME.

%description gnome-askpass -l uk
Ssh (Secure Shell) - �� �������� ��� "������" (login) �� צ������ϧ
������ �� ��� ��������� ������ �� צ�����Φ� ����Φ.

��� ����� ͦ����� Ħ���� ����� ������ϧ ����� ��� ������������ Ц�
GNOME.

%prep
%setup -q
%patch0 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%{?with_ldap:%patch5 -p1}
%{?with_kerberos5:%patch6 -p1}
#%patch7 -p1
%patch8 -p1
%{?with_selinux:%patch9 -p1}
%{?with_selinux:%patch10 -p1}
%{?with_hpn:%patch11 -p1}
%{?with_hpn_none:%patch12 -p1}
%patch13 -p1

%build
cp %{_datadir}/automake/config.sub .
%{__aclocal}
%{__autoconf}
%{?with_chroot:CPPFLAGS="-DCHROOT"}
%configure \
	PERL=%{__perl} \
	--with-dns \
	--with-pam \
	--with-mantype=man \
	--with-md5-passwords \
	--with-ipaddr-display \
	%{?with_libedit:--with-libedit} \
	--with-4in6 \
	--disable-suid-ssh \
	--with-tcp-wrappers \
	%{?with_ldap:--with-libs="-lldap -llber"} \
	%{?with_ldap:--with-cppflags="-DWITH_LDAP_PUBKEY"} \
	%{?with_kerberos5:--with-kerberos5} \
	--with-privsep-path=%{_privsepdir} \
	--with-pid-dir=%{_localstatedir}/run \
	--with-xauth=/usr/X11R6/bin/xauth

echo '#define LOGIN_PROGRAM           "/bin/login"' >>config.h

%{__make}

cp -f %{SOURCE9} .
cp -f %{SOURCE10} .
%{__cc} %{rpmcflags} %{rpmldflags} connect.c -o connect

cd contrib
%if %{with gnome}
%{__make} gnome-ssh-askpass1 \
	CC="%{__cc} %{rpmldflags} %{rpmcflags}"
%endif
%if %{with gtk}
%{__make} gnome-ssh-askpass2 \
	CC="%{__cc} %{rpmldflags} %{rpmcflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},/etc/{pam.d,rc.d/init.d,sysconfig,security,env.d}} \
	$RPM_BUILD_ROOT%{_libexecdir}/ssh
%{?with_sshagentsh:install -d $RPM_BUILD_ROOT/etc/{profile.d,X11/xinit/xinitrc.d}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install connect    $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE4} $RPM_BUILD_ROOT/etc/pam.d/sshd
install %{SOURCE6} $RPM_BUILD_ROOT/etc/pam.d/passwdssh
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/sshd
install %{SOURCE3} $RPM_BUILD_ROOT/etc/rc.d/init.d/sshd
install %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/ssh_config
install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/sshd_config
%if %{with sshagentsh}
install %{SOURCE11} $RPM_BUILD_ROOT/etc/profile.d/
ln -sf	/etc/profile.d/ssh-agent.sh $RPM_BUILD_ROOT/etc/X11/xinit/xinitrc.d/ssh-agent.sh
install %{SOURCE12} $RPM_BUILD_ROOT/etc/ssh/
%endif

bzip2 -dc %{SOURCE7} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}

%if %{with gnome}
install contrib/gnome-ssh-askpass1 $RPM_BUILD_ROOT%{_libexecdir}/ssh/ssh-askpass
%endif
%if %{with gtk}
install contrib/gnome-ssh-askpass2 $RPM_BUILD_ROOT%{_libexecdir}/ssh/ssh-askpass
%endif
%if %{with gnome} || %{with gtk}
cat << EOF >$RPM_BUILD_ROOT/etc/env.d/GNOME_SSH_ASKPASS_GRAB_SERVER
#GNOME_SSH_ASKPASS_GRAB_SERVER="true"
EOF
cat << EOF >$RPM_BUILD_ROOT/etc/env.d/GNOME_SSH_ASKPASS_GRAB_POINTER
#GNOME_SSH_ASKPASS_GRAB_POINTER="true"
EOF
ln -s %{_libexecdir}/ssh/ssh-askpass $RPM_BUILD_ROOT%{_libexecdir}/ssh-askpass
%endif

rm -f	$RPM_BUILD_ROOT%{_mandir}/man1/slogin.1
echo ".so ssh.1" > $RPM_BUILD_ROOT%{_mandir}/man1/slogin.1

touch $RPM_BUILD_ROOT/etc/security/blacklist.sshd

%if "%{_lib}" != "lib"
find $RPM_BUILD_ROOT%{_sysconfdir} -type f -print0 | xargs -0 perl -pi -e "s#/usr/lib#/usr/%{_lib}#"
%endif

cat << EOF >$RPM_BUILD_ROOT/etc/env.d/SSH_ASKPASS
#SSH_ASKPASS="%{_libexecdir}/ssh-askpass"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%pre server
%useradd -P %{name}-server -u 40 -d %{_privsepdir} -s /bin/false -c "OpenSSH PrivSep User" -g nobody sshd

%post server
/sbin/chkconfig --add sshd
if [ -f /var/lock/subsys/sshd ]; then
	/etc/rc.d/init.d/sshd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/sshd start\" to start openssh daemon."
fi
if ! grep -qs ssh /etc/security/passwd.conf ; then
	umask 022
	echo "ssh" >> /etc/security/passwd.conf
fi

%preun server
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/sshd ]; then
		/etc/rc.d/init.d/sshd stop 1>&2
	fi
	/sbin/chkconfig --del sshd
fi

%postun server
if [ "$1" = "0" ]; then
	%userremove sshd
fi

%files
%defattr(644,root,root,755)
%doc *.RNG TODO README OVERVIEW CREDITS Change*
%attr(755,root,root) %{_bindir}/ssh-key*
%{_mandir}/man1/ssh-key*.1*
%dir %{_sysconfdir}
%dir %{_libexecdir}

%files clients
%defattr(644,root,root,755)
%doc connect.html
%attr(755,root,root) %{_bindir}/connect
%attr(755,root,root) %{_bindir}/ssh
%attr(755,root,root) %{_bindir}/slogin
%attr(755,root,root) %{_bindir}/sftp
%attr(755,root,root) %{_bindir}/ssh-agent
%attr(755,root,root) %{_bindir}/ssh-add
%attr(755,root,root) %{_bindir}/scp
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ssh_config
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/SSH_ASKPASS
%if %{with sshagentsh}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/ssh-agent.conf
%attr(755,root,root) /etc/profile.d/ssh-agent.sh
%attr(755,root,root) /etc/X11/xinit/xinitrc.d/ssh-agent.sh
%endif
%{_mandir}/man1/scp.1*
%{_mandir}/man1/ssh.1*
%{_mandir}/man1/slogin.1*
%{_mandir}/man1/sftp.1*
%{_mandir}/man1/ssh-agent.1*
%{_mandir}/man1/ssh-add.1*
%{_mandir}/man5/ssh_config.5*
%lang(it) %{_mandir}/it/man1/ssh.1*
%lang(it) %{_mandir}/it/man5/ssh_config.5*
%lang(pl) %{_mandir}/pl/man1/scp.1*
%lang(zh_CN) %{_mandir}/zh_CN/man1/scp.1*

# for host-based auth (suid required for accessing private host key)
#%attr(4755,root,root) %{_libexecdir}/ssh-keysign
#%{_mandir}/man8/ssh-keysign.8*

%files server
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/sshd
%attr(755,root,root) %{_libexecdir}/sftp-server
%attr(755,root,root) %{_libexecdir}/ssh-keysign
%{_mandir}/man8/sshd.8*
%{_mandir}/man8/sftp-server.8*
%{_mandir}/man8/ssh-keysign.8*
%{_mandir}/man5/sshd_config.5*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/sshd_config
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/pam.d/sshd
%attr(640,root,root) %{_sysconfdir}/moduli
%attr(754,root,root) /etc/rc.d/init.d/sshd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/sshd
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/security/blacklist.sshd

%if %{with gnome} || %{with gtk}
%files gnome-askpass
%defattr(644,root,root,755)
%config(noreplace,missingok) %verify(not md5 mtime size) /etc/env.d/GNOME_SSH_ASKPASS*
%dir %{_libexecdir}/ssh
%attr(755,root,root) %{_libexecdir}/ssh/ssh-askpass
%attr(755,root,root) %{_libexecdir}/ssh-askpass
%endif
