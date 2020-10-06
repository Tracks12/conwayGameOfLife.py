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
