package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.series.PointSeries;
import com.hardmatch.javaDashboard.WicketApplication;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class CompatibilityDistributionOptions extends PieChartOptions {

	private static final long serialVersionUID = -5500294143646234645L;

	public CompatibilityDistributionOptions() {
		PointSeries series = new PointSeries();
		setTitle(new Title("Compatibility distribution"));
		series.setType(SeriesType.PIE).setName("Compatibility Share");
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (c)-[:COMPATIBLE]-(), (n)-[NOT_COMPATIBLE]-() RETURN COUNT(DISTINCT n) AS not_compatible, COUNT(DISTINCT c) AS compatible");
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		series.addPoint(createPoint("Compatible", Double.parseDouble(results.get(0).get(1).toString()), 0));
		series.addPoint(createPoint("Not compatible", Double.parseDouble(results.get(0).get(0).toString()), 1));
		addSeries(series);
	}

}
