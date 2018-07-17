### Deployment in production

This needs more documentation for now points of reference:


Docker Deploy: http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html

Backups: http://cookiecutter-django.readthedocs.io/en/latest/docker-postgres-backups.html


Once setup you'll have an nginx container, gunicorn with 4 workers and a postgres DB.

Future:

Add Redis for caching.  

Scaling:  
  - django 
  - redis 
  - celery / celery worker 
 
 These type of containers can be scaled up and if we take advantage of docker swarm we can go grow within the limits
 of our budget.
 
 Postgres and such will not be as easily scalable and will require some foresight once we reach the point 
 where the traffic cannot be handled by a single DB server.
 
   