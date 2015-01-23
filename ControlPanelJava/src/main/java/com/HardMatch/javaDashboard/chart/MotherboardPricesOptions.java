package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.HardMatch.controlpanel.WicketApplication;
import com.googlecode.wickedcharts.highcharts.options.Cursor;
import com.googlecode.wickedcharts.highcharts.options.DataLabels;
import com.googlecode.wickedcharts.highcharts.options.Function;
import com.googlecode.wickedcharts.highcharts.options.PlotOptions;
import com.googlecode.wickedcharts.highcharts.options.PlotOptionsChoice;
import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.color.HexColor;
import com.googlecode.wickedcharts.highcharts.options.series.PointSeries;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class MotherboardPricesOptions extends PieChartOptions {

	private static final long serialVersionUID = 7973796499991789038L;

	public MotherboardPricesOptions() {
		super();
		PointSeries series = new PointSeries();
		setTitle(new Title(""));
		series.setType(SeriesType.PIE).setName("Component Share");
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Motherboard)-[r:SOLD_AT]-(:Store) RETURN DISTINCT n.Merk, AVG(r.Price)");
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		for (int i = 0; i < results.size(); i++) {
			JSONArray row = results.get(i);
			series.addPoint(createPoint(row.get(0).toString(), Double.parseDouble(row.get(1).toString()), i));
		}

		addSeries(series);
		
		setPlotOptions(new PlotOptionsChoice()
		.setPie(new PlotOptions()
		.setAllowPointSelect(Boolean.TRUE)
		.setCursor(Cursor.POINTER)
		.setDataLabels(new DataLabels()
		.setEnabled(Boolean.TRUE)
		.setColor(new HexColor("#000000"))
		.setConnectorColor(new HexColor("#000000"))
		.setFormatter(new Function("return '<b>' + this.point.name + '</b>: ' + this.y.toFixed(2);")))));
	}

}
