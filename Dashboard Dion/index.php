<html>
<head>
	<title>Dashboard Dion</title>
	<script src="js/jquery-1.11.1.min.js"></script>

	<script src="js/bootstrap.min.js"></script>

	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.css">
	<script src="https://cdnjs.cloudflare.com/ajax/libs/raphael/2.1.0/raphael-min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/morris.js/0.5.1/morris.min.js"></script>

	<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">

	<link rel=stylesheet href="css/styles.css">
</head>
<body>
	<nav class="navbar navbar-default">
		<div class="container-fluid">
			<div class="navbar-header">
				<a class="navbar-brand" href="#">Dashboard Dion</a>
			</div>
		</div>
	</nav>

	<div class="container">
		<div class="row">
			<div class="col-md-4">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title text-center">Aantal producten per website</h3>
					</div>
					<div class="panel-body">
						<div id="store-components" style="height:200px"></div>
					</div>
				</div>
			</div>
			<div class="col-md-4">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title text-center">Verdeling van componenten</h3>
					</div>
					<div class="panel-body">
						<div id="components" style="height:200px"></div>
					</div>
				</div>
			</div>
			<div class="col-md-4">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title text-center">Verdeling van merken</h3>
					</div>
					<div class="panel-body">
						<div id="brands" style="height:200px"></div>
					</div>
				</div>
			</div>			
		</div>
		<div class="row">
			<div class="col-md-12">
				<div class="panel panel-default">
					<div class="panel-heading">
						<h3 class="panel-title text-center">Per component: goedkoopste, duurste en gemiddelde prijs</h3>
					</div>
					<div class="panel-body">
						<div id="prices-components" style="height:200px"></div>
					</div>
				</div>
			</div>
		</div>
	</div>	

	<div id="bartest"></div>

	<?php	
	require('functions.php');
	
	query("MATCH (n:Component)-[r:SOLD_AT]->(s:Store) RETURN s.Name, COUNT(n)", 'donut-stores.twig');
	query("MATCH (n:Component) RETURN LABELS(n), COUNT(n)", 'donut-components.twig');
	query("MATCH (n:Component) WHERE n.Merk <> 'NULL' RETURN n.Merk, COUNT(n)", 'donut-brands.twig');
	query("MATCH (n:Component)-[r:SOLD_AT]->(s:Store) RETURN LABELS(n), MIN(r.Price), MAX(r.Price), AVG(r.Price)", 'bar.twig');	

	?>

</body>
</html>