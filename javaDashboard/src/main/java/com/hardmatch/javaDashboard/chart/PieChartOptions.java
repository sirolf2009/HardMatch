package com.hardmatch.javaDashboard.chart;

import com.googlecode.wickedcharts.highcharts.options.ChartOptions;
import com.googlecode.wickedcharts.highcharts.options.Cursor;
import com.googlecode.wickedcharts.highcharts.options.DataLabels;
import com.googlecode.wickedcharts.highcharts.options.Function;
import com.googlecode.wickedcharts.highcharts.options.Options;
import com.googlecode.wickedcharts.highcharts.options.PlotOptions;
import com.googlecode.wickedcharts.highcharts.options.PlotOptionsChoice;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.Tooltip;
import com.googlecode.wickedcharts.highcharts.options.color.HexColor;
import com.googlecode.wickedcharts.highcharts.options.color.HighchartsColor;
import com.googlecode.wickedcharts.highcharts.options.color.NullColor;
import com.googlecode.wickedcharts.highcharts.options.color.RadialGradient;
import com.googlecode.wickedcharts.highcharts.options.functions.PercentageFormatter;
import com.googlecode.wickedcharts.highcharts.options.series.Point;

public class PieChartOptions extends Options {

	private static final long serialVersionUID = 5156236940550124508L;

	public PieChartOptions() {
		setChartOptions(new ChartOptions()
		.setPlotBackgroundColor(new NullColor())
		.setPlotBorderWidth(null)
		.setPlotShadow(Boolean.FALSE));

		setTitle(new Title("NO NAME DEFINED"));

		setTooltip(new Tooltip()
		.setFormatter(new PercentageFormatter())
		.setPercentageDecimals(1));

		setPlotOptions(new PlotOptionsChoice()
		.setPie(new PlotOptions()
		.setAllowPointSelect(Boolean.TRUE)
		.setCursor(Cursor.POINTER)
		.setDataLabels(new DataLabels()
		.setEnabled(Boolean.TRUE)
		.setColor(new HexColor("#000000"))
		.setConnectorColor(new HexColor("#000000"))
		.setFormatter(new Function("return '<b>' + this.point.name + '</b>: ' + this.percentage.toFixed(2) + '%';")))));
	}

	public PieChartOptions(Options template) {
		super(template);
	}
	
	public Point createPoint(String name, double value, int index) {
		return new Point(name, value).setColor(new RadialGradient()
		.setCx(0.5)
		.setCy(0.3)
		.setR(0.7)
		.addStop(0, new HighchartsColor(index))
		.addStop(1, new HighchartsColor(index)
		.brighten(-0.3f)));
	}

}
