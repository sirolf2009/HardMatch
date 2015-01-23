<?php
require('vendor/autoload.php');
require('NodeExtension.php');

$myfile = fopen("neo4JPort.txt", "r") or die("Unable to open file!");
$port = fread($myfile,filesize("neo4JPort.txt"));
fclose($myfile);

$client = new Everyman\Neo4j\Client('149.210.188.74', $port);
$client->getTransport()->setAuth('username', 'password');

$loader = new Twig_Loader_Filesystem('./templates/');
$twig = new Twig_Environment($loader);
$twig->addExtension(new NodeExtension());

function query($cypher, $template, $name, $table){
		global $client;
		global $twig;
		$query = new Everyman\Neo4j\Cypher\Query($client, $cypher);
		$result = $query->getResultSet();
		$template = $twig->loadTemplate($template);
		echo $template->render(array('nodes' => $result, 'name' => $name, 'table' => $table));
	}
?>