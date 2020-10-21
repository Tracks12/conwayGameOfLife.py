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

| Fonctionnalités                   | Commandes                                                                                |
| --------------------------------- | ---------------------------------------------------------------------------------------- |
| Exécuter le script                | `$ python main.py`                                                                       |
| Créer une nouvelle map            | `$ python main.py -n <x> <y>`<br />`$ python main.py --new <x> <y>`                      |
| Insérer une ou plusieurs cellules | `$ python main.py -a "[(x, y), ...]"`<br />`$ python main.py --add "[(x, y), ...]"`      |
| Insérer une entité                | `$ python main.py -A <type> <x> <y>`<br />`$ python main.py --add-entity <type> <x> <y>` |
| Afficher la map enregistrée       | `$ python main.py -d`<br />`$ python main.py --display`                                  |

## Sauvegarde

Les maps générées sont sauvegardées automatiquement sous format **JSON** après chaque mise à jour de celle-ci dans le fichier [`data.json`](data.json)

### Les entités

De même que pour la map, les entités sont stockées dans le fichier [`entity.json`](entity.json) au format **JSON**

Si vous voulez ajouter des entités dans le fichier, vous pouvez le faire en suivant le formatage de positionnement relatif avec les coordonnées **x** et **y** comme dans l'exemple ci dessous:

```json
{
  "nom de l'entité": "[(x, y), (x, y+1), (x+1, y), (x+1, y+1)]",
  ...
}
```

## Exemples d'utilisations

![gamePlay-example](example.gif)

On génère une nouvelle map avec `python main.py -n 50 50`

On ajoute les cellules active de sorte à former une entité:

- **Bloc**: `python main.py -a "[(2,1), (2,2), (3,1), (3,2)]"`
- **Grenouille**: `python main.py -a "[(2,1), (3,1), (4,2), (3,4), (2,4), (1,3)]"`
- **Planeur**: `python main.py -a "[(1,1), (2,2), (2,3), (3,1), (3,2)]"`

Et on lance le jeu avec `python main.py`

### Remarque

- Vous pouvez checker votre configuration avec `python main.py -d` pour afficher la map avec vos cellules actives
- Depuis la version 2.0, vous pouvez maintenant enregistrer une entité complète dans `entity.json` et l'ajouter sur la map comme ceci:
  - **Départ de floraison**: `python main.py -A flowering 25 25`
  - **Le clown**: `python main.py -A clown 25 25`

## Licence

Code sous license [GPL v3](LICENSE)
