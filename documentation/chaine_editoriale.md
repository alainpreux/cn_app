# Comment les éléments de cours "Culture Numérique" sont-ils produits ?
========================================================================

Nous détaillons ici la chaine éditoriale adoptée pour la production des modules mis à dispositions sur ce dépôt.  
Nous utilisons un fichier dit "maitre" comme matrice de base pour générer le cours. La syntaxe employée est basée sur le format MarkDown, que nous avons étendu pour nos besoins spécifiques. Ces ajouts consistent en des conventions décrites ci-dessous et l'usage d'extensions proposées par la [librairie Python de MarkDown](https://pythonhosted.org/Markdown/extensions).


### Structure globale d'un cours Culture Numérique
Un cours se décompose en sections et sous-sections. Le niveau sous-sections constitue le niveau "pivot" de la structure d'un cours Culture NUmérique. Chaque sous-section peut être du type et de la forme suivante:  

1. cours simple (texte + images)  
2. vidéo de cours accompagnée de la version texte
3. activité de 3 types possibles:
    - auto-évaluation sous forme de quiz
    - exercice autonome
    - exercice d'approfondissement

RMQ: les 2 derniers types d'exercice incluent un énoncé (texte riche) et un espace pour fournir une réponse sous forme de texte libre


### Cours simple

Rédigée en MarkDown, c'est un type de sous-section simple consistant en du texte mis en forme et enrichi d'images.
Par rapport au MArkdown simple, nous utilisons les fonctions supplémentaires décrites ci-après.


#### ajouter des classes CSS

Avec des [Attribute list](https://pythonhosted.org/Markdown/extensions/attr_list.html): Pour permettre d'ajouter des classes CSS à une image ou à un bloc de texte, pour permettre une mise en page enrichie.
Un exemple pour ajouter un attribut en ligne à un lien:  
`[link](http://example.com){: class="foo bar" .titre title="Some title!" }`  
qui produit le HTML suivant:  
`<p><a href="http://example.com" class="foo bar titre" title="Some title!">link</a></p>`  

Notez que pour ajouter des classes on peut soit spécifier `.une_classe` ou `class='une_classe``


#### Commentaires invisibles
En utilisant simplement les commentaires HTML:

        <!-- On pourrait aussi mentionner les lol cats dans cette section non ? -->

Le commentaire suivant ne sera donc pas visible dans le rendu HTML final.
<!-- Il faudrait vraiment enrichir cette documentation de quelques Gifs animés -->        


### Vidéo de cours

Ces éléments de cours consistent en des sous-sections pouvant inclure 1 ou plusieurs vidéos d'animations. Pour qu'un lien vers une vidéo (Vimeo uniquement pour l'instant) soit reconnu comme video de cours,  on utilise le principe des *attribute lists* (cf ci-dessus) en ajoutant la classe `cours_video`:  

    [Introduction au web](https://vimeo.com/138623497){: .cours_video }

ou  

    [Introduction au web](https://vimeo.com/138623497){: class="cours_video" }

Ce lien doit être placé à l'intérieur d'une sous-section. Une sous-section peut bien sûr comporter plusieurs vidéos de cours.

Ces liens vidéos font l'objet d'un traitement spécifique selon le type d'export:
* export Site Vitrine HTML: on génère un code d'iframe qui permet de lire le/les vidéo/s sans quitter la page courante;
* pour l'export Moodle/IMSCC, le plugin Viméo de Moodle permet de transformer le lien vidéo en iframe automatiquement:
![video_moodle](media/3.vue_cours_avec_video.png)

**NB:** les liens de videos doivent être de la forme

`https://vimeo.com/1234568`

et non

`https://player.vimeo.com/video/1234568`

La 2e forme est celle du champ "src" des iframes vimeo, mais l'API Vimeo requiert la 1ère forme, et qui est le lien permettant de plus d'accéder à la page vimeo de la video, et donc d'accéder à la chaine, aux autres videos, de liker, partager, etc.

### Sous-sections d'activités

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


#### Syntaxe GIFT

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

#### HTML et MarkDown dans les questions rédigées en GIFT

Dans les questions rédigées en GIFT il est possible de rédiger le texte au format HTML ou Markdown en spécifiant devant chaque bloc la syntaxe ([voir explications à la fin de ce paragraphe](https://docs.moodle.org/28/en/GIFT_format#Percentage_Answer_Weights)).

Dans le cas du Markdown, il y a cependant une limitation pour les listes (simples ou numérotées). En Markdown il faut laisser une ligne vide avant de commencer une liste:
```
Ingrédients:

- carottes
- pommes de terre

```
... or dans la spécification GIFT, une ligne vide sépare 2 questions distinctes. Le compromis que nous adoptons ici consiste à dire qu'un simple passage à la ligne est conservé dans l'export texte **pour les activités uniquement et non le reste du texte de cours**. Les listes pourront donc être écrite à l'aide de `-` après un passage à la ligne:
Par exemple:
```
Ingrédients:
- carottes
- pommes de terre

```  
sera interprété comme ceci (en HTML):
```
<p>
Ingrédients<br />
- carottes<br />
- pommes de terre<br />
</p>
```
