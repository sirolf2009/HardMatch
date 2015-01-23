package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.HardMatch.controlpanel.WicketApplication;
import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.series.PointSeries;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class MotherboardDistributionOptions extends PieChartOptions {

	private static final long serialVersionUID = 7973796499991789038L;

	public MotherboardDistributionOptions() {
		super();
		PointSeries series = new PointSeries();
		setTitle(new Title(""));
		series.setType(SeriesType.PIE).setName("Component Share");
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Motherboard) RETURN DISTINCT n.Merk, COUNT(n)");
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		for (int i = 0; i < results.size(); i++) {
			JSONArray row = results.get(i);
			series.addPoint(createPoint(row.get(0).toString(), Double.parseDouble(row.get(1).toString()), i));
		}

		addSeries(series);
	}

}
