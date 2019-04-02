# Jeu de dames

Pour exécuter le jeu, lancer le fichier main.py. (nécessite le module pygame)

L'invite de commande demande ensuite N (entier), puis une valeur pour "debug mode" (on peut la poser égale à 0 s'il s'agit simplement de tester le jeu).

Ensuite, le jeu avec les règles spécifiées s'exécute:
- La grille de dimension NxN s'affiche.
- Le joueur est amené à positionner sa première dame.
- Les ligne, colonne et diagonales associées se colorent en rouge
- Le joueur continue, mais ne peut plus placer sur les cases colorées/occupées par ses dames

Lorsque le joueur tente de placer une dame sur une case colorée, il reçoit un message d'avertissement.
Aussi, lorsque les N dames sont placées, il reçoit un message de victoire.
Si ce n'est pas le cas mais que les cases sont toutes colorées, il reçoit un message de défaite.

Le joueur peut à tout moment (après son premier tour) décider de revenir en arrière via le bouton en bas à gauche.
