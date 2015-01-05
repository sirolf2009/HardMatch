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

// Not used yet - still in index.php
function getProcessors(){
	global $client;
	global $tpl;

	$queryString = "MATCH (n:Processor) RETURN n";
	$query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
	$result = $query->getResultSet();

	$tpl->loadTemplatefile("processor_table.html", true, true);

	foreach ($result as $row) {
		$tpl->setCurrentBlock("row") ;
		$tpl->setVariable("ID", $row['n']->getId()) ;
		$tpl->setVariable("NAME", $row['n']->getProperty('name')) ;
		$tpl->setVariable("DESC", $row['n']->getProperty('description')) ;
		$tpl->setVariable("PRICE", $row['n']->getProperty('price')) ;
		$tpl->parseCurrentBlock("row") ;
	}

	$tpl->show();
}


function getInfo(){
	global $client;
	global $twig;
	$nodeid = $_POST['node'];
	$node = $client->getNode($nodeid);

	$template = $twig->loadTemplate('tableinfo.twig');
    echo $template->render(array('node' => $node));
}


function componentOverview(){
	global $client;
	global $twig;

	$template = $twig->loadTemplate('overview-cart.twig');

	if(!empty($_POST['processorid'])){
		// addHtml($processornode);
		$processornode = $client->getNode($_POST['processorid']);
		echo $template->render(array('node' => $processornode));
	}
	if(!empty($_POST['videokaartid'])){
		// addHtml($videokaartnode);
		$videokaartnode = $client->getNode($_POST['videokaartid']);
		echo $template->render(array('node' => $videokaartnode));
	}
	if(empty($_POST['videokaartid']) && empty($_POST['processorid'])){
		echo("Geen componenten gekozen");
	}
}

function compareComponents(){
	global $client;
	global $twig;

	$ids = $_POST['nodeids'];
	$nodes = array();

	foreach($ids as $i){
		array_push($nodes,$client->getNode($i));
	}

	$template = $twig->loadTemplate('compare.twig');
    echo $template->render(array('nodes' => $nodes));
}
?>