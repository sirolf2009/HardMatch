var motherboardSelect = "";
var cpuSelect = "";
var cpufanSelect = "";
var graphicscardSelect = "";
var ramSelect = "";
var caseSelect = "";
var storageSelect = "";

var motherboardCompare = [];
var cpuCompare = [];
var cpufanCompare = [];
var graphicscardCompare = [];
var ramCompare = [];
var caseCompare = [];
var storageCompare = [];

$(document).ready(function() {
    var motherboard = $('#motherboard').DataTable();
    var cpu = $('#cpu').DataTable();
    var cpufan = $('#cpufan').DataTable();
    var graphicscard = $('#graphicscard').DataTable();
    var ram = $('#ram').DataTable();
    var cases = $('#case').DataTable();
    var storage = $('#storage').DataTable();

    $('tbody').on('click', '.btn-warning', function() {
        var tr = $(this).closest('tr');
        var tableid = $(this).closest('table').attr('id');
        var id = tr.find("td:first").text();
        var row;

        if (tableid == "motherboard") {
            row = motherboard.row(tr);
        } else if (tableid == "cpu") {
            row = cpu.row(tr);
        } else if (tableid == "cpufan") {
            row = cpufan.row(tr);
        } else if (tableid == "graphicscard") {
            row = graphicscard.row(tr);
        } else if (tableid == "ram") {
            row = ram.row(tr);
        } else if (tableid == "case") {
            row = cases.row(tr);
        } else if (tableid == "storage") {
            row = storage.row(tr);
        };

        if (row.child.isShown()) {
            row.child.hide();
        } else {
            row.child(getInfo(id, tableid)).show();
            tr.next('tr').addClass('more-info');
        }
    });

    $('.overzicht-componenten').on('click', '.delete-component', function(event) {
        var button = ($(this).attr('id'));

        if (button == "motherboardButton"){
            motherboardSelect = "";
            $("#motherboard").find("tr").removeClass("info");
            $('#motherboard-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        } else if(button == "cpuButton"){
            cpuSelect = "";
            $("#cpu").find("tr").removeClass("info");
            $('#cpu-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        } else if(button == "cpufanButton"){
            cpufanSelect = "";
            $("#cpufan").find("tr").removeClass("info");
            $('#cpufan-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        } else if(button == "graphicscardButton"){
            graphicscardSelect = "";
            $("#graphicscard").find("tr").removeClass("info");
            $('#graphicscard-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        } else if(button == "ramButton"){
            ramSelect = "";
            $("#ram").find("tr").removeClass("info");
            $('#ram-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        } else if(button == "caseButton"){
            caseSelect = "";
            $("#case").find("tr").removeClass("info");
            $('#case-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        } else if(button == "storageButton"){
            storageSelect = "";
            $("#storage").find("tr").removeClass("info");
            $('#storage-item').slideUp(function() {
                $("div.overzicht-componenten").html(componentsOverview());
            });
        }
    });
});

$('.vergelijkButton').click(function() {
    var tableid = $(this).closest('table').attr('id');

    if (motherboardCompare.length >= 2 && tableid == "motherboard") {
        $('.modal-body').html(compareComponents(motherboardCompare, tableid));
        $('#modal').modal('show');
    } else if (cpuCompare.length >= 2 && tableid == "cpu") {
        $('.modal-body').html(compareComponents(cpuCompare, tableid));
        $('#modal').modal('show');
    } else if (cpufanCompare.length >= 2 && tableid == "cpufan") {
        $('.modal-body').html(compareComponents(cpufanCompare, tableid));
        $('#modal').modal('show');
    } else if (graphicscardCompare.length >= 2 && tableid == "graphicscard") {
        $('.modal-body').html(compareComponents(graphicscardCompare, tableid));
        $('#modal').modal('show');
    } else if (ramCompare.length >= 2 && tableid == "ram") {
        $('.modal-body').html(compareComponents(ramCompare, tableid));
        $('#modal').modal('show');
    } else if (caseCompare.length >= 2 && tableid == "case") {
        $('.modal-body').html(compareComponents(caseCompare, tableid));
        $('#modal').modal('show');
    } else if (storageCompare.length >= 2 && tableid == "storage") {
        $('.modal-body').html(compareComponents(storageCompare, tableid));
        $('#modal').modal('show');
    } else {
        addAlert("danger", "U moet minimaal twee producten selecteren om te kunnen vergelijken.")
    }
});

$('.table-checkbox').change(function() {
    var tableid = $(this).closest('table').attr('id');
    var nodeid = $(this).closest('tr').find("td:first").text();

    if (this.checked) {
        if (tableid == "motherboard") {
            motherboardCompare.push(nodeid);
        } else if (tableid == "cpu") {
            cpuCompare.push(nodeid);
        } else if (tableid == "cpufan") {
            cpufanCompare.push(nodeid);
        } else if (tableid == "graphicscard") {
            graphicscardCompare.push(nodeid);
        } else if (tableid == "ram") {
            ramCompare.push(nodeid);
        } else if (tableid == "case") {
            caseCompare.push(nodeid);
        } else if (tableid == "storage") {
            storageCompare.push(nodeid);
        }

    } else {
        if (tableid == "motherboard") {
            var i = motherboardCompare.indexOf(nodeid);
            motherboardCompare.splice(i, 1);
        } else if (tableid == "cpu") {
            var i = cpuCompare.indexOf(nodeid);
            cpuCompare.splice(i, 1);
        } else if (tableid == "cpufan") {
            var i = cpufanCompare.indexOf(nodeid);
            cpufanCompare.splice(i, 1);
        } else if (tableid == "graphicscard") {
            var i = graphicscardCompare.indexOf(nodeid);
            graphicscardCompare.splice(i, 1);
        } else if (tableid == "ram") {
            var i = ramCompare.indexOf(nodeid);
            ramCompare.splice(i, 1);
        } else if (tableid == "case") {
            var i = caseCompare.indexOf(nodeid);
            caseCompare.splice(i, 1);
        } else if (tableid == "storage") {
            var i = storageCompare.indexOf(nodeid);
            storageCompare.splice(i, 1);
        }
    }
});

$('tbody').on('click', '.btn-success', function() {
    var row = $(this).closest('tr');
    var nodeid = row.find("td:first").text();
    var tableid = $(this).closest('table').attr('id');
    row.addClass('info').siblings().removeClass('info');

    if (tableid == "motherboard") {        
        motherboardSelect = nodeid;
    } else if (tableid == "cpu") {        
        cpuSelect = nodeid;
    } else if (tableid == "cpufan") {        
        cpufanSelect = nodeid;
    } else if (tableid == "graphicscard") {
        graphicscardSelect = nodeid;
    } else if (tableid == "ram") {
        ramSelect = nodeid;
    } else if (tableid == "case") {
        caseSelect = nodeid;
    } else if (tableid == "storage") {
        storageSelect = nodeid;
    }
})

$('.nexttab').click(function() {
    var id = $(this).attr('id');
    if (id == "next1") {
        $("div.overzicht-componenten").html(componentsOverview());
    } else if (id == "next2") {
        if (motherboardSelect == "" && cpuSelect == "" && cpufanSelect == "" && graphicscardSelect == "" && ramSelect == "" && caseSelect == "" && storageSelect == "") {
            addAlert('danger', 'U moet minimaal één component kiezen om verder te gaan.');
            return;
        }
    }
    $('.nav-tabs > .active').next('li').find('a').trigger('click');
});

$('.prevtab').click(function() {
    $('.nav-tabs > .active').prev('li').find('a').trigger('click');
});

$('#myTab li a').click(function(e) {
    e.preventDefault();
    $(this).parent().nextAll('li').find('a').addClass('disabledTab');
    $(this).parent().prevAll('li').find('a').removeClass('disabledTab');
});

$(function() {
    $('#alerts').hide();
    $('#alerts').on('click', '.close', function(event) {
        $('#alerts').slideUp();
    });
});

function addAlert(type, message) {
    $('#alerts').html(
        '<div class="alert alert-' + type + ' page-alert"><div class="container"><button type="button" class="close">' +
        '<span aria-hidden="true">×</span><span class="hidden">Close</span>' +
        '</button>' + message + '</div></div>');
    $('#alerts').slideDown();
}

function getInfo(id, tableid) {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'getInfo',
            node: id,
            table: tableid
        },
        type: 'post'
    }).responseText;

    return info;
}

function compareComponents(ids, tableid) {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'compareComponents',
            nodeids: ids,
            table: tableid
        },
        type: 'post'
    }).responseText;

    return info;
}

function componentsOverview() {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'componentOverview',
            motherboardid: motherboardSelect,
            cpuid: cpuSelect,
            cpufanid: cpufanSelect,
            graphicscardid: graphicscardSelect,
            ramid: ramSelect,
            caseid: caseSelect,
            storageid: storageSelect
        },
        type: 'post'
    }).responseText;

    return info;
}