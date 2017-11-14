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
		'singleBatch'=>true,
		'projection'=> ['RSSI'=>1]];
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
		'singleBatch'=>true,
		'projection'=> ['RSSI'=>1],
		'sort' => ['ts' => 1]];
   	$query = new MongoDB\Driver\Query($filter, $options);
   	$cursor = $manager->executeQuery('walsh.fyp', $query);
   	//$cursor = $collection->find()->sort(array('ts'=> -1))->limit(1);
   	print("<p>The contents of the collection walsh.fyp are:</p>");
   	print_r($cursor->toArray());
}
?>
<html>
	<p> This is hopefully going to work </p>
</html>
