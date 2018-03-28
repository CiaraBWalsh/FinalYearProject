<?php

require '/var/composer/vendor/autoload.php';

$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
$collection = new MongoDB\Collection($manager, 'walsh', 'fyp');

   	$filter = [];
   	$options = [
		'batchSize'=>1,
		'limit'=>1,
		'sort' => ['time' => (int)-1]];
   	$query = new MongoDB\Driver\Query($filter, $options);
   	$cursor = $manager->executeQuery('walsh.fyp', $query);
	$rssi = 'RSSI';
	$sensor = 'Sensor';
	foreach($cursor as $doc) {
		$obj->rssi = $doc->$rssi;
		$obj->us = $doc->$sensor;
		echo dataAnalysis($obj->rssi,$obj->us);
	}

function dataAnalysis($rssi,$us) {
	$rLimit = -80;
	$sLimit = 200;
	if($rssi == 0) {
		return (int)-1;
	}
	if($us == 0) {
		return (int)-2;
	}
	if(($rssi>$rLimit) & ($us<$sLimit)) {
		return (int)1;
	}
	else {
		return 0;
	}
}
?>
