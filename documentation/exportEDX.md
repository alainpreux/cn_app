Export vers EDX
----------------

# Utilisation

Simplement ajouter l'option `-e` à la commande cnExport.py 

# Correspondance entre les modèles de cours

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


# 