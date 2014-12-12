var processor = "";
var videokaart = "";
var moederbord = "";

var processorCompare = [];
var videokaartCompare = [];

$(document).ready(function() {
    var processors = $('#processors').DataTable();
    var videokaarten = $('#videokaarten').DataTable();

    $('tbody').on('click', '.btn-warning', function() {
        var tr = $(this).closest('tr');
        var tableid = $(this).closest('table').attr('id');
        var id = tr.find("td:first").text();
        var row;
        if (tableid == "processors") {
            row = processors.row(tr);
        } else if (tableid == "videokaarten") {
            row = videokaarten.row(tr);
        };

        if (row.child.isShown()) {
            row.child.hide();
        } else {
            row.child(getInfo(id)).show();
            tr.next('tr').addClass('more-info');
        }
    });

    $('.overzicht-componenten').on('click', '.delete-component', function(event) {
        var button = ($(this).attr('id'));
        switch (button) {
            case "processorButton":
                processor = "";
                $("#processors").find("tr").removeClass("info");
                $('#processor').slideUp(function() {
                    $("div.overzicht-componenten").html(componentenOverzicht(processor, videokaart));
                });
                break;
            case "videokaartButton":
                videokaart = "";
                $("#videokaarten").find("tr").removeClass("info");
                $('#videokaart').slideUp(function() {
                    $("div.overzicht-componenten").html(componentenOverzicht(processor, videokaart));
                });
                break;
        }
    });
});

$('.vergelijkButton').click(function() {
    var tableid = $(this).closest('table').attr('id');
    if (processorCompare.length >= 2 && tableid == "processors") {
        $('.modal-body').html(compareComponents(processorCompare));
        $('#modal').modal('show');
    } else if (videokaartCompare.length >= 2 && tableid == "videokaarten") {
        $('.modal-body').html(compareComponents(videokaartCompare));
        $('#modal').modal('show');
    } else {
        addAlert("danger", "U moet minimaal twee producten selecteren om te kunnen vergelijken.")
    }
});

$('.table-checkbox').change(function() {
    var tableid = $(this).closest('table').attr('id');
    var nodeid = $(this).closest('tr').find("td:first").text();
    if (this.checked) {
        if (tableid == "processors") {
            processorCompare.push(nodeid);
        } else if (tableid == "videokaarten") {
            videokaartCompare.push(nodeid);
        }
    } else {
        if (tableid == "processors") {
            var i = processorCompare.indexOf(nodeid);
            if (i != -1) {
                processorCompare.splice(i, 1);
            }
        } else if (tableid == "videokaarten") {
            var i = videokaartCompare.indexOf(nodeid);
            if (i != -1) {
                videokaartCompare.splice(i, 1);
            }
        }
    }
});

$('tbody').on('click', '.btn-success', function() {
    var row = $(this).closest('tr');
    var nodeid = row.find("td:first").text();
    var tableid = $(this).closest('table').attr('id');
    row.addClass('info').siblings().removeClass('info');

    if (tableid == "processors") {
        processor = nodeid;
    } else if (tableid == "videokaarten") {
        videokaart = nodeid;
    }
})

$('.nexttab').click(function() {
    var id = $(this).attr('id');
    if (id == "next1") {
        $("div.overzicht-componenten").html(componentenOverzicht(processor, videokaart));
    } else if (id == "next2") {
        if (processor == "" && videokaart == "") {
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

function getInfo(id) {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'getInfo',
            node: id
        },
        type: 'post'
    }).responseText;

    return info;
}

function compareComponents(ids) {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'compareComponents',
            nodeids: ids
        },
        type: 'post'
    }).responseText;

    return info;
}

function componentenOverzicht(processor, videokaart) {
    var info = $.ajax({
        url: 'ajax.php',
        dataType: "text",
        async: false,
        data: {
            action: 'componentOverview',
            videokaartid: videokaart,
            processorid: processor
        },
        type: 'post'
    }).responseText;

    return info;
}