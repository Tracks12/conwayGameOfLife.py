# **conwayGameOfLife**

Le jeu de la vie de John Horton Conway

[https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

## Pré-requis

L'installation de [**Python 3**](https://www.python.org/downloads/) est recommandé pour l'éxécution du script

## Dépendances

- [json](https://docs.python.org/3/library/json.html)
- [os.system](https://docs.python.org/3/library/os.html#os.system)
- [sys.argv](https://docs.python.org/3/library/sys.html#sys.argv)
- [platform.system](https://docs.python.org/3/library/platform.html#platform.system)
- [random.getrandbits](https://docs.python.org/3/library/random.html#random.getrandbits) & [random.randint](https://docs.python.org/3/library/random.html#random.randint)
- [time.sleep](https://docs.python.org/3/library/time.html#time.sleep)

## Utilisations

| Fonctionnalités                  | Commande                                                                            |
| -------------------------------- | ----------------------------------------------------------------------------------- |
| Executer le script               | `$ python main.py`                                                                  |
| Créer une nouvelle map           | `$ python main.py -n <x> <y>`<br />`$ python main.py --new <x> <y>`                 |
| Insérer une ou plusieur cellules | `$ python main.py -a "[(x, y), ...]"`<br />`$ python main.py --add "[(x, y), ...]"` |
| Afficher la map enregistrer      | `$ python main.py -d`<br />`$ python main.py --display`                             |

## Sauvegarde

Les maps générés sont sauvegarder automatiquement sous format **JSON** après chaque mise à jour ce celle-ci dans le fichier `data.json`

## Exemples d'utilisations

![gamePlay-example](example.gif)

On génère une nouvelle map avec `python main.py -n 50 50`

On ajoute les cellules active de sorte à former une entité:
- **Block**: `python main.py -a "[(2,1), (2,2), (3,1), (3,2)]"`
- **Grenouille**: `python main.py -a "[(2,1), (3,1), (4,2), (3,4), (2,4), (1,3)]"`
- **Planeur**: `python main.py -a "[(1,1), (2,2), (2,3), (3,1), (3,2)]"`
- **Départ de floraison**: `python main.py -a "[(10, 7), (9, 8), (11, 8), (9, 9), (10, 9), (11, 9), (9, 10), (11, 10), (10, 11)]"`
- **Le clown**: `python main.py -a "[(26, 24), (25, 24), (24, 24), (26, 25), (24, 26), (25, 26), (26, 26)]"`

Et on lance le jeu avec `python main.py`

### Remarque

Vous pouvez checker votre configuration avec `python main.py -d` pour afficher la map avec vos cellules actives

## Licence

Code sous license [GPL v3](LICENSE)
