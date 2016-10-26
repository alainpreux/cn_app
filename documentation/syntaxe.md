Syntaxe et structuration
========================

Nous détaillons ici la syntaxe adoptée pour la production de modules de cours à partir d'une arborescence de fichier source au format texte. Une arborescence type pouvant servir d'exemple est proposé dans le dépôt
[`course_template`](https://github.com/CultureNumerique/course_template) incluant un exemple type de fichier source de cours  [`course_template/module1/example_module1.md`](https://github.com/CultureNumerique/course_template/blob/master/module1/example_module1.md)


## Arborescence et structure des fichiers sources

Pour fonctionner normalement, l'application web Escapad nécessite d'avoir accès à un dossier `depot_de_cours` structuré à minima de la manière suivante:

    depot_de_cours/
        - moduleX/
            module_de_coursX.md
            media/
                - img.jpg
                - img2.png
        - moduleY/

Commentaires sur l'arborescence:

- Un dépôt de cours peut contenir plusieurs modules de cours chacun contenu dans un dossier
- Pour chaque dossier de module de cours:
    - un seul fichier source de type MarkDown dont le suffixe est '.md'
    - le dossier media est optionnel, mais doit être nommé `media`. Voir plus bas pour la gestion des images, mais nous recommandons de gérer les medias séparemment et d'utiliser préférablement des urls absolues

Le fichier source permettant de générer un cours (`module_de_coursX.md` dans noter exemple) peut se décompose en sections et sous-sections. Le niveau sous-sections constitue le niveau "pivot" de la structure d'un cours Culture NUmérique. Chaque sous-section peut être de 2 types:  

- sous-section de cours, incluant ou pas une ou plusieurs videos
- sous-section d'activité, chacune de 3 types possibles:
    - auto-évaluation sous forme de quiz
    - exercice autonome
    - exercice d'approfondissement

A noter qu'optionnellement le fichier peut débuter par une section d'en-tête comprenant des paramètres tels que titre, langue, etc. Cette partie se place avant la première section et comporte les champs suivants:

```
TITLE: Module de cours test 1 (Titre long)
MENUTITLE: Module Test 1 (Titre court)
AUTHOR: Culture Numérique
LANGUAGE: fr

# Section 1
## Sous-section 1.1
etc....

```
## Sous-section de cours

C'est un type de sous-section simple consistant en du texte structuré à l'aide de la syntaxe markdown et qui peut inclure des liens, des images, ou des videos à partir de l'url de ces ressources additionelles. La syntaxe markdown de base est expliqué dans [ce récapitulatif](http://daringfireball.net/projects/markdown/syntax).

### Extension markdow

Pour compléter les spécifications du markdow, plusieurs variantes ont été développées. Nous incluons les variantes de syntaxe ["PHP Markdown Extra"](https://michelf.ca/projects/php-markdown/extra/). La variante PHP Markdown Extra permet par exemple de spécifier des attributs attachés à des éléments de la syntaxe (lien, titre, image, etc). Ces ["special attributes"](https://michelf.ca/projects/php-markdown/extra/#spe-attr) permettent par exemple d'ajouter des classes CSS à une image ou à un bloc de texte, ou un titre:

```
[link](http://example.com){: class="foo bar" .titre title="Some title!" }`  
```
qui produit le HTML suivant:  


```
<p><a href="http://example.com" class="foo bar titre" title="Some title!">link</a></p>`  
```

**Notez** que pour ajouter des classes on peut soit spécifier `.une_classe` ou `class='une_classe``


### Ajouter des Vidéos



Ces éléments de cours consistent en des sous-sections pouvant inclure 1 ou plusieurs vidéos d'animations. Pour qu'un lien vers une vidéo (Vimeo uniquement pour l'instant) soit reconnu comme video de cours,  on utilise le principe des *attribute lists* (cf ci-dessus) en ajoutant la classe `cours_video`:  

    [Introduction au web](https://vimeo.com/138623497){: .cours_video }

ou  

    [Introduction au web](https://vimeo.com/138623497){: class="cours_video" }

Ce lien doit être placé à l'intérieur d'une sous-section. Une sous-section peut bien sûr comporter plusieurs vidéos de cours.

Ces liens vidéos font l'objet d'un traitement spécifique selon le type d'export:
* export Site Vitrine HTML: on génère un code d'iframe qui permet de lire le/les vidéo/s sans quitter la page courante;
* pour l'export Moodle/IMSCC, le plugin Viméo de Moodle permet de transformer le lien vidéo en iframe automatiquement:
![video_moodle](media/3.vue_cours_avec_video.png)

**NB:** les liens de videos Vimeo doivent être de la forme

`https://vimeo.com/1234568`

et non

`https://player.vimeo.com/video/1234568`

La 2e forme est celle du champ "src" des iframes vimeo, mais l'API Vimeo requiert la 1ère forme, et qui est le lien permettant de plus d'accéder à la page vimeo de la video, et donc d'accéder à la chaine, aux autres videos, de liker, partager, etc.

### Ajouter des images ou des fichiers resources

<!-- TBD -->

- syntaxe markdown
- prise en compte des medias locaux intégrés
- recommendations sur les medias externalisés


## Sous-section de type Activité

### Repérer les activités

Les activités peuvent être de 3 types:

- auto-évaluation pour vérifier la compréhension du cours: `comprehension`
- exercices de recherche autonome : `activité`
- Exercices d'approfondissement: `activité-avancée`

Pour le découpage des activités, nous n'utilisons plus les `##` de la syntaxe markdown, mais les "fenced code blocks" en spécifiant le type d'activité  juste à côté des "backticks":

        ```comprehension

        ```

ou

        ```activité-avancée

        ```


### Syntaxe GIFT

Ces activités sont rédigées en GIFT; chaque question est séparée par une ligne vide. La syntaxe Gift a été proposé par l'équipde Moodle pour permettre de gagner du temps dans la rédaction de quizz et de tests. Cette syntaxe est disponible sur [cette page](https://docs.moodle.org/28/en/GIFT_format). Il s'agit d'un format "texte" qui peut s'éditer dans n'importe quel "éditeur de texte" (et non dans un "traitement de texte").

Exemple:

        ```activité-avancée

        ::Représentation numérique::La représentation numérique d'un livre peut inclure des données qui ne se limitent pas au texte. Donnez quelques exemples
        {
        #### Le genre, la date de création, ...
        }

        ::Fonctionnalités d'un éditeur de textes::
        [html]<p>Parmi les  fonctionnalités suivantes, lesquelles sont possibles ?</p>
        {
        ~%25%copier/couper/coller#tous les éditeurs le permettent
        ~%25%rechercher et remplacer#très souvent disponible
        ~%25%avancer de mots en mots#souvent par la conjonction CRTL-flèches
        ~%25%corriger l'orthographe#certains le font
        ~%-100%mettre en gras#l'éditeur ne permet pas d'enregistrer des mises en forme (il est possible toutefois d'écrire des commandes de mise en forme : un mot n'est pas en gras mais un texte dans un langage peut exprimer l'ordre de mettre en gras)
        }
        ```


### Contenu des questions rédigées en GIFT

#### Spécifier le format

Dans les questions rédigées en GIFT il est possible de rédiger le texte au format HTML ou Markdown en spécifiant devant chaque bloc la syntaxe (voir explications à la fin de [ce paragraphe de la documentation Moodle sur le format GIFT](https://docs.moodle.org/28/en/GIFT_format#Percentage_Answer_Weights)).

#### Gestion des medias

<!-- TBD -->

#### Listes

Si le format choisi est le Markdown, il y a une limitation pour les listes (simples ou numérotées). En Markdown il faut laisser une ligne vide avant de commencer une liste:
```
Ingrédients:

- carottes
- pommes de terre

```
... or dans la spécification GIFT, une ligne vide sépare 2 questions distinctes. Les lignes vides pourront donc être indiquées dans un énoncé en GIFT avec le caractère de retour à la ligne "echappé" `\n`. Par exemple:
```
Ingrédients:
\n
- carottes
- pommes de terre

```  
Qui permettra donc d'avoir une liste dans l'export HTML:
```
Ingrédients:
<ul>
<li>carottes</li>
<li>pommes de terre</li>
</ul>
```
