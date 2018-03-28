<?php

require '/var/composer/vendor/autoload.php';

$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
$collection = new MongoDB\Collection($manager, 'walsh', 'fyp');

	// Set up MongoDB query to pull only the most recently added document
   	$filter = [];
   	$options = [
		'batchSize'=>1,
		'limit'=>1,
		'sort' => ['time' => (int)-1]];
   	$query = new MongoDB\Driver\Query($filter, $options);
	
	//Execute the query
   	$cursor = $manager->executeQuery('walsh.fyp', $query);
	
	$rssi = 'RSSI';
	$sensor = 'Sensor';
	// Analyse the resulting data and return the status
	foreach($cursor as $doc) {
		$obj->rssi = $doc->$rssi;
		$obj->us = $doc->$sensor;
		echo dataAnalysis($obj->rssi,$obj->us);
	}

function dataAnalysis($rssi,$us) {
	// Linear threshold values
	$rLimit = -80;
	$sLimit = 200;

	// Error statuses if device is not found
	if($rssi == 0) {
		return (int)-1;
	}
	if($us == 0) {
		return (int)-2;
	}
	//Check the data against the thresholds
	if(($rssi>$rLimit) & ($us<$sLimit)) {
		return (int)1;
	}
	else {
		return 0;
	}
}
?>
