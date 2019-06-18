GitLab-parser
==============================

### Environment variables
| Key    | Description   |    Default value  |
| :---         |     :---      |          :--- |
| `PRIVATE_GITLAB_TOKEN`  | personal access token on gitlab  | token |
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
