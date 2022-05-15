import os
import re
import sys


from src.classes.R5_automate import Automate
from src.functions.R5_completion import completer, complement
from src.functions.R5_determinisation import determinize
from src.functions.R5_standardisation import standardize
from src.functions.R5_reconnaissance import reconnaissance


FORMAT_FICHIER = "R5-%d.txt"


# Génére les traces de test de chaque automate
def trace() -> None:
    for idAutomate in range(1, 45):
        with open(f"traces/R5-trace-{idAutomate}.txt", "w", encoding="utf-8") as f:
            sys.stdout = f
            print("\n\n===== LECTURE DE L'AUTOMATE =====")
            cheminFichier = "docs/" + (FORMAT_FICHIER % idAutomate)
            automate = Automate.readFile(cheminFichier)
            automate.display()

            print("\n\n===== DETERMINISATION ET COMPLEMENTARISATION =====")
            automate = determinize(automate)
            automate = completer(automate)
            automate.display()

            """
                print("\n\n===== MINIMISATION =====")
                """

            print("\n\n===== RECONNAISSANCE =====")
            reconnaissance(automate)

            print("\n\n===== RECONNAISSANCE LANGAGE COMPLEMENTAIRE =====")
            automate = complement(automate)
            automate.display()

            print("\n\n===== RECONNAISSANCE =====")
            reconnaissance(automate)

            print("\n\n===== STANDARDISATION =====")
            automate = standardize(automate)
            automate.display()

            print("\n\n===== RECONNAISSANCE =====")
            reconnaissance(automate)


def main() -> None:
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

            print("\n\n===== LECTURE DE L'AUTOMATE =====")
            cheminFichier = "docs/" + (FORMAT_FICHIER % idAutomate)
            automate = Automate.readFile(cheminFichier)
            automate.display()

            print("\n\n===== DETERMINISATION ET COMPLEMENTARISATION =====")
            automate = determinize(automate)
            automate = completer(automate)
            automate.display()

            """
            print("\n\n===== MINIMISATION =====")
            """

            print("\n\n===== RECONNAISSANCE =====")
            reconnaissance(automate)

            print("\n\n===== RECONNAISSANCE LANGAGE COMPLEMENTAIRE =====")
            automate = complement(automate)
            automate.display()

            print("\n\n===== RECONNAISSANCE =====")
            reconnaissance(automate)

            print("\n\n===== STANDARDISATION =====")
            automate = standardize(automate)
            automate.display()

            print("\n\n===== RECONNAISSANCE =====")
            reconnaissance(automate)
    except KeyboardInterrupt:
        print()
    print("Au revoir !")


if __name__ == "__main__":
    main()
    # trace()
