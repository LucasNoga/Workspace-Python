# Enoncé
#
# Vous allez recevoir des fichiers composés d’une séquence de nombres entiers strictement positifs écrits en hexadécimal
# (chiffres entre 0 et F), séparés par des espaces. Ces nombres sont des identifiants de requêtes et
# une session est composée d’une suite de requêtes dont les identifiants sont des nombres consécutifs.
# Par exemple, la séquence "1 2 9 A B 11 3 4 5" correspond aux sessions "1 2", "9 A B", "11" et "3 4 5".
#
# Vous devez réaliser un programme qui lit un tel jeu de données sur l’entrée standard et écrit sur
# la sortie standard la suite d’identifiants correspondant à la session la plus longue (en nombre de requêtes).
# En cas d’égalité entre plusieurs sessions de même taille, vous retournerez la première session à apparaître dans le jeu de données.
#
#
# Format des données
#
# Entrée
# Une ligne composée d’une séquence de nombres entiers strictement positifs, en écriture hexadécimale
# (sans préfixe particulier) le premier chiffre étant donc entre ’1’ et ’F’ et les éventuels autres chiffres entre ’0’ et ’F’.
# Ces nombres sont séparés par le caractère "espace".
#
# Sortie
# Une ligne composée de la sous-séquence de nombres entiers strictement positifs consécutifs (la plus longue, cf. énoncé),
# en écriture hexadécimale (sans préfixe particulier) le premier chiffre étant donc entre ’1’ et ’F’ et les éventuels
# autres chiffres entre ’0’ et ’F’. Ces nombres sont séparés par le caractère "espace".




A METTRE EN PYTHON
<?php
while( $f = fgets( STDIN ) ) {
   	$values = explode(" ", $f);
	$prev = $values[0];
	$sequences =array();
	$current_string = $prev;
	foreach($values as $value){
		if(hexdec($value) == hexdec($prev)+1){
			$current_string .=" ".$value;
		}else{
			$sequences[]= $current_string;
			$current_string = $value;
		}
		$prev = $value;
	}
	$sequences[]=$current_string;
	$top_sequence = $sequences[0];
	foreach($sequences as $thesequence){
		if(count(explode(" ",$thesequence))>count(explode(" ",$top_sequence))){
			$top_sequence = $thesequence;
		}
	}
	echo $top_sequence;
}
?>