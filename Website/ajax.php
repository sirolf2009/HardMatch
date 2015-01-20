<?php
require('vendor/autoload.php');
require('NodeExtension.php');

$client = new Everyman\Neo4j\Client('localhost', 7474);
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
	}
}

function getInfo(){
	global $client;
	global $twig;
	$nodeid = $_POST['node'];
	$tableid = $_POST['table'];
	$node = $client->getNode($nodeid);

	if ($tableid == "motherboard"){
		$template = $twig->loadTemplate('tableinfo/motherboard.twig');    	
	} else if ($tableid == "cpu"){
		$template = $twig->loadTemplate('tableinfo/cpu.twig');
	} else if ($tableid == "cpufan"){
		$template = $twig->loadTemplate('tableinfo/cpufan.twig');
	} else if ($tableid == "graphicscard"){
		$template = $twig->loadTemplate('tableinfo/graphicscard.twig');
	} else if ($tableid == "ram"){
		$template = $twig->loadTemplate('tableinfo/ram.twig');
	} else if ($tableid == "case"){
		$template = $twig->loadTemplate('tableinfo/case.twig');
	} else if ($tableid == "storage"){
		$template = $twig->loadTemplate('tableinfo/storage.twig');
	}

	echo $template->render(array('node' => $node));
}


function componentOverview(){
	global $client;
	global $twig;

	if(!empty($_POST['motherboardid'])){
		$template = $twig->loadTemplate('/cart/motherboard.twig');
		$motherboardnode = $client->getNode($_POST['motherboardid']);
		echo $template->render(array('node' => $motherboardnode));
	}
	if(!empty($_POST['cpuid'])){
		$template = $twig->loadTemplate('/cart/cpu.twig');
		$cpunode = $client->getNode($_POST['cpuid']);
		echo $template->render(array('node' => $cpunode));
	}
	if(!empty($_POST['cpufanid'])){
		$template = $twig->loadTemplate('/cart/cpufan.twig');
		$cpufannode = $client->getNode($_POST['cpufanid']);
		echo $template->render(array('node' => $cpufannode));
	}
	if(!empty($_POST['graphicscardid'])){
		$template = $twig->loadTemplate('/cart/graphicscard.twig');
		$graphicscardnode = $client->getNode($_POST['graphicscardid']);
		echo $template->render(array('node' => $graphicscardnode));
	}
	if(!empty($_POST['ramid'])){
		$template = $twig->loadTemplate('/cart/ram.twig');
		$ramnode = $client->getNode($_POST['ramid']);
		echo $template->render(array('node' => $ramnode));
	}
	if(!empty($_POST['caseid'])){
		$template = $twig->loadTemplate('/cart/case.twig');
		$casenode = $client->getNode($_POST['caseid']);
		echo $template->render(array('node' => $casenode));
	}
	if(!empty($_POST['storageid'])){
		$template = $twig->loadTemplate('/cart/storage.twig');
		$storagenode = $client->getNode($_POST['storageid']);
		echo $template->render(array('node' => $storagenode));
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

	if ($tableid == "motherboard"){
		$template = $twig->loadTemplate('compare/motherboard.twig');    	
	} else if ($tableid == "cpu"){
		$template = $twig->loadTemplate('compare/cpu.twig');
	} else if ($tableid == "cpufan"){
		$template = $twig->loadTemplate('compare/cpufan.twig');
	} else if ($tableid == "graphicscard"){
		$template = $twig->loadTemplate('compare/graphicscard.twig');
	} else if ($tableid == "ram"){
		$template = $twig->loadTemplate('compare/ram.twig');
	} else if ($tableid == "case"){
		$template = $twig->loadTemplate('compare/case.twig');
	} else if ($tableid == "storage"){
		$template = $twig->loadTemplate('compare/storage.twig');
	}

	echo $template->render(array('nodes' => $nodes));
}
?>