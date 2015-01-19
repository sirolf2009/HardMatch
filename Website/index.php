<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta charset="utf-8">
  <title>HardMatch - PC-Builder Test</title>
  <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">

  <script src="js/jquery-1.11.1.min.js"></script>
  <script src="js/jquery.dataTables.min.js"></script>

  <script src="js/bootstrap.min.js"></script>
  <script src="js/dataTables.bootstrap.js"></script>

  <link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
  <link rel="stylesheet" type="text/css" href="css/dataTables.bootstrap.css">

  <link href="css/styles.css" rel="stylesheet">

  <script type="text/javascript">

  $(document).ready(function() {
    $('#motherboard, #cpu, #cpufan, #graphicscard')
    .DataTable({
      "language": {
        "url": "dutch.json"
      },
      "columnDefs": [ {
        "targets": [1,5],
        "orderable": false,
        "class":'details-control'
      } ]
    });

    $('#ram, #storage')
    .DataTable({
      "language": {
        "url": "dutch.json"
      },
      "columnDefs": [ {
        "targets": [1,4],
        "orderable": false,
        "class":'details-control'
      } ]
    });

    $('#case')
    .DataTable({
      "language": {
        "url": "dutch.json"
      },
      "columnDefs": [ {
        "targets": [1,6],
        "orderable": false,
        "class":'details-control'
      } ]
    });
  } );

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  </script>

    </head>

    <?php
    // require('vendor/autoload.php');
    // require('NodeExtension.php');

    // $client = new Everyman\Neo4j\Client('localhost', 7474);
    // $client->getTransport()->setAuth('username', 'password');

    // $loader = new Twig_Loader_Filesystem('./templates/');
    // $twig = new Twig_Environment($loader);
    // $twig->addExtension(new NodeExtension());
    ?>

    <body>
      <nav class="navbar navbar-static">
       <div class="container">
        <div class="navbar-header">
          <a class="navbar-brand" href="./" target="ext"><b>HardMatch</b></a>
          <a class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
            <span class="glyphicon glyphicon-chevron-down"></span>
          </a>
        </div>
        <div class="navbar-collapse collapse">
          <ul class="nav navbar-nav">  
            <li><a href="./">Home</a></li>
            <li><a href="#">PC-Builder</a></li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- /.navbar -->

    <div id="alerts">
    </div>

    <!-- Begin Body -->
    <div class="container">

      <!-- Modal -->
      <div class="modal fade" id="modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
              <h4 class="modal-title">Vergelijken</h4>
            </div>
            <div class="modal-body">
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Sluit</button>
            </div>
          </div>
        </div>
      </div>
      <!-- End Modal -->

      <section>
        <div class="board">
          <div class="board-inner">
            <ul class="nav nav-tabs" id="myTab">
              <div class="liner"></div>
              <li class="active">
               <a href="#home" data-toggle="tab" title="Home" id="homeTab">
                <span class="round-tabs one">
                  <i class="glyphicon glyphicon-home"></i>
                </span> 
              </a></li>

              <li><a href="#overzicht" data-toggle="tab" title="Overzicht" id="overzichtTab" class="disabledTab">
               <span class="round-tabs two">
                 <i class="glyphicon glyphicon-list"></i>
               </span> 
             </a>
           </li>
           <li><a href="#uitkomst" data-toggle="tab" title="Goedkoopste winkel" id="uitkomstTab" class="disabledTab">
             <span class="round-tabs three">
              <i class="glyphicon glyphicon-tag"></i>
            </span> </a>
          </li>

          <li><a href="#afronding" data-toggle="tab" title="Afronden" id="afrondingTab" class="disabledTab">
           <span class="round-tabs five">
            <i class="glyphicon glyphicon-ok"></i>
          </span> </a>
        </li>

      </ul></div>

      <div class="tab-content">
        <div class="tab-pane fade in active" id="home">

          <h3 class="head text-center">Selecteer uw componenten</h3>
          <p class="narrow text-center">
            Hier misschien nog wat tekst met uitleg etc.
          </p>

          <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
            <?php

            // $template = $twig->loadTemplate('panels/motherboard.twig');
            // $queryString = "MATCH (n:Motherboard) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $motherboardResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Moederbord', 'table' => 'motherboard', 'nodes' => $motherboardResult));

            // $template = $twig->loadTemplate('panels/cpu.twig');
            // $queryString = "MATCH (n:CPU) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $cpuResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Processor', 'table' => 'cpu', 'nodes' => $cpuResult));

            // $template = $twig->loadTemplate('panels/cpufan.twig');
            // $queryString = "MATCH (n:CPUFan) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $cpufanResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Processor Fan', 'table' => 'cpufan', 'nodes' => $cpufanResult));

            // $template = $twig->loadTemplate('panels/graphicscard.twig');
            // $queryString = "MATCH (n:GraphicsCard) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $graphicscardResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Videokaart', 'table' => 'graphicscard', 'nodes' => $graphicscardResult));

            // $template = $twig->loadTemplate('panels/ram.twig');
            // $queryString = "MATCH (n:RAM) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $ramResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Geheugen', 'table' => 'ram', 'nodes' => $ramResult));

            // $template = $twig->loadTemplate('panels/case.twig');
            // $queryString = "MATCH (n:Case) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $caseResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Behuizing', 'table' => 'case', 'nodes' => $caseResult));

            // $template = $twig->loadTemplate('panels/storage.twig');
            // $queryString = "MATCH (n:Storage) RETURN n";
            // $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
            // $storageResult = $query->getResultSet();
            // echo $template->render(array('name' => 'Opslag', 'table' => 'storage', 'nodes' => $storageResult));

            ?>
          </div>


          <p class="text-center">
            <a id="next1" href="#overzicht" class="btn btn-success btn-outline-rounded green nexttab">volgende stap<span style="margin-left:10px;" class="glyphicon glyphicon-arrow-right"></span></a>
          </p>
        </div>

        <div class="tab-pane fade" id="overzicht">
          <h3 class="head text-center">Overzicht</h3>
          <p class="narrow text-center">
            Een overzicht van alle geselecteerde componenten.
            <br>
            <div class="col-xs-12">
              <div class="panel panel-info">
                <div class="panel-heading">
                  <div class="panel-title">
                    <div class="row">
                      <div class="col-xs-6">
                        <h5><span class="glyphicon glyphicon-shopping-cart"></span> Winkelwagen</h5>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="panel-body overzicht-componenten">
                </div>
              </div>
            </div>
          </p>

          <p class="text-center">
            <a id="prev2" class="btn btn-success btn-outline-rounded green prevtab"><span style="margin-right:10px;" class="glyphicon glyphicon-arrow-left"></span>vorige stap</a>
            <a id="next2" href="#overzicht" id="nexttab" class="btn btn-success btn-outline-rounded green nexttab">volgende stap<span style="margin-left:10px;" class="glyphicon glyphicon-arrow-right"></span></a>
          </p>

        </div>

        <div class="tab-pane fade" id="uitkomst">
          <h3 class="head text-center">Goedkoopste winkels</h3>
          <p class="narrow text-center">
            Een lijst met alle geselecteerde componenten en de daarbij horende goedkoopste winkel.
          </p>

          <div class="gdk-winkel">
            <img src="./images/icons/processor.png" class="gdk-img">
            <div class="info">
              <div class="details">
                <div class="details-title">Productnaam</div>
                <p> Beschrijving
                </div>

                <div class="store">
                  <div class="store-title">Goedkoopste winkel</div>
                  <img src="./images/shops/alternate.png" class="store-img">
                </div>
              </div>
              <div class="extra">
                <div class="extra-info" data-toggle="tooltip" data-placement="bottom" title="Bekijk product op Alternate">
                  <span class="fa fa-globe"></span>
                  Website
                </div>

                <div class="extra-info" data-html="true" data-toggle="tooltip" data-placement="bottom" title="Voor 23.59 besteld,<br>morgen in huis.">
                  <span class="fa fa-check"></span>
                  Op Voorraad
                </div>

                <div class="extra-info" data-html="true" data-toggle="tooltip" data-placement="bottom" title="Betaalmogelijkheden:<br>
                  iDeal, PayPal, Creditcard">
                  <span class="fa fa-tag"></span>
                  €150,00
                </div>
              </div>
            </div>

            <div class="gdk-winkel">
              <img src="./images/icons/videokaart.png" class="gdk-img">
              <div class="info">
                <div class="details">
                  <div class="details-title">Productnaam</div>
                  <p> Beschrijving
                  </div>

                  <div class="store">
                    <div class="store-title">Goedkoopste winkel</div>
                    <img src="./images/shops/coolblue.png" class="store-img">
                  </div>
                </div>
                <div class="extra">
                  <a href="#">
                    <div class="extra-info" data-toggle="tooltip" data-placement="bottom" title="Bekijk product op Coolblue">
                      <span class="fa fa-globe"></span>
                      Website
                    </div>
                  </a>
                  <div class="extra-info" data-html="true" data-toggle="tooltip" data-placement="bottom" title="Voor 23.59 besteld,<br>morgen in huis.">
                    <span class="fa fa-check"></span>
                    Op Voorraad
                  </div>

                  <div class="extra-info" data-html="true" data-toggle="tooltip" data-placement="bottom" title="Betaalmogelijkheden:<br>
                    iDeal, PayPal, Creditcard">
                    <span class="fa fa-tag"></span>
                    €150,00
                  </div>
                </div>
              </div>

              <p class="text-center">
                <a id="prev3" class="btn btn-success btn-outline-rounded green prevtab"><span style="margin-right:10px;" class="glyphicon glyphicon-arrow-left"></span>vorige stap</a>
                <a id="next3" href="#overzicht" id="nexttab" class="btn btn-success btn-outline-rounded green nexttab">klaar<span style="margin-left:10px;" class="glyphicon glyphicon-arrow-right"></span></a>
              </p>
            </div>

            <div class="tab-pane fade" id="afronding">
              <h3 class="head text-center">Klaar</h3>
              <div class="text-center">
                <a id="prev4" class="btn btn-success btn-outline-rounded green prevtab"><span style="margin-right:10px;" class="glyphicon glyphicon-arrow-left"></span>vorige stap</a>
              </div> 
            </div>

            <div class="clearfix"></div>
          </div>

        </div>
      </section>

    </div>

    <script src="js/scripts.js"></script>
  </body>
  </html>