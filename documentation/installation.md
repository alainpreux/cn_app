Installation
============

Cette section est destinée aux usagers techniciens ou aux contributeurs du code qui souhaitent installer l'application localement ou sur un serveur.

## Prérequis et installation minimale

Tout d'abord, il est nécessaire de disposer d'un environnement Python 2. Nous préconisons fortement l'adoption d'un environnement virtuel comme proposé par l'outils [`virtualenv`](https://virtualenv.pypa.io/en/stable/installation/) qui permet d'isoler des environnements python. Une fois virtualenv installé, créez un environnement:

    $ virtualenv cnappenv

Ceci créera un dossier `cnappenv`. Placez-vous dans ce dossier, et clonez l'application:

    $ cd cnappenv
    $ git clone https://github.com/CultureNumerique/cn_app
    $ cd cn_app
    $ source ../bin/activate

Ensuite, les librairies nécessaires sont installées via `pip` en utilisant le fichier de dépendences fourni `requirements.txt` de cette manière:

```
$ pip install -r requirements.txt
```

L'installation de toutes ces librairies reposent parfois sur des packets "systèmes". Pour une distribution linux basé sur Debian, assurez-vous que les paquets suivants sont installés:

- libxml2-dev
- libxslt-dev
- python-libxml2
- python-libxslt1
- python-dev
- zlib1g-dev


## Exécution du script en local

En supposant que vous disposez d'un dossier local `mon_dossier_de_cours` contenant votre contenu de cours structuré en respectant [le guide d'utilisation](usage.html) et la [syntaxe Esc@pad](syntaxe.html),  le script `src/cnExport.py` vous permet d'obtenir un export Web contenant les archives importable dans Moodle ou EDX. L'usage de base est le suivant:

```
$ cd cnappenv
$ source bin/activate
$ cd cn_app
$ python src/cnExport.py -r chemin/vers/mon_dossier_de_cours -d /chemin/vers/dossier/cible [OPTIONS]
```

Cette commande génère uniquement le mini site web reprenant tous les modules présent dans le dossier `mon_dossier_de_cours`. Les options suivantes sont disponibles (et doivent être placées à la suite de la commande ci-dessus à la place de `[OPTIONS]`):

- `-m moduleX moduleY ` : exporte uniquement les modules contenus dans les dossiers de module `moduleX`, `moduleY`
- `-i` : génère en plus l'archive IMSCC (IMS Common Cartridge) de chaque module de cours et la place dans le dossier d'export de chaque module avec le nom `moduleX.imscc.zip`
- `-e` : génère en plus l'archive EDX de chaque module de cours et la place dans le dossier d'export de chaque module avec le nom `moduleX_edx.tar.gz`
- `-f` : inclue les feedbacks dans l'export HTML, i.e dans le minisite.


## Running the Web application locally

For the Django web app cn_app to work, you need to copy `cn_app/site_settings.template.py` as `cn_app/site_settings.py`:

```
 $ cp cn_app/site_settings.template.py cn_app/site_settings.py

```
and change the settings depending on your running environment (dev, production, domain name, database, etc) as explained in comments in the file.

Then do the database migrations in order to bootstrap the database with the schemas needed by the application:
```
$ python manage.py migrate
```

Then start the web application locally with:

```
$ python manage.py runserver
```

and go to web adress at `http://localhost:8000`

## Déploiement sur un serveur

** TBD **

## Mettre à jour la documentation

** TBD **

- générée avec Spinx + recommonmark pour le support des fichiers markdown
- placez-vous dans le dossier `documentation` de votre installation
- copier le fichier `conf.py.template` en nommant la copie `conf.py`
- modifier les chemins de sys.path (vers ligne 21) pour permettre à Sphinx de trouver le code des modules Escapad situés dans le dossier `src` (utilisé pour l'autodocumentation du module `src/model.py`)
- la commande ` make html` permet alors de régénérer la documentation. 
