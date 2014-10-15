<html>
<head>
	<title>HardMatch</title>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
</head>
<body>
	<table class="table">
		<thead>
			<tr>
				<th>Naam</th>
			</tr>
		</thead>
		<tbody>
			<?php
			require('vendor/autoload.php');

			// Connecting to host:port
			$client = new Everyman\Neo4j\Client('localhost', 7474);
			$client->getTransport()
  			// ->useHttps()
			->setAuth('username', 'password');

			//print_r($client->getServerInfo());

			//Return all nodes
			$queryString = "MATCH n RETURN n";
			$query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
			$result = $query->getResultSet();

			foreach ($result as $row) {
    		//echo $row['n']->getProperty('name') . "<br>";
				echo "<tr><td>" . $row['n']->getProperty('name') . "</td></tr>";
			}

			?>
		</tbody>
	</table>

</body>
</html>