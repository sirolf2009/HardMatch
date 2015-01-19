package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.series.SimpleSeries;
import com.hardmatch.javaDashboard.WicketApplication;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class AverageComponentPriceOptions extends ColumnChartOptions {

	private static final long serialVersionUID = 7086312263334411682L;

	public AverageComponentPriceOptions() {
		setTitle(new Title("Average Component Prices"));
		
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Component)-[r:SOLD_AT]->(:Store) RETURN DISTINCT LABELS(n), AVG(r.price)");
		List<JSONArray> rows = rest.json.getRowsFromQuery(object);
		for(JSONArray row : rows) {
			String name = row.get(0).toString().replace("Component", "").replace("\"", "").replace("[", "").replace("]", "").replace(",", "").trim();
			addSeries(new SimpleSeries()
			.setName(name)
			.setData(Double.parseDouble(row.get(1).toString())));
		}
	}

}
