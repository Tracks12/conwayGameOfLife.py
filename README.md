# **conwayGameOfLife**

Le "Jeu de la Vie", créé par John Horton Conway en 1970, est un automate cellulaire sur une grille en 2D, où chaque cellule peut être vivante ou morte. À chaque génération, l’état des cellules évolue selon des règles simples: une cellule vivante meurt par sous-population (moins de deux voisines) ou surpopulation (plus de trois voisines), mais survit avec deux ou trois voisines. Une cellule morte reprend vie si elle a exactement trois voisines vivantes. La première configuration est choisie manuellement, mais les suivantes se déduisent automatiquement. Le but est d’observer des évolutions surprenantes et complexes.

> [!Note]
> Pour en connaître un peu plus, vous pouvez visiter la page **[Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)** du jeu de la vie.

## Sommaire

- [**conwayGameOfLife**](#conwaygameoflife)
  - [Sommaire](#sommaire)
  - [Consignes](#consignes)
  - [Pré-requis](#pré-requis)
    - [Dépendances](#dépendances)
  - [Utilisations](#utilisations)
  - [Sauvegarde](#sauvegarde)
    - [Les entités](#les-entités)
  - [Exemples d'utilisations](#exemples-dutilisations)
    - [Aperçu](#aperçu)
    - [Remarque](#remarque)
  - [Licence](#licence)

## Consignes

La liste des consignes du sujet est disponible dans le [todo.md](todo.md)

[Sommaire](#sommaire)

## Pré-requis

L'installation de **[Python 3](https://www.python.org/downloads/)** est recommandé pour l'éxécution du script

> [!Note]
> Une fois l'installation de **[Python 3](https://www.python.org/downloads/)** terminée, tapez `$ pip install -r requirements.txt` dans un terminal à la racine du projets pour installer toutes les dépendances du projet

[Sommaire](#sommaire)

### Dépendances

- [base64](https://docs.python.org/3/library/base64.html)
- [concurrent.futures](https://docs.python.org/3/library/concurrent.futures.html)
- [json](https://docs.python.org/3/library/json.html)
- [keyboard](https://pypi.org/project/keyboard/) (For Windows system)
- [math](https://docs.python.org/3/library/math.html)
- [os](https://docs.python.org/3/library/os.html)
- [platform](https://docs.python.org/3/library/platform.html)
- [sys](https://docs.python.org/3/library/sys.html)
- [termios](https://docs.python.org/3/library/termios.html) (For Linux system)
- [tty](https://docs.python.org/3/library/tty.html) (For Linux system)
- [time](https://docs.python.org/3/library/time.html)
- [zlib](https://docs.python.org/3/library/zlib.html)

[Sommaire](#sommaire)

## Utilisations

Pour lancer le programme principal en mode interactif, tapez `$ python main.py` dans un terminal ouvert à la racine du projet, vous n'aurez plus qu'à choisir le nom de la map que vous voulez chargé et simulé.

Usage: `$ python main.py <argument>`

| Arguments            | Options | Values      | Descriptions                                 |
| -------------------- | ------- | ----------- | -------------------------------------------- |
| `-a`, `--add`        | -       | `<mapName>` | Insérer une ou plusieurs cellule(s)          |
| `-A`, `--add-entity` | -       | `<mapName>` | Insérer une entité                           |
| `-d`, `--display`    | -       | `<mapName>` | Afficher une map enregistrée                 |
| `-l`, `--list`       | -       | -           | Lister les maps sauvegardés                  |
| `-n`, `--new`        | -       | `<mapName>` | Créer une nouvelle map                       |
| `-r`, `--reset`      | -       | `<mapName>` | Réinitialiser une map                        |
| `-s`, `--start`      | `-t`    | `<mapName>` | Jouer une map, `-t` pour le rendu multicoeur |

[Sommaire](#sommaire)

## Sauvegarde

Les maps générées sont sauvegardées de manière automatique après chaque mise à jour de celle-ci ou arrêt de la simulation dans un fichier **.map** portant le nom de la map dans le répertoire **[saves](saves/)** (_exemple: **[world.map](saves/world.map)**_)

[Sommaire](#sommaire)

### Les entités

De même que pour les maps, les entités sont stockées dans le dossier **[entities](entities/)**

Si vous voulez ajouter des entités dans le fichier, vous pouvez le faire en suivant le formatage de positionnement relatif avec les coordonnées **x** et **y** comme dans l'exemple ci dessous pour l'entité "block":

```json
// block.json
{
  "block": "[(x, y), (x, y+1), (x+1, y), (x+1, y+1)]"
}
```

Depuis la version 2.4, les entités sont chargés de façon asynchrone de sorte à diminuer les temps de chargement lors d'ajouts d'entités ou du lancement de simulations

[Sommaire](#sommaire)

## Exemples d'utilisations

On génère une nouvelle map qu'on va appeller "world" avec `$ python main.py -n world 50 50`

On ajoute les cellules active de sorte à former une entité:

- **Bloc**: `$ python main.py -a world "[(2,1), (2,2), (3,1), (3,2)]"`
- **Grenouille**: `$ python main.py -a world "[(2,1), (3,1), (4,2), (3,4), (2,4), (1,3)]"`
- **Planeur**: `$ python main.py -a world "[(1,1), (2,2), (2,3), (3,1), (3,2)]"`

Et on lance le jeu avec `$ python main.py` en entrant le nom de la map que l'on souhaite charger, ou bien le jeu avec la map souhaitée en entrant `$ python main.py -s world` directement

[Sommaire](#sommaire)

### Aperçu

![aperçu](preview.gif)

[Sommaire](#sommaire)

### Remarque

- Vous pouvez checker votre configuration avec `$ python main.py -d world` pour afficher la map avec vos cellules actives
- Depuis la version 2.0, vous pouvez maintenant enregistrer une entité complète dans le dossier **[entities](entities)** et l'ajouter sur la map comme ceci:
  - **Départ de floraison**: `$ python main.py -A world flowering 25 25`
  - **Le clown**: `$ python main.py -A world clown 25 25`

> [!Tip]
> Si vous voulez entièrement la réinitialiser, `$ python main.py -r world` remet toutes les cellules d'une map à 0

[Sommaire](#sommaire)

## Licence

Code sous license [GPL v3](LICENSE)

[Sommaire](#sommaire)
