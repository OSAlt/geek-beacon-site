## Docker 

If you're not familiar with docker you can learn more about docker [here](http://www.docker.com/).

There are two configuration files one titled local.yml and another titled production.yml

For development purposes you can completely ignore production.yml so my suggestion is to simply create 
an alias to local.

``` 
ln -s local.yml docker-compose.yml
```

The database credentials are configured in local.yml.  

Simply build the containers by running:

``` 
docker-compose build
```

Bring up the containers:


``` 
docker-compose up -d 
``` 


Then follow the logs if you like:

``` 
docker-compose logs -f 
``` 


Create your super user:

``` 
docker-compose run django python manage.py migrate  ## this should not be needed
docker-compose run django python manage.py createsuperuser
``` 


## Debugging:

http://cookiecutter-django.readthedocs.io/en/latest/developing-locally-docker.html


https://www.youtube.com/watch?v=n-wwp17MqhU Possibly useful. 

## Recommended IDE setup instructions.

These instructions are for PyCharm.  It is not required by any means, but makes it easier to develop.

Add the docker image as a python interpreter in your IDE.

![docker](/doc/screens/docker_setup.png)


Run the following script:

script: $PROJECT_DIR/manage.py
parameters: runserver_plus 0.0.0.0:8000


![debug_setup](/doc/screens/debug_setup.png)

# Running App

You should be able to access the site via http://0.0.0.0:8000/admin/ and will have to create the default site. 
Start by logging into admin interface.


IMPORTANT::

In the left hand menu select Pages and then again Pages. Add new child page and make sure
you select Home Page type. Give it a nice title and publish it. Now delete the default Welcome page.
Go to the Settings and select Sites. Add a site. Use localhost as a hostname and also give it a nice name. :)

Select a root page. There should be only one page available. Check 'Is default site:' and save the site.

Point your browser to http://0.0.0.0:8000 and it should be working.

Now you can start adding pages, blog index pages and blog posts.

Categories are hidden in the Snippets menu.

  
### Setting up stuff
#### Footer section

Right now there are 4 categories hardcoded in the `footer.html` template:

- geeks-abroad
- gaming
- osalt
- squirrel-army

This means that these categories have to exist and their _slugs_, have
to be the same as on this list. If they are not, then posts in those
categories won't be shown in the footer.  
