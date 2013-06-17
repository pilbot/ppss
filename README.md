Pilbot's Pokémon Storage System
===============================

A basic django project to manage Pokémon card collections. The basic install will setup a personal database (currently tested on SQLite, but should work on any [Django compatible database](https://docs.djangoproject.com/en/1.5/topics/install/#database-installation)) that can be used to store your collection including card condition (e.g. Mint/NM/Excellent etc.) and variants (e.g. Normal, Reverse Holo, Cracked Holo).

Setup
-----

1. Download repository using `git`.
2. You may need to install the python dev package (e.g. On Ubuntu `sudo apt-get install python-dev`) to be able to install the requirements.
3. (Optional) It is best to run this all in a [virtualenv](https://pypi.python.org/pypi/virtualenv). Then it doesn't mess with your system python install. 
4. Run `pip install pip_requirements` to install the required packages.
5. Copy the file `pkmn/custom_settings.py.example` to  `pkmn/custom_settings.py` and fill in the required fields.
6. Run `python manage.py syncdb`.
    * Enter a personal username and password.
7. Run `python manage.py scrapesets`, this will pull all set information from [Bulbapedia](http://bulbapedia.bulbagarden.net/) using the [MediaWiki API](http://www.mediawiki.org/wiki/API:Main_page).
8. Run `python manage.py scrapeset`.
    * If you are only interested in one particular set you can supply the set name as the first argument and it will create it.
9. Run `python manage.py runserver`.
    * This will start the development webserver on port 8000, you can test the site by going to <http://localhost:8000>.

