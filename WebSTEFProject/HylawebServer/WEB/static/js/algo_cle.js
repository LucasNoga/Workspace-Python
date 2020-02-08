//**************************************************************************************
// Fonction permettant de regarder si la cle de controle d'un num de recep est correcte
// L'algo utilise est la version ASCII
//**************************************************************************************
// Paramètres entrées
//		.num_recep : num recep (8 car) + cle controle (2 car)
// Valeur sortie
//		.booleen true si cle ASCII correcte
//**************************************************************************************
function verifie_cle_controle_ASCII(num_recep) {
    var num_pos;
    var cle;
    var long_recep;
    var i;
    var somme_ascii;

    //Si le num recep <> 10 caractères => pas de controle possible
    if ((num_recep.length != 10) && (num_recep.length != 14))
        return false;
    long_recep = num_recep.length - 2;
    // Decomposition du num recep
    num_pos = num_recep.substr(0, long_recep);
    cle = num_recep.substr(long_recep, 2);

    //Algo ASCII
    somme_ascii = 0;
    for (i = 0; i < long_recep; i++) {
        somme_ascii = somme_ascii + (num_pos.charCodeAt(i) * Math.pow(2, i + 1));
    }
    cle_calculee = somme_ascii % 97;
    return (cle_calculee == parseInt(cle, 10));
}
