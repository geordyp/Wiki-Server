# Wiki-Server
Working with the [iPlant Cyberinfrastructure Collaborative](http://www.iplantcollaborative.org) to share biological applications and data for high-throughput phenotyping. Creating a wiki-style web server where users are allowed to post to share their own projects and algorithms.

## Technologies Used
* [Django](https://www.djangoproject.com/)
* [Vagrant](https://www.vagrantup.com/)

## Setup
1. After cloning this repo to your machine, enter the command `vagrant up` from the directory containing "Vagrantfile"
2. From the same directory, enter the command `vagrant ssh`
3. Once vagrant is up and running, enter `cd /vagrant/researchproject`
4. Then enter the command `python manage.py runserver 0:5000` and use the following url to view the project: http://localhost:5000/wiki/
5. To run tests, use `python manage.py test`

## Author
Geordy Williams
