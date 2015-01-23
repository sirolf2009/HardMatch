<?php
require('vendor/autoload.php');
$client = new Everyman\Neo4j\Client('149.210.188.74', 7474);
$client->getTransport()->setAuth('username', 'password');
$loader = new Twig_Loader_Filesystem('./templates/');
$twig = new Twig_Environment($loader);


function query($cypher, $template){
	global $client;
	global $twig;
	$query = new Everyman\Neo4j\Cypher\Query($client, $cypher);
	$result = $query->getResultSet();
	$template = $twig->loadTemplate($template);
	echo $template->render(array('stores' => $result));
}
?>