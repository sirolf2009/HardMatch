<?php
require('vendor/autoload.php');
require('NodeExtension.php');

require_once __DIR__.'/lib/php/lib/Thrift/ClassLoader/ThriftClassLoader.php';
require_once 'Types.php';  
require_once 'MatcherPHPHandler.php';

use Thrift\ClassLoader\ThriftClassLoader;

use Thrift\Protocol\TBinaryProtocol;
use Thrift\Transport\TSocket;
use Thrift\Transport\THttpClient;
use Thrift\Transport\TBufferedTransport;
use Thrift\Exception\TProtocol; 
use Thrift\Exception\TTransport; 
use Thrift\Exception\TTransportException; 
use Thrift\Exception\TException; 

$myfile = fopen("neo4JPort.txt", "r") or die("Unable to open file!");
$port = fread($myfile,filesize("neo4JPort.txt"));
fclose($myfile);

$client = new Everyman\Neo4j\Client('149.210.188.74', $port);
$client->getTransport()->setAuth('username', 'password');

$loader = new Twig_Loader_Filesystem('./templates/');
$twig = new Twig_Environment($loader);
$twig->addExtension(new NodeExtension());

if(isset($_POST['action']) && !empty($_POST['action'])) {
	$action = $_POST['action'];
	switch($action) {
		case 'getInfo' : getInfo(); break;
		case 'componentOverview' : componentOverview(); break;
		case 'compareComponents' : compareComponents(); break;
		case 'thriftInfo' : getThriftInfo(); break;
		case 'checkCompatability' : checkCompatability(); break;
	}
}

function getInfo(){
	global $client;
	global $twig;
	$nodeid = $_POST['node'];
	$tableid = $_POST['table'];
	$node = $client->getNode($nodeid);

	$template = $twig->loadTemplate('tableinfo/'.$tableid.'.twig');

	echo $template->render(array('node' => $node));
}


function componentOverview(){
	global $client;
	global $twig;

	if(!empty($_POST['motherboardid'])){
		showComponent("motherboard", $_POST['motherboardid']);
	}
	if(!empty($_POST['cpuid'])){
		showComponent("cpu", $_POST['cpuid']);
	}
	if(!empty($_POST['cpufanid'])){
		showComponent("cpufan", $_POST['cpufanid']);
	}
	if(!empty($_POST['graphicscardid'])){
		showComponent("graphicscard", $_POST['graphicscardid']);
	}
	if(!empty($_POST['ramid'])){
		showComponent("ram", $_POST['ramid']);
	}
	if(!empty($_POST['caseid'])){
		showComponent("case", $_POST['caseid']);
	}
	if(!empty($_POST['storageid'])){
		showComponent("storage", $_POST['storageid']);
	}
	if(empty($_POST['motherboardid']) && empty($_POST['cpuid']) && empty($_POST['cpufanid']) && empty($_POST['graphicscardid']) && empty($_POST['ramid']) && empty($_POST['caseid']) && empty($_POST['storageid'])){
		echo("Geen componenten gekozen");
	}
}

function compareComponents(){
	global $client;
	global $twig;

	$ids = $_POST['nodeids'];
	$tableid = $_POST['table'];
	$nodes = array();

	foreach($ids as $i){
		array_push($nodes,$client->getNode($i));
	}

	$template = $twig->loadTemplate('compare/'.$tableid.'.twig');
	echo $template->render(array('nodes' => $nodes));
}

function getThriftInfo(){
	global $client;
	global $twig;
	$ids = $_POST['ids'];
	$nodes = array();
	$components = array();

	$template = $twig->loadTemplate('store.twig');

	foreach($ids as $i){
		array_push($components,$client->getNode($i)->getProperty("ModelID"));
	}

	$loader = new ThriftClassLoader();
	$loader->registerNamespace('Thrift', __DIR__ . '/lib/php/lib');
	$loader->register();

	try {
		$socket = new TSocket('149.210.188.74', 9090);
		$transport = new TBufferedTransport($socket, 1024, 1024);
		$protocol = new TBinaryProtocol($transport);
		$client = new MatcherPHPHandlerClient($protocol);

		$transport->open();

		$thriftOutput = $client->match($components);

		echo $template->render(array('components' => $thriftOutput));

	} catch (TTransportException $te) {
		print 'TTransportException: '.$te->getMessage()."\n";
	}catch (TException $tx) {
		print 'TException: '.$tx->getMessage()."\n";
	}
}

function checkCompatability(){
	global $twig;
	global $client;
	if(!empty($_POST['motherboardid']) && !empty($_POST['cpuid'])){
		getCompatability($_POST['motherboardid'],$_POST['cpuid'], "Het gekozen moederbord is niet compatibel met de gekozen processor");
	}

	if(!empty($_POST['motherboardid']) && !empty($_POST['ramid'])){
		getCompatability($_POST['motherboardid'],$_POST['ramid'], "Het gekozen moederbord is niet compatibel met het gekozen geheugen");
	}

	if(!empty($_POST['motherboardid']) && !empty($_POST['graphicscardid'])){
		getCompatability($_POST['motherboardid'],$_POST['graphicscardid'], "Het gekozen moederbord is niet compatibel met de gekozen videokaart");
	}

	if(!empty($_POST['motherboardid']) && !empty($_POST['caseid'])){
		getCompatability($_POST['motherboardid'],$_POST['caseid'], "Het gekozen moederbord is niet compatibel met de gekozen behuizing");
	}

	if(!empty($_POST['motherboardid']) && !empty($_POST['cpufanid'])){
		getCompatability($_POST['motherboardid'],$_POST['cpufanid'], "Het gekozen moederbord is niet compatibel met de gekozen processor fan");
	}

	if(!empty($_POST['cpuid']) && !empty($_POST['cpufanid'])){
		getCompatability($_POST['motherboardid'],$_POST['cpufanid'], "De gekozen processor is niet compatibel met de gekozen processor fan");
	}
}

function showComponent($component, $nodeid){
	global $client;
	global $twig;
	$template = $twig->loadTemplate('/cart/'.$component.'.twig');
	$node = $client->getNode($nodeid);
	echo $template->render(array('node' => $node));
}

function getCompatability($node1, $node2, $message){
	global $client;
	global $twig;
	$queryString = "START n=node(".$node1."), s=node(".$node2.") MATCH (n)-[r:COMPATABILITY]-(s) RETURN r.compatability";
	$query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
	$result = $query->getResultSet();

	$template = $twig->loadTemplate('compatability.twig');
	echo $template->render(array('results' => $result, 'message' => $message));
}
?>