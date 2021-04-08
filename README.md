## 2FA App 
App consist of:
- application - Flask REST Api
- static/src - React app created with Material UI

[![IMAGE ALT TEXT](http://img.youtube.com/vi/baiuDVE0yiE/0.jpg)](https://www.youtube.com/watch?v=baiuDVE0yiE "Video Title")

###
Issues of current implementation:
1. I would use useAuth hook https://usehooks.com/useAuth/ instead of checkAuth.
2. I need to migrate this code from Flow to TypeScript.
3. I would use useDebouncedEffect/useThrottledEffect or count failed login attempts on backend to 
   improve security.
4. I need to add support for submit form via 'Enter' 
5. I would improve backend code by using Flask-RESTful + Flask-Marshmallow.
6. I would add twilio integration to properly implement SMS handling.
7. I neeed to add backend/frontend unittests.

### Run Backend
```sh
$ export DATABASE_URL="postgresql://username:password@localhost/mydatabase"
$ python3 -m venv env - to create virtualenv
$ source env/bin/activate - to activate virtualenv
$ python3 -m pip install --upgrade pip - to upgrade pip to newer version
$ pip install -r requirements.txt - to install required package
$ python manage.py create_db
$ python manage.py db upgrade
$ python manage.py db migrate
$ python manage.py runserver
```

### Run Frontend
To build the app one can run:
```sh
$ cd static
$ yarn to install the dependencies

$ yarn build to generate the bundle (done by _parcel-bundler_)
```

Then please open _localhost:5000_ in your browser.

To run development mode:

`yarn start`

