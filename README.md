# Geek Beacon


Website, built on wagtail

This website is a combination of wagtail and features cherry-picked out of the CookieCutter project: http://cookiecutter-django.readthedocs.io/en/latest/index.html.

There are features that are just simply missing, others that are consciously omitted due to a variety of reasons, we'll call them artistic differences. 

See  [Doc Folder](doc/) for more details


## Design Choices

1. Docker Volumes are mounted locally.  cookie cutter uses the docker managed volumes, my personal preference is to have the docker container write the project file system. 

It makes it easier in my mind to backup and see what is going on. We may re-visit this at a later date. 

