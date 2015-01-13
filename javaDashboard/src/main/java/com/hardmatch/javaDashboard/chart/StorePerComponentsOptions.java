package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.series.PointSeries;
import com.hardmatch.javaDashboard.WicketApplication;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class StorePerComponentsOptions extends PieChartOptions {

	private static final long serialVersionUID = 356722944686025762L;

	public StorePerComponentsOptions(int amount) {
		PointSeries series = new PointSeries();
		series.setType(SeriesType.PIE).setName("Component Share");
		setTitle(new Title("Components with most stores"));
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Component)-[r:SOLD_AT]-(m:Store) RETURN n.modelID, COUNT(r) ORDER BY count(r) DESC LIMIT "+amount);
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		for (int i = 0; i < results.size(); i++) {
			JSONArray row = results.get(i);
			series.addPoint(createPoint(row.get(0).toString(), Double.parseDouble(row.get(1).toString()), i));
		}

		addSeries(series);
	}

}
