#!/bin/sh
NBR_RESULTS=$(find ./cert -name '*.p12' | wc -l)
if [ $NBR_RESULTS = '0' ]; then
    printf "Aucun fichier trouvé avec l'extension .p12 dans cert/\n"
    exit 1
elif [ $NBR_RESULTS -gt '1' ]; then
    printf "Il existe plusieurs fichiers avec l'extension .p12 dans cert/\nMerci de n'en laisser qu'un seul"
    exit 1
else
    FILE_NAME=$(find ./cert -name '*.p12')
    printf "Un fichier .p12 a bien été trouvé dans /cert.\nQuel est votre mot de passe ?\n"
    read PASSWORD
    printf "On créé maintenant les fichier crt.pem et key.pem.\n"
    openssl pkcs12 -in ${FILE_NAME} -passin=pass:${PASSWORD} -out ./cert/crt.pem -clcerts -nokeys # pour le certificat
    openssl pkcs12 -in ${FILE_NAME} -passin=pass:${PASSWORD} -out ./cert/key.pem -nocerts -nodes  # pour la clé
    printf "Fichiers créés avec succès"
fi