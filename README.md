GitLab-parser
==============================

### Environment variables
create .env file on the project root diretory

| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `PRIVATE_GITLAB_TOKEN`  | personal access token on gitlab  | token |
| `DJANGO_SECRET_KEY`  | secret key  | my_secret_key |
| `DJANGO_DEBUG`  | debug_site  | False |
| `DJANGO_ALLOWED_HOST`  | allowed host  | 0.0.0.0 |
```.bash
$ export PRIVATE_GITLAB_TOKEN='your_token'
```  
### How to run project
```.bash
$ pipenv install
``` 
```.bash
$ ./manage.py migrate
``` 
```.bash
$ ./manage.py time_track
``` 
