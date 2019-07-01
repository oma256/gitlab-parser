GitLab-parser
==============================
> The peculiarity of the application is to parse all the tasks 
> whose status is open, and store the working log in the database

### Environment variables
create .env file on the project root diretory

| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `DJANGO_GITLAB_TOKEN`  | personal access token on gitlab  | token |
| `DJANGO_SECRET_KEY`  | secret key  | my_secret_key |
| `DJANGO_DEBUG`  | debug_site  | False |
| `DJANGO_ALLOWED_HOST`  | allowed host  | 0.0.0.0 |

.env file example:
```
DJANGO_DEBUG=True 
DJANGO_SECRET_KEY=you secret key for project 
DJANGO_ALLOWED_HOSTS=0.0.0.0 
DJANGO_GITLAB_TOKEN=your gitlab token 
```

REQUIREMENTS
------------
The following requirements are required to run the project on your host:
1) Docker
2) docker-compose


HOW TO RUN PROJECT
------------------
```.bash
$ git clone https://github.com/oma256/gitlab-parser.git
``` 
```.bash
$ cd gitlab-parse
``` 
```.bash
$ docker-compose up --build
``` 
