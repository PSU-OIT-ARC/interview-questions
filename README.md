# Project Template

## Introduction

Quick Start Template for ARC projects.
No need to download! Just follow the instructions below.

## Installation

Start a new Django project using this template

    project_name="lame"
    django-admin.py startproject --name=project_name.conf,README.md,Makefile,MANIFEST.in --extension=template,py --template=https://github.com/PSU-OIT-ARC/project_template/archive/master.zip $project_name

    cd $project_name

    virtualenv --no-site-packages .env
    source .env/bin/activate
    pip install -r requirements.txt

    chmod +x ./manage.py

    cp $project_name/settings/local.py.template $project_name/settings/local.py
    vi $project_name/settings/local.py

Sync the database

    ./manage.py syncdb
    ./manage.py migrate

NOTE: If you are using make, you can do the initial setup by running
`make initial-setup`.

Run the server

    make

or

    ./manage.py runserver

## Extras

Install RabbitMQ if you need it

    yum install rabbitmq-server
    service rabbitmq-server start
    chkconfig rabbitmq-server on

Run Celery if you are working with task queues

    celery -A project_name.celery worker --loglevel=info

Install ElasticSearch if you need it

    rpm --import http://packages.elasticsearch.org/GPG-KEY-elasticsearch
    echo "[elasticsearch-1.1]
    name=Elasticsearch repository for 1.1.x packages
    baseurl=http://packages.elasticsearch.org/elasticsearch/1.1/centos
    gpgcheck=1
    gpgkey=http://packages.elasticsearch.org/GPG-KEY-elasticsearch
    enabled=1" | sed -e 's/^[ \t]*//'  > /etc/yum.repos.d/elasticsearch.repo
    yum install elasticsearch
    sudo /sbin/chkconfig --add elasticsearch
    sudo service elasticsearch start

If you get an error saying "Can't start up: Not enough memory", update your version of java

    yum install java-1.6.0-openjdk

Rebuild the search index

    ./manage.py rebuild_index
