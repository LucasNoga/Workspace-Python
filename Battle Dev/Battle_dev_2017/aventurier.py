# coding=utf-8
Click on the following link to get the english version:
https://questionsacm.isograd.com/codecontest/pdf/adventurer.pdf

Objectif

C’est bien connu, il est dangereux de partir seul à l’aventure sans équipement. Avant d’aller explorer de lointaines contrées, votre première épreuve en tant qu’aventurier consiste ainsi à dérober une épée dans une salle au trésor piégée, puisqu’aucun vieux sage n’a bien voulu vous en donner une.

La salle au trésor est représentée par un quadrillage dont l’entrée se situe dans le coin supérieur gauche. L’épée se trouve dans le coin inférieur droit. Les cases sont soit des murs, soit des cases traversables, soit des cases piégées : le plancher s’effondre sous vos pieds quand vous marchez sur ces dernières. Heureusement, vous courez assez vite pour passer rapidement à la prochaine case de votre chemin et ne pas tomber avec le plancher, mais une fois que vous avez marché sur une telle case, elle devient infranchissable. Par conséquent, lorsque vous vous trouvez sur une case, vous pouvez donc vous déplacer sur l’une des 4 cases adjacentes du moment que ce soit une case traversable ou une case piégée sur laquelle vous n’êtes jamais passé.

Votre but est d’aller de l’entrée de la salle jusqu’à l’épée, et ensuite de revenir vivant à l’entrée. Vous pouvez traverser chaque case piégée au plus une fois au cours de votre aller-retour. On vous demande également de minimiser le nombre de cases piégées traversées sur votre chemin.

Indication : On attend un algorithme de complexité polynomiale dans le pire cas.


Données

Entrée

Ligne 1 : un entier N compris entre 3 et 20 représentant la taille de la carte (une grille carrée de dimension NxN).
Lignes 2 à N+1 : les lignes de la carte représentées par des chaînes de N caractères. Les caractères de la ligne sont soit # (mur), soit . (case traversable), soit ! (case piégée). Les cases de l’entrée et de l’épée, situées respectivement en haut à gauche et en bas à droite, seront toujours des cases traversables.

Sortie

Un entier, indiquant le nombre minimal de cases piégées à traverser pour pouvoir prendre l’épée et la ramener à l’entrée. S’il est possible d’atteindre l’épée mais pas de revenir vivant ensuite, renvoyez -1. S’il n’est pas possible d’atteindre l’épée, renvoyez -2.




<?php
/***************************************************************
#*
#*
#* Solution by Isograd
#*
#*
#*****************************************************************/
function dfs(&$input, &$map, $n, $fy, $fx, $m){
	$dds = array(array(1, 0), array(-1, 0), array(0, 1), array(0, -1));
	$acc = array();

	$stack = new SplStack();
	$stack->push(array($fy, $fx));
	$map[$fy][$fx] = $m;

	while(!$stack->isEmpty()){
		list($y, $x) = $stack->pop();

		foreach($dds as $d){
			$ny = $y+$d[0];
			$nx = $x+$d[1];
			if($nx>=0 && $ny>=0 && $nx<$n && $ny<$n && $input[$ny][$nx]!=='#')
				if($input[$ny][$nx]==='.' && $map[$ny][$nx]===-1){
					$map[$ny][$nx] = $m;
					$stack->push(array($ny, $nx));
				} else if($input[$ny][$nx]==='!')
					$acc[] = array($ny, $nx);
		}
	}

	return $acc;
}

function bellmanford(&$graph, $from, $to){
	$n = count($graph);
	$distance = array_fill(0, $n, INF);
	$distance[$from] = 0;
	$parent = array_fill(0, $n, -1);
	for($i=0; $i<$n-1; $i++)
		for($c=0; $c<$n; $c++)
			foreach($graph[$c] as $e)
				if($e[2]>0 && $distance[$c] + $e[1] < $distance[$e[0]]){
					$distance[$e[0]] = $distance[$c] + $e[1];
					$parent[$e[0]] = $c;
				}

	$rdist = $distance[$to];

	$path = array();
	while($to != -1){
		$path[] = $to;
		$to = $parent[$to];
	}

	return array(array_reverse($path), $rdist);
}

function solve($input){
	$dds = array(array(1, 0), array(-1, 0), array(0, 1), array(0, -1));
	$n = intval(array_shift($input));
	$map = array_fill(0, $n, array_fill(0, $n, -1));

	$c = 0;
	$graph = array();
	$type = array();

	for($y=0; $y<$n; $y++)
		for($x=0; $x<$n; $x++)
			if($input[$y][$x]==='.' && $map[$y][$x]===-1){
				$graph[] = array();
				$type[] = '.';
				$graph[$c] = dfs($input, $map, $n, $y, $x, $c);
				$c++;
			} else if($input[$y][$x]==='!'){
				$graph[] = array();
				$type[] = '!';
				$map[$y][$x] = $c;
				foreach($dds as $d){
					$ny = $y+$d[0];
					$nx = $x+$d[1];
					if($nx>=0 && $ny>=0 && $nx<$n && $ny<$n && $input[$ny][$nx]!=='#')
						$graph[$c][] = array($ny, $nx);
				}
				$c++;
			}

	$pc = 0;
	$twin = array();
	for($i=0; $i<$c; $i++)
		if($type[$i] === '!'){
			$twin[] = $c+$pc;
			$graph[] = array();
			$pc++;
		} else
			$twin[] = -1;

	for($i=0; $i<$c; $i++)
		if($type[$i] === '!'){
			$graph[$twin[$i]] = (array_map(function($v)use(&$map){ return array($map[$v[0]][$v[1]], 0, INF); }, $graph[$i]));
			$graph[$i] = array(array($twin[$i], 1, 1));
		} else
			$graph[$i] = (array_map(function($v)use(&$map){ return array($map[$v[0]][$v[1]], 0, INF); }, $graph[$i]));

	$target = $map[$n-1][$n-1];

	$r = bellmanford($graph, 0, $target);
	$path = $r[0];
	if($input[0][0]==='#' || $r[1] == INF)
		return -2;
	$cost = $r[1];

	for($i=0; $i<count($path)-1; $i++){
		$f = $path[$i];
		$t = $path[$i+1];
		for($j=0; $j<count($graph[$f]); $j++)
			if($graph[$f][$j][0] == $t)
				break;
		$graph[$f][$j][2] -= 1;
		$graph[$t][] = array($f, -$graph[$f][$j][1], 1);
	}

	$r = bellmanford($graph, 0, $target);
	$path = $r[0];
	if($r[1] == INF)
		return -1;
	$cost += $r[1];

	return $cost;
}

$input = [];
while ($f = stream_get_line(STDIN, 10000, PHP_EOL))
	$input[] = $f;
echo solve($input)."\n";
?>

