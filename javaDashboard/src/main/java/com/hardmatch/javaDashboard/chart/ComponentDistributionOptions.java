package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.googlecode.wickedcharts.highcharts.options.SeriesType;
import com.googlecode.wickedcharts.highcharts.options.series.PointSeries;
import com.hardmatch.javaDashboard.WicketApplication;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class ComponentDistributionOptions extends PieChartOptions {

	private static final long serialVersionUID = 356722944686025762L;

	public ComponentDistributionOptions() {
		super();		
		PointSeries series = new PointSeries();
		series.setType(SeriesType.PIE).setName("Component Share");
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Component) RETURN DISTINCT LABELS(n), COUNT(n)");
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		for (int i = 0; i < results.size(); i++) {
			JSONArray row = results.get(i);
			String name = row.get(0).toString().replace("Component", "").replace("\"", "").replace("[", "").replace("]", "").replace(",", "").trim();
			series.addPoint(createPoint(name, Double.parseDouble(row.get(1).toString()), i));
		}

		addSeries(series);
	}

}
