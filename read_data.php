<?php

require '/var/composer/vendor/autoload.php';

$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
$collection = new MongoDB\Collection($manager, 'walsh', 'fyp');

   	$filter = [];
   	$options = [
		'batchSize'=>1,
		'limit'=>1,
		'sort' => ['time' => -1]];
   	$query = new MongoDB\Driver\Query($filter, $options);
   	$cursor = $manager->executeQuery('walsh.fyp', $query);
   	print("<p>The contents of the collection walsh.fyp are:</p>");
	$rssi = 'RSSI';
	$sensor = 'Sensor';
	foreach($cursor as $doc) {
		print("RSSI ");
		print($doc->$rssi);
		print("\nDistance Sensor ");
		print($doc->$sensor);
	}
?>
