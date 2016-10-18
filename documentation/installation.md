Installation
============

Nous allons couvrir ici l'installation de l'application Escapad qui peut être utilisée de différente manières:

- via le script d'export
- via l'application web en local
- via l'application web déployé sur un serveur

Cette section est destinée aux usagers techniciens ou aux contributeurs du code qui souhaite installer l'application localement ou sur un serveur. 

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

## Obtenir les fichiers sources des modules de cours

Le principe d'Esc@pad consiste à transformer une arborescence de modules de cours en différents formats d'exports (mini-site web et archives pour LMS). Le point de départ est donc un dossier contenant plusieurs modules de cours, appelé "programme de cours" au même titre que [les cours Culture Numérique](https://culturenumerique.univ-lille3.fr/) qui comprennent plusieurs modules et qui sont produits à partir de l'application Esc@pad.

Chaque module de cours doit suivre la syntaxe et la structuration définie dans la [section syntaxe](syntaxe.md)). Le résultat de l'export est un dossier contenant un mini site Web (un dossier de fichiers HTML statiques) reprenant tous les modules de cours et incluant des archives IMSCC et EDX (cf [section export](export.md) pour l'usage de ces archives et le mapping adopté). Pour obtenir vos propres fichiers sources "Esc@pad", vous pouvez soit partir d'un dossier vide et suivre les [instructions de syntaxe](syntaxe.md), soit partir du dépôt git suivant proposant un patron de programme de cours:

    $ git clone https://github.com/CultureNumerique/course_template mon_nom_de_cours

Pour la suite, il est possible de simplement utiliser le script d'export localement à partir de ce dossier lui aussi local. Esc@pad est cependant pensé pour le travail collaboratif, et l'application web nécessite de disposer de l'adresse d'un dépôt git. Pour cela vous pouvez par exemple:

- forker le dépôt `course_template` depuis GitHub puis cloner votre fork localement, ou bien même le modifier sur la plateforme
- téléverser votre clone local sur l'hébergeur git de votre choix.

Dans les 2 cas vous disposerez ainsi de l'adresse "git" de votre propre version d'un dossier de cours transformable par Esc@pad.


## Exécution du script en local

En supposant donc que vous disposez d'un dossier local contenant votre contenu de cours structuré en respectant [le guide d'utilisation et la syntaxe Esc@pad](syntaxe.md),  le script `src/cnExport.py` vous permet d'obtenir un export Web contenant les archives importable dans Moodle ou EDX. L'usage de base est le suivant:

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
