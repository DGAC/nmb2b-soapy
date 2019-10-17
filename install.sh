#!/bin/sh
SEP="-----------------------------------------------------"

echo $SEP
echo "Version de Python trouvée : "
python3 -V

echo $SEP
echo "Création d'un environnement virtuel python pour soapy..."
python3 -m venv venv
source venv/bin/activate
echo "...terminé."

echo $SEP
echo "Mise à jour de pip et installation des dépendances..."
pip --quiet install --upgrade pip
pip --quiet install -r requirements.txt
echo "...terminé."

echo $SEP
echo "Mise à jour du fichier collection.py (zeep/xsd/types/collection.py)..."
NBR_RESULTS=$(find ./venv -name collection.py | wc -l)
if [ $NBR_RESULTS != '1' ]; then
    echo "Impossible de trouver collection.py. Avez-vous bien installé la librairie Python Zeep ?"
    exit 1
fi
PATH_TO_ZEEP_COLLECTION=$(find . -name collection.py)
yes | cp -rf ./upgrade/collection_new.py $PATH_TO_ZEEP_COLLECTION
echo "...terminé."

echo $SEP
echo "L'installation de soapy est terminée !"
exit 0