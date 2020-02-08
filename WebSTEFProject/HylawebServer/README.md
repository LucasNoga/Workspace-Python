# HylaWEB

Version WEB de Hylafax

## Installation
Installer ubuntu LTS version serveur (Actuellement la 16.04 LTS)
serveur : hylaweb

### Installer ERLANG + RABBITMQ
Installation via apt
* ERLANG : https://packages.erlang-solutions.com/erlang/#tabs-debian
* RABBITMQ : https://www.rabbitmq.com/install-debian.html

Configuration de RabbitMQ

Activation des Plugins : 
```
rabbitmq-plugins enable rabbitmq_management
rabbitmq-plugins enable rabbitmq_federation
rabbitmq-plugins enable rabbitmq_federation_management
```

Déclaration du Virtual Host :
`rabbitmqctl add_vhost HYLAFAX`

Ajout du fichier de configuration pour autoriser les users à se connecter à l'interface de management.


```
/etc/rabbitmq/rabbitmq.conf
---------------------------
##
## Security, Access Control
## ==============
##

## Related doc guide: http://rabbitmq.com/access-control.html.

## The default "guest" user is only permitted to access the server
## via a loopback interface (e.g. localhost).
## {loopback_users, [<<"guest">>]},
##
# loopback_users.guest = true

## Uncomment the following line if you want to allow access to the
## guest user from anywhere on the network.
loopback_users.guest = false
```
### Installation de NGINX
`apt-get install nginx`

### Installation de VIRTUALENV
`pip install --proxy=http://10.253.255.100:3128 virtualenv`

### Installation de proftp
`apt-get install proftpd-basic`

Ajouter cette ligne à la fin du fichier /etc/shells
```
/bin/false
```

creation du compte ftp
```
mkdir /home/ftpHylaprint
useradd ftpHylaprint -p ftpHylaprint -d /home/ftpHylaprint -s /bin/false
chown -R ftpHylaprint:ftpHylaprint /home/ftpftrecal
```

## Configuration
### configuration de la federation RabbitMQ (A effectuer sur le serveur distant)

installer les plugins 
```
rabbitmq-plugins enable rabbitmq_management
rabbitmq-plugins enable rabbitmq_federation
rabbitmq-plugins enable rabbitmq_federation_management
```
Déclaration du Virtual Host :
`rabbitmqctl add_vhost HYLAFAX`

Déclaration de la fédération :

`rabbitmqctl set_parameter  -p HYLAFAX federation-upstream my-upstream '{"uri":"amqp://server","expires":3600000}'`

déclaration de la policy :


```
rabbitmqctl set_policy -p HYLAFAX --apply-to exchanges federate-abo "^hyla\." '{"federation-upstream-set":"all"}'
rabbitmqctl set_policy -p HYLAFAX --apply-to exchanges federate-sys ".*\\\.*\\\HYL\\\SYS$" '{"federation-upstream-set":"all"}'
```

### configuration de NGINX
Tutorial pour configurer la publicartion d'application FLASK sur NGINX

> https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04

Cloner le depot dans /opt pour installer le site WEB et les API

Creer un environnement virtuel pour Pyhton et installer les dependances

```
cd /opt/HylaWEB
virtualenv HylaWEBenv
source HylaWEBenv/bin/activate
pip install --proxy=http://10.253.255.100:3128 -r dependance
deactivate
```
changer le propriétaire du dossier WEB pour mettre www-data
chmod wwww-data:www-data HylaWEB/API


créer le fichier : /etc/systemd/system/HylaWEBapi.service

```
[Unit]
Description=Gunicorn instance to serve HylaWEB API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/opt/HylaWEB/API
Environment="PATH=/opt/HylaWEB/HylaWEBenv/bin"
ExecStart=/opt/HylaWEB/HylaWEBenv/bin/gunicorn --workers 3 --bind unix:HylaWEBapi.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
``` 

et activer le service

```
sudo systemctl start HylaWEBapi.service
sudo systemctl enable HylaWEBapi.service
```


creer le fichier :  /etc/nginx/sites-available/HylaWEBapi

```
server {
    listen 8091;
    server_name 10.253.254.74;

    location /HylaWEB {
        rewrite ^/HylaWEB(.*) /$1 break;
        include proxy_params;
        proxy_pass http://unix:/opt/HylaWEB/API/HylaWEBapi.sock;
    }
}
```

activer le site
```
ln -s /etc/nginx/sites-available/myproject /etc/nginx/sites-enabled
nginx -t
sudo systemctl restart nginx
```