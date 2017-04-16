# irkshop
## Django Shopping Mall WebSite for IRK

# How to Use

1.First, clone this repo.
```sh
$ git clone https://github.com/Beomi/irkshop.git
```

1-1.(Optional, but Strongly suggested) Make Virtualenv for this project.
If you have installed virtualenv and virtualenv-wrapper, you can make like this:
```
$ mkvirtualenv irkshop
$ workon irkshop
(irkshop) $ 
```

If you dont' use virtualenv, you can still use pyvenv in Python3(over 3.4):
```
$ python3 -m venv irkshop
$ source irkshop/bin/activate
(irkshop) $
```


2.Install Python Packages required.
```
$ cd irkshop
$ pip install -r requirements.txt
```

3.You should make `envs.json`(or `envs_dev.json` for develope on local) file before first migration.
```json
{
  "FACEBOOK_KEY":"",
  "FACEBOOK_SECRET":"",
  "GOOGLE_KEY":"",
  "GOOGLE_SECRET":"",
  "PAYPAL_ID":"",
  "GMAIL_ID":"",
  "GMAIL_PW":"",
  "DB_NAME":"",
  "DB_USER":"",
  "DB_PW":"",
  "DB_HOST":"",
  "DB_PORT":""
}

```
like this.

FACEBOOK_KEY and _SECRET are used for Facebook Login.
You can get on https://developers.facebook.com/

GOOGLE_KEY and _SECRET are used for Google Login.
You can get on https://console.developers.google.com/

PAYPAL_ID is used for Paypal Payment accept. It works with django-paypal.
You can use your paypal id or sandbox paypal id.

GMAIL_ID and _PW are used for sending mail for customers.
You can use your google account.

4.Then go with first migrate!
```
(irkshop) $ python manage.py migrate
```
then db.sqlite3 file will be created.

5.Go to your shop with django test server!
```
(irkshop) $ python manage.py runserver
```
and go to http://localhost:8000

# Packages used on this project
## Python/pip
- Django(1.10) // noqa
- django-carton // django session-based, simple cart addon.
- django-ckeditor // use ckeditor on django admin page
- django-paypal // use paypal with django
- pillow // django image field
- python-social-auth // FB/Google social login
## JS/CSS
- jQuery 2
- fullpage.js
- izimodal.js
- bootstrap 3

# How to deploy
## Before start
You should fork this repo for your own github account.
Because we'll use github repo as deploy method.

## Deploy Env
OS: Ubuntu 14/16

## Let's Begin!
You'll want to deploy your own shop.
I use "fabric3" to deploy this project on real-server.

so, let's start with install fabric3.
```
$ python3 -m pip install fabric3
```
fabric3 is python3-based, fabric fork project. 
(original fabric doesn't support py3 yet)

Before use fabric, you should make deploy.json file.
It can be like this:
```
{
  "REPO_URL":"https://github.com/Beomi/irkshop.git",
  "PROJECT_NAME":"irkshop",
  "REMOTE_HOST":"shop.resist.kr",
  "REMOTE_USER":"sudo-granted-user",
  "REMOTE_PASSWORD":"sudo-granted-user's-password"
}
```
You should change elements of that.
REPO_URL to your account's repo,
REMOTE_HOST for your website's url(and ssh url),
REMOTE_USER should not be ROOT but sudo granted user.

If you finished above all, you can setting your new server with this:
```
$ fab new_server
```
This command let you install apache2, python3 and link them, and then even make virtualenv / virtualhost and finishing deploy on real-server.
(It even setting your firewall, too!)
However, that command should be used just 1 time after server setup.

If you made your code changed, and commit&push to github, you can just simply deploy:
```
$ fab deploy
```
This command just fetch your github repo and do migrate/collectstatics/restart server.
