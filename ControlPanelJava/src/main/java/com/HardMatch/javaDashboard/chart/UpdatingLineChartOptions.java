package com.hardmatch.javaDashboard.chart;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Date;
import java.util.List;

import com.googlecode.wickedcharts.highcharts.options.Axis;
import com.googlecode.wickedcharts.highcharts.options.AxisType;
import com.googlecode.wickedcharts.highcharts.options.ChartOptions;
import com.googlecode.wickedcharts.highcharts.options.ExportingOptions;
import com.googlecode.wickedcharts.highcharts.options.Function;
import com.googlecode.wickedcharts.highcharts.options.Legend;
import com.googlecode.wickedcharts.highcharts.options.Options;
import com.googlecode.wickedcharts.highcharts.options.PlotLine;
import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.Tooltip;
import com.googlecode.wickedcharts.highcharts.options.color.HexColor;
import com.googlecode.wickedcharts.highcharts.options.series.Point;

public class UpdatingLineChartOptions extends Options {

	private static final long serialVersionUID = -4311861410504006415L;

	public UpdatingLineChartOptions() {
		setChartOptions(new ChartOptions()
		.setType(SeriesType.LINE).setMarginRight(10));

		setxAxis(new Axis()
		.setType(AxisType.DATETIME)
		.setTickPixelInterval(150));

		setyAxis(new Axis()
		.setTitle(new Title("Value"))
		.setPlotLines(Collections.singletonList(new PlotLine()
		.setValue(0f)
		.setWidth(1)
		.setColor(new HexColor("#808080")))));

		setTooltip(new Tooltip()
		.setFormatter(new Function()
		.setFunction("return '<b>'+ this.series.name +'</b><br/>'+"
				+ "Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +'<br/>'+"
				+ "Highcharts.numberFormat(this.y, 2);")));

		setLegend(new Legend(Boolean.FALSE));

		setExporting(new ExportingOptions()
		.setEnabled(Boolean.FALSE));
	}

	public List<Point> emptyData(int size) {
		long time = new Date()
		.getTime() - 5000*size;
		List<Point> result = new ArrayList<Point>();
		for (int i = 0; i < size; i++) {
			result.add(new Point()
			.setX(time)
			.setY(0));
			time += 5000;
		}
		return result;
	}

}
