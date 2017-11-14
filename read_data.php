<?php

require '/var/composer/vendor/autoload.php';

$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
$collection = new MongoDB\Collection($manager, 'walsh', 'fyp');

if(!empty($_POST['RSSI'])) {
	$rssi_value = $_POST['RSSI'];
	print("<p>" + $_POST['RSSI'] + "</p>");
	$sensor_value = 1;
		
	$ts = new MongoDB\BSON\UTCDateTime(new DateTime);
   	$data = ['RSSI'=>$rssi_value, 'Sensor'=> $sensor_value, 'time'=>$ts];
   	try {
      		$collection->insertOne($data);
  	} catch (\Exception $e) {
      		print("<p>Insert failed.</p>");
   	}
   	$filter = [];
   	$options = [
		'batchSize'=>1,
		'limit' =>1,
		'sort' => ['time' => -1]];
   	$query = new MongoDB\Driver\Query($filter, $options);
   	$cursor = $manager->executeQuery('walsh.fyp', $query);
   	print("<p>The contents of the collection walsh.fyp are:</p>");
   	print_r($cursor->toArray());
}
else {
	$ts = new MongoDB\BSON\UTCDateTime(new DateTime);
   	$filter = [];
	//$options=[];
   	$options = [
		'batchSize'=>1,
		'limit'=>1,
		'sort' => ['time' => -1]];
   	$query = new MongoDB\Driver\Query($filter, $options);
   	$cursor = $manager->executeQuery('walsh.fyp', $query);
   	print("<p>The contents of the collection walsh.fyp are:</p>");
   	$rssi_values[] = $cursor->toArray();
	print_r($rssi_values);
}
?>
<html>
	<p> This is hopefully going to work </p>
</html>
