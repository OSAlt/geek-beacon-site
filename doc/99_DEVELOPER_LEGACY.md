## Legacy Method

Linux / Mac is not required but you'll find any *Nix like OS to be much easier to work with.  Windows in theory will
work, but you will probably have a harder time working in it. 


###NOTE:

Classic method requires you to have a postgres database server setup.  

Make sure that:

- Python 3.4 at least needs to be installed
- Make sure that venv is also installed, it usually is


First you need to setup your virtual environment:

```
$ mkdir -p ~/.venv/geekbeacon
$ python3 -m venv ~/.venv/geekbeacon
$ sudo apt-get install python3-pip      # Just in case
```

Now, activate the environment and complete installation there:

```
$ source ~/.venv/geekbeacon/bin/activate
$ pip install -r requirements/local.txt
$ pip install -r requirements/test.txt
```

Clone the project (If you haven't done soe already)

Create a directory for your site and clone the github repo:

```
$ git clone git@github.com:OSAlt/geek-beacon-site.git 
```

At this point you should probably setup an IDE to execute this.  or expose the following env variables locally.

```
DATABASE_URL=postgres://$POSTGRES_USER:$POSTGRES_PASSWORD@postgres:5432/$POSTGRES_USER
```

```
$ pyhton manage.py migrate
$ python manage.py createsuperuser
```

```
$ python manage.py runserver
```

### Upgrades and migrations

Upon deploying the new code it will sometimes become necessary to perform
database migrations, like so:

```
$ cd ~/where/your/project/lives
$ source ~/.venv/geekbeacon/bin/activate 
$ python manage migrate
```
And that's basically it.



This setup is mainly based on: http://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html and you can 
read up a bit more on it at the source if you run into any troubles.


