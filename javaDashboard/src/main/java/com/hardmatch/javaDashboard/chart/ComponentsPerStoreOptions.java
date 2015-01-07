package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.series.PointSeries;
import com.hardmatch.javaDashboard.WicketApplication;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class ComponentsPerStoreOptions extends PieChartOptions {

	private static final long serialVersionUID = 356722944686025762L;

	public ComponentsPerStoreOptions() {
		PointSeries series = new PointSeries();
		series.setType(SeriesType.PIE).setName("Store Share");
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Store)-[r:SOLD_AT]-(m:Component) RETURN n.name, COUNT(r)");
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		for (int i = 0; i < results.size(); i++) {
			JSONArray row = results.get(i);
			series.addPoint(createPoint(row.get(0).toString(), Double.parseDouble(row.get(1).toString()), i));
		}

		addSeries(series);
	}

}
