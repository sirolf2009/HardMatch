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
    $('#alerts').hide();
    $('#alerts').on('click', '.close', function(event) {
        $('#alerts').slideUp();
    });

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
        var row = eval(tableid).row(tr);
        var id = tr.find("td:first").text();
        if (row.child.isShown()) {
            row.child.hide();
        } else {
            row.child(getInfo(id, tableid)).show();
            tr.next('tr').addClass('more-info');
        }
    });
});

$('.overzicht-componenten').on('click', '.delete-component', function(event) {
    var button = ($(this).attr('id'));
    var id = button.substring(0, button.length - 6);

    window[id+"Select"] = "";
    $("#"+id).find("tr").removeClass("info");
    $("#"+id+"-item").slideUp(function(){
        $("div.overzicht-componenten").html(componentsOverview());
        $("div.compatability").html(checkCompatability());
    });
});

$('.vergelijkButton').click(function() {
    var tableid = $(this).closest('table').attr('id');
    var selectedCompare = eval(tableid+"Compare");
    var minItemsSelected = 2;
    var maxItemsSelected = 6;

    if (selectedCompare.length >= minItemsSelected && selectedCompare.length <= maxItemsSelected) {
        $('.modal-body').html(compareComponents(selectedCompare, tableid));
        $('#modal').modal('show');
    } else if (selectedCompare.length <= minItemsSelected){
        addAlert("danger", "U moet minimaal twee producten selecteren om te kunnen vergelijken.")
    } else if (selectedCompare.length >= maxItemsSelected){
        addAlert("danger", "U kunt maximaal 6 producten vergelijken.")
    } else{
        addAlert("danger", "Error.")
    }
});

$('.table-checkbox').change(function() {
    var tableid = $(this).closest('table').attr('id');
    var nodeid = $(this).closest('tr').find("td:first").text();
    var selectedCompare = eval(tableid+"Compare");

    if (this.checked) {
        selectedCompare.push(nodeid);
    } else {
        var i = selectedCompare.indexOf(nodeid);
        selectedCompare.splice(i, 1);
    }
});

$('tbody').on('click', '.btn-success', function() {
    var row = $(this).closest('tr');
    var nodeid = row.find("td:first").text();
    var tableid = $(this).closest('table').attr('id');
    row.addClass('info').siblings().removeClass('info');
    selectedComponent = nodeid;

    eval(tableid+"Select" + " = " + nodeid);
})

$('.nexttab').click(function() {
    var id = $(this).attr('id');
    if (id == "next1") {
        $("div.overzicht-componenten").html(componentsOverview());
        $("div.compatability").html(checkCompatability());
    } else if (id == "next2") {
        var thriftItems = [];
        var selectedItems = [motherboardSelect, cpuSelect, cpufanSelect, graphicscardSelect, ramSelect, caseSelect, storageSelect];
        var count = 0;
        for (index = 0; index < selectedItems.length; index++) {            
            if (selectedItems[index] != ""){                
                thriftItems.push(selectedItems[index]);
                count++;
            }
        }
        if (count == 0){
            addAlert('danger', 'U moet minimaal één component kiezen om verder te gaan.');
            return;
        }
        else{
            $('.thrift').html(getThriftInfo(thriftItems));
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

function getThriftInfo(thriftItems) {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'thriftInfo',
            ids: thriftItems
        },
        type: 'post'
    }).responseText;

    return info;
}

function checkCompatability() {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'checkCompatability',
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