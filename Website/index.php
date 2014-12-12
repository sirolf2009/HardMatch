<html lang="en">
<head>
  <meta http-equiv="content-type" content="text/html; charset=UTF-8">
  <meta charset="utf-8">
  <title>HardMatch - PC-Builder</title>
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
    $('#processors').DataTable({
      "language": {
        "url": "dutch.json"
      },
      "columnDefs": [ {
        "targets": [1,5],
        "orderable": false,
        "class":'details-control'
      } ]
    });
    $('#videokaarten').DataTable({
      "language": {
        "url": "dutch.json"
      },
      "columnDefs": [ {
        "targets": [1,5],
        "orderable": false,
        "class":'details-control'
      } ]
    });
  } );

  </script>

		<!--[if lt IE 9]>
			<script src="//html5shim.googlecode.com/svn/trunk/html5.js"></script>
      <![endif]-->
    </head>

    <?php
    ini_set('display_errors',1);
    require_once "HTML/Template/IT.php";
    require('vendor/autoload.php');

    $client = new Everyman\Neo4j\Client('localhost', 7474);
    $client->getTransport()
    ->setAuth('username', 'password');
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
            <div class="panel panel-default">
              <div class="panel-heading" role="tab" id="headingOne">
                <h4 class="panel-title">
                  <a class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseOne" aria-expanded="false" aria-controls="collapseOne">
                    Processor
                  </a>
                </h4>
              </div>
              <div id="collapseOne" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingOne">
                <div class="panel-body">
                  <?php                      
                  $tpl = new HTML_Template_IT("./templates");

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

                  ?>
                </div>
              </div>
            </div>

            <div class="panel panel-default">
              <div class="panel-heading" role="tab" id="headingTwo">
                <h4 class="panel-title">
                  <a class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo">
                    Videokaart
                  </a>
                </h4>
              </div>
              <div id="collapseTwo" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingTwo">
                <div class="panel-body">
                  <?php
                  $tpl = new HTML_Template_IT("./templates");

                  $queryString = "MATCH (n:Videokaart) RETURN n";
                  $query = new Everyman\Neo4j\Cypher\Query($client, $queryString);
                  $result = $query->getResultSet();

                  $tpl->loadTemplatefile("videokaart_table.html", true, true);

                  foreach ($result as $row) {
                    $tpl->setCurrentBlock("row") ;
                    $tpl->setVariable("ID", $row['n']->getId()) ;
                    $tpl->setVariable("NAME", $row['n']->getProperty('name')) ;
                    $tpl->setVariable("DESC", $row['n']->getProperty('description')) ;
                    $tpl->setVariable("PRICE", $row['n']->getProperty('price')) ;
                    $tpl->parseCurrentBlock("row") ;
                  }

                  $tpl->show();

                  ?>
                </div>
              </div>
            </div>
            <div class="panel panel-default">
              <div class="panel-heading" role="tab" id="headingThree">
                <h4 class="panel-title">
                  <a class="collapsed" data-toggle="collapse" data-parent="#accordion" href="#collapseThree" aria-expanded="false" aria-controls="collapseThree">
                    Geheugen
                  </a>
                </h4>
              </div>
              <div id="collapseThree" class="panel-collapse collapse" role="tabpanel" aria-labelledby="headingThree">
                <div class="panel-body">
                  Geheugen  
                </div>
              </div>
            </div>
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
<!--                 <div class="panel-footer">
                  <div class="row text-center">
                    <div class="col-xs-4">
                      <button type="button" class="btn btn-success btn-block">
                        Verder
                      </button>
                    </div>
                  </div>
                </div> -->
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