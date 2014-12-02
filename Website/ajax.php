<?php
require('vendor/autoload.php');

if(isset($_POST['action']) && !empty($_POST['action'])) {
	$action = $_POST['action'];
	switch($action) {
		case 'getInfo' : getInfo(); break;
		case 'componentOverview' : componentOverview(); break;
		case 'compareComponents' : compareComponents(); break;
	}
}

function getProcessors(){
	$queryString = "MATCH (n:Processor) RETURN n";
	$query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
	$result = $query->getResultSet();

	$client->getNode($id);

	foreach ($result as $row) {
		echo "<tr><td class='hidden'>".$row['n']->getId()."</td>".
		"<td>".$row['n']->getProperty('name')."</td>".
		"<td>".$row['n']->getProperty('description')."</td>".
		"<td>".$row['n']->getProperty('price')."</td>".
		"<td><button type='button' class='btn btn-warning'><span class='glyphicon glyphicon-list-alt'></span></button>".
		"<button type='button' class='btn btn-danger'><span class='glyphicon glyphicon-plus'></span></button></td></tr>";
	}
}

function getInfo(){
	$client = new Everyman\Neo4j\Client('localhost', 7474);
	$client->getTransport()
	->setAuth('username', 'password');

	$nodeid = $_POST['node'];
	$node = $client->getNode($nodeid);

	echo'<td><table border="0">'.
	'<tr><td style="width:150px">Node id:</td>'.
	'<td>'.$nodeid.'</td>'.
	'</tr><tr><td>Naam:</td>'.
	'<td>'.$node->getProperty('name').'</td>'.
	'</tr><tr><td>Omschrijving:</td>'.
	'<td>'.$node->getProperty('description').'</td>'.
	'</tr><tr><td>Categorie:</td>'.
	'<td>'.$node->getProperty('category').'</td>'.
	'</tr><tr><td>Info:</td>'.
	'<td>'.$node->getProperty('info').'</td>'.
	'</tr></table></td>';
}


function componentOverview(){
	$client = new Everyman\Neo4j\Client('localhost', 7474);
	$client->getTransport()
	->setAuth('username', 'password');

	$videokaartnode = $client->getNode($_POST['videokaartid']);
	$processornode = $client->getNode($_POST['processorid']);
	$html = "";

	if($_POST['videokaartid'] != ""){
		$html .= addHtml($videokaartnode);
	}

	if($_POST['processorid'] != ""){
		$html .= addHtml($processornode);
	}

	if($_POST['videokaartid']=="" && $_POST['processorid']==""){
		$html = "Geen componenten gekozen";
	}

	echo $html;
}

function compareComponents(){
	$client = new Everyman\Neo4j\Client('localhost', 7474);
	$client->getTransport()
	->setAuth('username', 'password');

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

	echo '<table class="table table-hover table-bordered">'.
	'<thead><tr><th class="compare-table"></th>'.$headers.'</tr></thead><tbody>'.
	'<tr><td class="compare-table">Categorie </td>'.$category.'</tr>'.
	'<tr><td class="compare-table">Info </td>'.$description.'</tr>'.
	'</tbody></table>';
}

function addHtml($node){
	switch ($node->getProperty('category')) {
		case 'videokaart':
		$description = $node->getProperty('name')."<p> ".$node->getProperty('description');
		break;

		default:
		$description = $node->getProperty('description');
		break;
	}

	echo '<div id="'.$node->getProperty('category').'">'.
	'<div class="row component"><div class="overview-icon col-md-1">'.
	'<img class="img-responsive" src="./images/icons/'.$node->getProperty('category').'.png">'.
	'</div><div class="col-md-10">'.
	'<h4 class="product-name"><strong>'.$node->getProperty('name').'</strong></h4>'.
	'<h4><small>'.$description.'</small></h4>'.
	'</div><div class="overview-delete col-md-1">'.
	'<button type="button" class="btn btn-link delete-component" id="'.$node->getProperty('category').'Button"><span class="glyphicon glyphicon-trash"></span>'.
	'</button></div></div><hr></div>';
}
?>