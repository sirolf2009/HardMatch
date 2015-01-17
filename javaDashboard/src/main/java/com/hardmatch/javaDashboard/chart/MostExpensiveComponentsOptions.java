package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.series.SimpleSeries;
import com.hardmatch.javaDashboard.WicketApplication;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class MostExpensiveComponentsOptions extends ColumnChartOptions {

	private static final long serialVersionUID = -373464100751610560L;

	public MostExpensiveComponentsOptions(int amount) {
		setTitle(new Title("Top "+amount+" Most Expensive Components"));
		
		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:Component)-[r:SOLD_AT]->(:Store) RETURN DISTINCT n.modelID, MAX(r.Price) ORDER BY MAX(r.price) DESC LIMIT "+amount);
		List<JSONArray> rows = rest.json.getRowsFromQuery(object);
		for(JSONArray row : rows) {
			String name = row.get(0).toString();
			addSeries(new SimpleSeries()
			.setName(name)
			.setData(Double.parseDouble(row.get(1).toString())));
		}
	}

}
