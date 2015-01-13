package com.hardmatch.javaDashboard.chart;

import com.googlecode.wickedcharts.highcharts.options.Axis;
import com.googlecode.wickedcharts.highcharts.options.ChartOptions;
import com.googlecode.wickedcharts.highcharts.options.Function;
import com.googlecode.wickedcharts.highcharts.options.HorizontalAlignment;
import com.googlecode.wickedcharts.highcharts.options.Legend;
import com.googlecode.wickedcharts.highcharts.options.LegendLayout;
import com.googlecode.wickedcharts.highcharts.options.Options;
import com.googlecode.wickedcharts.highcharts.options.PlotOptions;
import com.googlecode.wickedcharts.highcharts.options.PlotOptionsChoice;
import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.Tooltip;
import com.googlecode.wickedcharts.highcharts.options.VerticalAlignment;
import com.googlecode.wickedcharts.highcharts.options.color.HexColor;

public class ColumnChartOptions extends Options {

	private static final long serialVersionUID = 3864104238565956680L;

	public ColumnChartOptions() {
		setChartOptions(new ChartOptions().setType(SeriesType.COLUMN));
		
		setxAxis(new Axis().setCategories(""));
		setyAxis(new Axis().setMin(0).setTitle(new Title("Price")));

		setLegend(new Legend()
		.setLayout(LegendLayout.VERTICAL)
		.setBackgroundColor(new HexColor("#FFFFFF"))
		.setAlign(HorizontalAlignment.RIGHT)
		.setVerticalAlign(VerticalAlignment.TOP)
		.setY(70)
		.setFloating(Boolean.TRUE)
		.setShadow(Boolean.TRUE));

		setTooltip(new Tooltip()
		.setFormatter(new Function()
		.setFunction(" return '€' + this.y;")));

		setPlotOptions(new PlotOptionsChoice()
		.setColumn(new PlotOptions()
		.setPointPadding(0.2f)
		.setBorderWidth(0)));
	}

}
