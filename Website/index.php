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
    $('#motherboard, #cpu, #cpufan, #graphicscard, #ram, #case, #storage')
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
  } );

  $(function () {
    $('[data-toggle="tooltip"]').tooltip()
  })

  </script>

</head>

<body>
  <nav 
  class="navbar navbar-static">
  <div class="container">
    <div class="navbar-header">
      <a class="navbar-brand" href="./" target="ext"><b>HardMatch</b></a>
      <a class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
        <span class="glyphicon glyphicon-chevron-down"></span>
      </a>
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
        Selecteer de gewenste componenten in de tabellen.
      </p>

      <div class="panel-group" id="accordion" role="tablist" aria-multiselectable="true">
        
        <?php
        
        require('functions.php');

        query("MATCH (n:Motherboard) RETURN n", "panels/motherboard.twig", "Moederbord", "motherboard");
        query("MATCH (n:CPU) RETURN n", "panels/cpu.twig", "Processor", "cpu");
        query("MATCH (n:CPUFan) RETURN n", "panels/cpufan.twig", "Processor Fan", "cpufan");
        query("MATCH (n:GraphicsCard) RETURN n", "panels/graphicscard.twig", "Videokaart", "graphicscard");
        query("MATCH (n:RAM) RETURN n", "panels/ram.twig", "Geheugen", "ram");
        query("MATCH (n:Case) RETURN n", "panels/case.twig", "Behuizing", "case");
        query("MATCH (n:Storage) RETURN n", "panels/storage.twig", "Opslag", "storage");

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
          <div class="compatability"></div>
          <br>
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
      <div class="thrift"></div>

          <p class="text-center">
            <a id="prev3" class="btn btn-success btn-outline-rounded green prevtab"><span style="margin-right:10px;" class="glyphicon glyphicon-arrow-left"></span>vorige stap</a>
            <a id="next3" href="#overzicht" id="nexttab" class="btn btn-success btn-outline-rounded green nexttab">klaar<span style="margin-left:10px;" class="glyphicon glyphicon-arrow-right"></span></a>
          </p>
        </div>

        <div class="tab-pane fade" id="afronding">
          <h3 class="head text-center">Afgerond</h3>
          <p class="narrow text-center">
            Bedankt voor het gebruikmaken van ons systeem. Veel plezier met uw resultaten!
          </p>          
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