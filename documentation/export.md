Export
======

Cette section est destinée à ceux qui souhaitent utiliser une archive EDX ou IMSCC générée par Esc@pad. Nous abordons les questions suivantes pour chaque type :

* Comment récupérer et utiliser ces archives dans EDX-Studion ou Moodle
* comment sont structurées les modules produits, ou quelles sont les correspondances établies entre le modèle de cours Esc@pad et le modèle inhérent de chacun des LMS supportés.


## Export EDX

Simplement ajouter l'option `-e` à la commande cnExport.py

### Correspondance entre les modèles de cours

La mapping se fait très naturellement entre le modèle Esc@Pad et le modèle EDX. Le grain pivot est celui de **sous-section** dans les 2 cas

|  EDX                     |      Esc#pad  |
| ------------             | --------------|
| course                  |        module |
| chapter                 |    section    |
| sequential              |  sous-section |
| sequential:display_name | titre de la sous-section  |
| sequential:format       | type de ssection |
| sequential:graded (T/F) |  en fonction du type  |
| vertical ("Unité")      |  1 seul "vertical" par sous-section   |
| component               | type de contenu > type de sous-section. |

Les sous-section peuvent être de 4 types qui sont notées ou pas selon un type défini dans une "grading policy". Pour Esc@Pad :

- (ungraded) : cours
- Compréhension : comprehension
- Activité : activite
- Activité Avancé : activite-avancee

Ensuite chaque `sequential` peut avoir plusieurs `vertical` dénommés "Unité" dans l'interface, mais dans Esc#pad il n'y a qu'une 'unité' par sous-section.

Chaque unité peut ensuite contenir différents composant EDX qui seront déterminé selon le contenu de la sous-section:

| composant EDX  |  Contenu d'une s-section   |
|----------------| ---------------------------|
| cnvideo        | video de cours = lien avec `{: .cours_video}` |
| html           | contenu de cours en HTML |
| problem        | quiz rédigés en GIFT |


### Stratégie de notation

Avec EDX il est possible de défninir :

- Le critère de "passation" du cours, ie la note globale minimale
- différents types d'exercices notés (ou de notation)
- pour chaque type:
   - nombre mini à passer pour être évalué
   - nombre d'exo que l'on peut sauter
   - poids dans note globale
   - nom et nom de code

 Tout ceci est défini dans le fichier de template
 [`templates/toEDX/policies/course/grading_policy.json`](../templates/toEDX/policies/course/grading_policy.json)


## Export vers Moodle via IMSCC

### Usage
<!-- FIXME :
- howto retrieve IMSCC archive
- global structure
-->

Esc@pad peut générer un fichier `module_folder.imscc.zip` qui peut être importé dans Moodle en tant que cours (cf [restauration d'un cours depuis une archive IMSCC sous Moodle](https://docs.moodle.org/28/en/IMS_Common_Cartridge_import_and_export)).

Cette archive contient également toutes les activités avec les questions associées déjà intégrées.

### Limitations à l'import d'archives IMS dans Moodle

Cette procédure d'import vers Moodle au format IMS Common Cartridge a quelques limitations :

- un bug affecte la version 3.0 de Moodle et **empêche l'import d'archive IMS si les quiz intégré (au format [XML/IMS-QTI](http://www.imsglobal.org/question/qtiv1p2/imsqti_asi_bindv1p2.html#1439623)) contiennent au moins une question Vrai/Faux**. [Ce bug a été signalé au groupe de developpement de Moodle](https://tracker.moodle.org/browse/MDL-53337); un contournement a été inclu dans le code actuel de toIMS.py qui déclare les questions Vrai/Faux comme des questions à choix multiples (toIMS.py ~l52).
- les **paramétrages d'achèvement et de revue des quiz ne sont pas conservés**. En effet ces paramètres spécifiques à Moodle ne sont pas capturés dans le format IMS. Le comportement limitant vient surtout de ce que **[les paramètres globaux](https://docs.moodle.org/29/en/Common_module_settings)**, qui normalement sont utilisés comme paramètres par défaut lors de la création d'un nouveau quiz **ne sont pas pris en compte lors de l'import IMSCC**. Ce comportement semble plutôt anormal et [a été signalé également](https://tracker.moodle.org/browse/MDL-53422)
