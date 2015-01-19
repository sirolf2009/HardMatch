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
		setTitle(new Title("CPU distribution"));
		series.setType(SeriesType.PIE).setName("Compatibility Share");
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:CPU) WHERE n.Socket <> 'null' RETURN distinct n.Socket, COUNT(n.Socket) LIMIT 100");
		List<JSONArray> results = rest.json.getRowsFromQuery(object);
		for (int i = 0; i < results.size(); i++) {
			JSONArray row = results.get(i);
			String name = row.get(0).toString();
			series.addPoint(createPoint(name, Double.parseDouble(row.get(1).toString()), i));
		}
		addSeries(series);
	}

}
