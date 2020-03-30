Description
-----------
Ce logiciel est un simple projet fabriqué en une journée en guise d'exemple de mes capacités informatique pour les différents établissements de ParcourSup.

Shopify Discount Bot est un programme écrit en Python pour Windows sous forme de TUI (Text-Based User Interface) et qui permet d'automatiser des tâches autour des sites web sous Shopify. 

Capacités:
- Lister les produits disponibles d'un site Shopify ainsi que leur prix
- Chercher automatiquement (en scrapping) via le site www.promocodes.com pour des codes de réductions disponibles pour les sites Shopify
- Automatiquement ajouter au panier et procéder au checkout d'un item d'un site Shopify afin de pouvoir vérifier le solde d'une carte cadeau/d'un bon de réduction.

Dépendances
-----------
- Python (>= 3.2)
- BeautifulSoup4 (>= 4.7.1)
- colorama (>= 0.4.1)
- tabulate (>= 0.8.3)
- lxml (>= 4.3.3)
- requests (>= 2.21.0)

Misc
----
Ce logiciel n'est pas particulèrement optimisé au delà du nécessaire, en conséquence son code peut être un peu "hacky" et la liste de dépendances aurait pu être fortement réduite.

De plus ce logiciel utilise les APIs Windows afin d'obtenir un meilleure rendu visuel en tant que TUI. De ce fait, il n'est pas optimisé ou conçu pour d'autre systèmes d'exploitation tel que Mac OS ou Linux. Les "graphismes textuels" en couleures on été conçu en utilisant le progiciel colorama autour du système d'exploitation Windows 10. Il est possible que les anciennes versions de Windows ne supporte pas/mal les couleurs TUI.

Même si il a été conçu en tant qu'exemple pour Parcoursup, ce logiciel est sous license MIT. Il est ouverte à toute copie ou modification de son code source
