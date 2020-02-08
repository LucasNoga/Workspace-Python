
A NETTRE EN PYTHON

$input = array();
while( $f = fgets( STDIN ) ) {
    $input[]= $f;
}
$size = $input[0];
	$center = ($size-1)/2;
	$result = array("value"=>-99999999, "x"=>0,"y"=>0);
	for($y=1;$y<=$size;$y++){
	    $input[$y] = explode(" ", $input[$y]);
	    for($x=0;$x<$size;$x++){
			$real_x = $x- $center;
			$real_y = $center+1-$y;
			if((int)$input[$y][$x]>(int)$result['value']){
				$result = array("value"=>$input[$y][$x], "x"=>$real_x,"y"=>$real_y);
			}elseif((int)$input[$y][$x]==(int)$result['value']){
				if((pow($real_x,2)+pow($real_y,2))<=(pow($result['x'],2)+pow($result['y'],2))){
					$result['x']=$real_x;
					$result['y']=$real_y;
				}
			}
		}
	}
	echo $result['x']." ".$result['y'];