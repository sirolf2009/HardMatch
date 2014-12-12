<?php
require('vendor/autoload.php');
require_once "HTML/Template/IT.php";

$client = new Everyman\Neo4j\Client('localhost', 7474);
$client->getTransport()->setAuth('username', 'password');

$tpl = new HTML_Template_IT("./templates");

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
	$nodeid = $_POST['node'];
	$node = $client->getNode($nodeid);

	global $tpl;
	$tpl->loadTemplatefile("tableinfo.html", true, true);
	$tpl->setVariable("ID", $nodeid);
	$tpl->setVariable("NAME", $node->getProperty('name'));
	$tpl->setVariable("DESC", $node->getProperty('description'));
	$tpl->setVariable("CAT", $node->getProperty('category'));
	$tpl->setVariable("INFO", $node->getProperty('info'));
	$tpl->show();
}


function componentOverview(){
	global $client;

	$processornode = $client->getNode($_POST['processorid']);
	$videokaartnode = $client->getNode($_POST['videokaartid']);

	if(!empty($_POST['processorid'])){
		addHtml($processornode);
	}
	if(!empty($_POST['videokaartid'])){
		addHtml($videokaartnode);
	}
	if(empty($_POST['videokaartid']) && empty($_POST['processorid'])){
		echo("Geen componenten gekozen");
	}
}

function compareComponents(){
	global $client;
	global $tpl;

	$ids = $_POST['nodeids'];
	$headers = "";
	$category = "";
	$description = "";
	$a = array();

	foreach($ids as $i){
		array_push($a,$client->getNode($i));
	}

	foreach ($a as $j){
		$headers .= '<th>'.$j->getProperty('name').'</th>';
		$category .= '<td>'.$j->getProperty('category').'</td>';
		$description .= '<td>'.$j->getProperty('description').'</td>';
	}

	$tpl->loadTemplatefile("comparetable.html", true, true);
	$tpl->setVariable("HEADER", $headers);
	$tpl->setVariable("CAT", $category);
	$tpl->setVariable("DESC", $description);
	$tpl->show();
}

function addHtml($node){
	$tpl = new HTML_Template_IT("./templates");

	switch ($node->getProperty('category')) {
		case 'videokaart':
		$description = $node->getProperty('name')."<p> ".$node->getProperty('description');
		break;

		default:
		$description = $node->getProperty('description');
		break;
	}

	$tpl->loadTemplatefile("overviewhtml.html", true, true);
	$tpl->setVariable("CAT", $node->getProperty('category'));
	$tpl->setVariable("NAME", $node->getProperty('name'));
	$tpl->setVariable("DESC", $node->getProperty('description'));
	$tpl->show();
}
?>