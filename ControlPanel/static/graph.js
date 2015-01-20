$(document).ready(function () {
   $(chart_id).highcharts({

            chart: chart,
            rangeSelector: rangeSelector,
            dataGrouping: dataGrouping,
            title: title,
            xAxis: xAxis,
            yAxis: yAxis,
            series: series
        });
    });
});

/*
$(document).ready(function() {
    $(chart_id).highcharts({
        chart: chart,
        rangeSelector: rangeSelector,
        title: title,
        xAxis: xAxis,
        yAxis: yAxis,
        series: series
    });
});*/