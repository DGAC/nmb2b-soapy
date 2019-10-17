#!/bin/sh
NBR_RESULTS=$(find ./cert -name '*.p12' | wc -l)
# NBR_RESULTS=$(find ./venv -name collection.py | wc -l)
if [ $NBR_RESULTS = '0' ]; then
    printf "Aucun fichier trouvé avec l'extension .p12 dans cert/"
    exit 1
elif [ $NBR_RESULTS -gt '1' ]; then
    printf "Il existe plusieurs fichiers avec l'extension .p12 dans cert/\nMerci de n'en laisser qu'un seul"
    exit 1
else
    FILE_NAME=$(find ./cert -name '*.p12')
    #FILE_NAME="${FULL_FILE_NAME%.*}"
    printf "Un fichier .p12 a bien été trouvé dans /cert.\nQuel est votre mot de passe ?\n"
    read PASSWORD
    printf "On créé maintenant les fichier crt.pem et key.pem.\n"
    #echo "openssl pkcs12 -in ${FILE_NAME} -passin=pass:${PASSWORD} -out ./cert/crt.pem -clcerts -nokeys"
    openssl pkcs12 -in ${FILE_NAME} -passin=pass:${PASSWORD} -out ./cert/crt.pem -clcerts -nokeys # pour le certificat
    openssl pkcs12 -in ${FILE_NAME} -passin=pass:${PASSWORD} -out ./cert/key.pem -nocerts -nodes  # pour la clé
fi

# filename=$(basename -- "$fullfile")
# extension="${filename##*.}"
# filename="${filename%.*}"
# b2bcert4dpa2019