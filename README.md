# emptracker-django

* Python (3.8, 3.9)
* Django (3.0, 3.1)

We **highly recommend** and only officially support the latest patch release of
each Python and Django series.


## Installation
The first thing to do is to clone the repository:

```sh
$ https://github.com/VAIBHAV-BODHANE/Gallery_Django.git
$ cd Gallery_Django/gallery
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv -p python3.8.10 venv
$ source env/bin/activate
```
Then install the dependencies:

```sh
(venv)$ pip install -r requirements.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv`.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py makemigrations gallery_app
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
