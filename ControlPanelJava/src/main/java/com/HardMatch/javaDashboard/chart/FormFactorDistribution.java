package com.hardmatch.javaDashboard.chart;

import java.util.List;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.HardMatch.controlpanel.WicketApplication;
import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.series.SimpleSeries;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class FormFactorDistribution extends ColumnChartOptions {

	private static final long serialVersionUID = 198761981680333580L;

	public FormFactorDistribution() {
		super();
		setTitle(new Title(""));

		RestAPI rest = WicketApplication.getRest();
		JSONObject object = rest.sendCypher("MATCH (n:`Motherboard`) RETURN DISTINCT (n.FormFactor), COUNT(n)");
		List<JSONArray> rows = rest.json.getRowsFromQuery(object);
		for(JSONArray row : rows) {
			String name = row.get(0).toString();
			addSeries(new SimpleSeries()
			.setName(name)
			.setData(Double.parseDouble(row.get(1).toString())));
		}
	}

}
