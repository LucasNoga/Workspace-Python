# HylaNOTIFYServer

Version du serveur commandant les HylaNOTIFY client (identification, notifications, ...)

Package requis : 
    - le package psycopg2 permet de gerer une base PostgreSQL
    - le package psycopg2.extras permet de recuperer mes enregistrements de fax dans un tableau associatifs
    - le package json permet serialiser et deserialiser mon fax
    - le package pika permet de gerer notre serveur RabbitMQ

# Installation des dépendances Python

```
apt install python-pip
pip install --proxy=http://10.253.255.100:3128 --upgrade pip
pip install --proxy=http://10.253.255.100:3128 -r dependance
```