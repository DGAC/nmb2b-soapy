#!/bin/sh
echo "On actualise le fichier collection.py (zeep/xsd/types/collection.py)"
NBR_RESULTS=$(find ./venv -name collection.py | wc -l)
if [ $NBR_RESULTS != '1' ]; then
    echo "Impossible de trouver collection.py. Avez-vous bien installé la librairie Python Zeep ?"
    exit 1
fi
PATH_TO_ZEEP_COLLECTION=$(find . -name collection.py)
yes | cp -rf ./upgrade/collection_new.py $PATH_TO_ZEEP_COLLECTION
echo "Le fichier collection.py a bien été remplacé !"
exit 0