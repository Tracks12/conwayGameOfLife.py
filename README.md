# **conwayGameOfLife**

Le jeu de la vie de John Horton Conway

Pour en connaître un peu plus, vous pouvez visiter la page **[Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)** du jeu de la vie.

## Consignes

La liste des consignes du sujet est disponible dans le [todo.md](todo.md)

## Pré-requis

L'installation de **[Python 3](https://www.python.org/downloads/)** est recommandé pour l'éxécution du script

## Dépendances

- [json](https://docs.python.org/3/library/json.html)
- [os.system](https://docs.python.org/3/library/os.html#os.system)
- [sys.argv](https://docs.python.org/3/library/sys.html#sys.argv), [sys.version_info](https://docs.python.org/3/library/sys.html#sys.version_info)
- [platform.system](https://docs.python.org/3/library/platform.html#platform.system)
- [time.sleep](https://docs.python.org/3/library/time.html#time.sleep)

## Utilisations

| Fonctionnalités                     | Commandes                                                                                                    |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Exécuter le script                  | `$ python main.py`                                                                                           |
| Créer une nouvelle map              | `$ python main.py -n <mapName> <x> <y>`<br />`$ python main.py --new <mapName> <x> <y>`                      |
| Insérer une ou plusieurs cellule(s) | `$ python main.py -a <mapName> "[(x, y), ...]"`<br />`$ python main.py --add <mapName> "[(x, y), ...]"`      |
| Insérer une entité                  | `$ python main.py -A <mapName> <type> <x> <y>`<br />`$ python main.py --add-entity <mapName> <type> <x> <y>` |
| Afficher une map enregistrée        | `$ python main.py -d <mapName>`<br />`$ python main.py --display <mapName>`                                  |

## Sauvegarde

Les maps générées sont sauvegardées de manière automatique après chaque mise à jour de celle-ci dans un fichier **JSON** portant le nom de la map dans le répertoire **[saves/](saves/)** (_exemple: **[world.json](saves/world.json)**_)

### Les entités

De même que pour la map, les entités sont stockées dans le fichier **[entity.json](entity.json)**

Si vous voulez ajouter des entités dans le fichier, vous pouvez le faire en suivant le formatage de positionnement relatif avec les coordonnées **x** et **y** comme dans l'exemple ci dessous:

```json
{
  "nom de l'entité": "[(x, y), (x, y+1), (x+1, y), (x+1, y+1)]",
  ...
}
```

## Exemples d'utilisations

![aperçu](preview.gif)

On génère une nouvelle map avec `$ python main.py -n data 50 50`

On ajoute les cellules active de sorte à former une entité:

- **Bloc**: `$ python main.py -a data "[(2,1), (2,2), (3,1), (3,2)]"`
- **Grenouille**: `$ python main.py -a data "[(2,1), (3,1), (4,2), (3,4), (2,4), (1,3)]"`
- **Planeur**: `$ python main.py -a data "[(1,1), (2,2), (2,3), (3,1), (3,2)]"`

Et on lance le jeu avec `$ python main.py` tout en entrant le nom de la map que l'on souhaite charger

### Remarque

- Vous pouvez checker votre configuration avec `$ python main.py -d data` pour afficher la map avec vos cellules actives
- Depuis la version 2.0, vous pouvez maintenant enregistrer une entité complète dans **[entity.json](entity.json)** et l'ajouter sur la map comme ceci:
  - **Départ de floraison**: `$ python main.py -A data flowering 25 25`
  - **Le clown**: `$ python main.py -A data clown 25 25`

## Licence

Code sous license [GPL v3](LICENSE)
