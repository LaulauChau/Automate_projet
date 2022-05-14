import os
import re


from src.classes.automate import Automate
from src.functions.completion import completer, complement
from src.functions.determinisation import determinize
from src.functions.standardisation import standardize
from src.functions.reconnaissance import reconnaissance


FORMAT_FICHIER = "BN3-%d.txt"


def main():
    automateAs = set()
    for file in os.listdir("docs"):
        if match := re.match(FORMAT_FICHIER.replace(r"%d", r"(\d+)"), file):
            automateAs.add(int(match[1]))

    listeAutomate = ", ".join(map(str, sorted(automateAs)))

    try:
        while True:
            idAutomate = None
            while idAutomate is None or idAutomate not in automateAs:
                if idAutomate is not None:
                    idAutomate = input("L'ID est invalide : ")
                else:
                    idAutomate = input(f"Entrez l'ID de l'automate {listeAutomate} : ")

                try:
                    idAutomate = int(idAutomate)
                except ValueError:
                    if idAutomate.lower() in ["quitter", "q"]:
                        break

            if idAutomate not in automateAs:
                break

            print()
            print("-1. Lecture de l'automate :")
            cheminFichier = "docs/" + (FORMAT_FICHIER % idAutomate)
            automate = Automate.readFile(cheminFichier)
            automate.display()

            print()
            print("-2. Déterminisation et complémentarisation de l'automate :")
            automate = determinize(automate)
            automate = completer(automate)
            automate.display()

            """
            print()
            print("-3. Minimisation de l'automate :")
            """

            print()
            print("-4. Reconnaissance du mot :")
            reconnaissance(automate)

            print()
            print(
                "-5. Création d'un automate qui reconnaît le langage complémentaire :"
            )
            automate = complement(automate)
            automate.display()

            print()
            print("-6. Reconnaissance du mot :")
            reconnaissance(automate)

            print()
            print("-7. Standardisation de l'automate :")
            automate = standardize(automate)
            automate.display()

            print()
            print("-8. Reconnaissance du mot :")
            reconnaissance(automate)
    except KeyboardInterrupt:
        print()
    print("Au revoir !")


if __name__ == "__main__":
    main()
