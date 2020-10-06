# **conwayGameOfLife**

Le jeu de la vie de John Horton Conway

## Pré-requis

L'installation de **Python 3** est recommandé pour l'éxécution du script

## Dépendances

- JSON
- sys
- os.system
- platform.system
- random.getrandbits & random.randint
- sleep

## Utilisations

| Fonctionnalités                  | Commande                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| Executer le script               | `$ python main.py`                                                                  |
| Créer une nouvelle map           | `$ python main.py -n <x> <y>`<br />`$ python main.py --new <x> <y>`                 |
| Insérer une ou plusieur cellules | `$ python main.py -a "[(x, y), ...]"`<br />`$ python main.py --add "[(x, y), ...]"` |
| Afficher la map enregistrer      | `$ python main.py -d`<br />`$ python main.py --display`                             |
