<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta charset="utf-8">
  <title>HardMatch - PC-Builder</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

  <script src="js/jquery.min.js"></script>
  <script src="js/jquery.dataTables.min.js"></script>

  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js"></script>
  <script src="http://cdn.datatables.net/plug-ins/a5734b29083/integration/bootstrap/3/dataTables.bootstrap.js"></script>

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="http://cdn.datatables.net/plug-ins/a5734b29083/integration/bootstrap/3/dataTables.bootstrap.css">

  <script type="text/javascript">

    $(document).ready(function() {
    $('#itemTable').DataTable({
      "language": {
            "url": "dutch.json"
        }
    });
  } );

  </script>

		<!--[if lt IE 9]>
			<script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
      <![endif]-->
      <link href="css/styles.css" rel="stylesheet">
    </head>
    <body>
      <nav class="navbar navbar-static">
       <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="#" target="ext"><b>HardMatch</b></a>
          <a class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="glyphicon glyphicon-chevron-down"></span>
          </a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">  
            <li><a href="#">Home</a></li>
            <li><a href="#">PC-Builder</a></li>
          </ul>
          <ul class="nav navbar-right navbar-nav">
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="glyphicon glyphicon-search"></i></a>
              <ul class="dropdown-menu" style="padding:12px;">
                <form class="form-inline">
                  <button type="submit" class="btn btn-default pull-right"><i class="glyphicon glyphicon-search"></i></button><input type="text" class="form-control pull-left" placeholder="Search">
                </form>
              </ul>
            </li>
            <li class="dropdown">
              <a href="#" class="dropdown-toggle" data-toggle="dropdown"><i class="glyphicon glyphicon-user"></i> <i class="glyphicon glyphicon-chevron-down"></i></a>
              <ul class="dropdown-menu">
                <li><a href="#">Login</a></li>
                <li><a href="#">Profiel</a></li>
                <li class="divider"></li>
                <li><a href="#">Over</a></li>
              </ul>
            </li>
          </ul>
        </div>
      </div>
    </nav><!-- /.navbar -->

    <header class="masthead">
      <div class="container">
        <div class="row">
          <div class="col col-sm-3">
            <div class="well">Processor      
            </div>
          </div>
          <div class="col col-sm-3">
            <div class="well">Videokaart      
            </div>
          </div>
          <div class="col col-sm-3">
            <div class="well">Moederbord      
            </div>
          </div>
          <div class="col col-sm-3">
            <div class="well">Geheugen
            </div>
          </div>

          <div class="col col-sm-12">
            <div class="progress">

              <div class="progress">
                <div class="progress-bar progress-bar-striped" role="progressbar" aria-valuenow="60" aria-valuemin="0" aria-valuemax="100" style="width: 60%;">
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- Begin Body -->
    <div class="container">
     <div class="row">
  			<!-- <div class="col col-sm-3">
              	<div id="sidebar">
      			<ul class="nav nav-stacked">
                    <li><h3 class="highlight">Instellingen <i class="glyphicon glyphicon-cog pull-right"></i></h3></li>
                    <li><input class="form-control" type="text" placeholder="Verfijn zoekresultaten"></li>
                  	<li><a href="#">Link</a></li>
          			<li><a href="#">Link</a></li>
				</ul>
                <div class="accordion" id="accordion2">
                    <div class="accordion-group">
                        <div class="accordion-heading">
                            <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseOne">
                                Accordion
                            </a>
                        </div>
                        <div id="collapseOne" class="accordion-body collapse in">
                            <div class="accordion-inner">
                              <p>There is a lot to be said about RWD.</p>
                            </div>
                        </div>
                    </div>
                    <div class="accordion-group">
                            <div class="accordion-heading">
                                <a class="accordion-toggle" data-toggle="collapse" data-parent="#accordion2" href="#collapseTwo">
                                    Accordion
                                </a>
                            </div>
                            <div id="collapseTwo" class="accordion-body collapse">
                                <div class="accordion-inner">
                                  <p>Use @media queries or utility classes to customize responsiveness.</p>
                                </div>
                            </div>
                        </div>
               	</div>
               </div>
             </div>  --> 
             <div class="col col-sm-12">
              <div class="panel">
                <h1>Artikelen</h1>
                
                <hr>

                <div class="main">

                  <table id="itemTable" class="table table-bordered">
                    <thead>
                      <tr>
                        <th></th>
                        <th>Naam</th>
                        <th>Beschrijving</th>
                        <th>Gemiddelde Prijs</th>
                        <th>Acties</th>
                      </tr>
                    </thead>
                    <tbody>
                      <!-- <tr>
                        <td><img class="list-img center-block" ng-src="images/{{item.filename}}.jpg"></td>
                        <td>{{ item.name }}</td>
                        <td>{{ item.description }}</td>
                        <td>{{ item.price }}</td>
                        <td>Prijs</td>
                        <td><button type="button" class="btn btn-warning"><span class="glyphicon glyphicon-list-alt"></span></button>
                          <button type="button" class="btn btn-danger"><span class="glyphicon glyphicon-plus"></span></button></td>
                      </tr> -->


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
        echo "<tr><td><img class='list-img' src='images/". $row['n']->getProperty('filename') .".jpg'></td>".
        "<td>".$row['n']->getProperty('name')."</td>".
        "<td>".$row['n']->getProperty('description')."</td>".
        "<td>".$row['n']->getProperty('price')."</td>".
        "<td><button type='button' class='btn btn-warning'><span class='glyphicon glyphicon-list-alt'></span></button>".
              "<button type='button' class='btn btn-danger'><span class='glyphicon glyphicon-plus'></span></button></td></tr>";
      }

      ?>


                    </tbody>
                  </table>

                </div>

              </div>
            </div> 
          </div>
        </div>

        <!-- script references -->
        <script src="js/scripts.js"></script>
      </body>
      </html>