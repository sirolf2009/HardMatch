package com.hardmatch.javaDashboard.chart;

import java.awt.Dimension;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.wicketstuff.googlecharts.AbstractChartData;
import org.wicketstuff.googlecharts.ChartAxis;
import org.wicketstuff.googlecharts.ChartAxisType;
import org.wicketstuff.googlecharts.ChartProvider;
import org.wicketstuff.googlecharts.ChartType;
import org.wicketstuff.googlecharts.IChartData;

import com.sirolf2009.util.neo4j.rest.RestAPI;

public class ChartGenerator {

	public static ChartProvider getTestChartLine() {
		IChartData data = new AbstractChartData() {
			private static final long serialVersionUID = 6928598373088425091L;

			public double[][] getData() {
				return new double[][] {{60, 59, 48, 38, 41, 22, 41, 44, 38, 1}};
			}
		};

		ChartProvider provider = new ChartProvider(new Dimension(600, 500), ChartType.LINE, data);

		ChartAxis axis = new ChartAxis(ChartAxisType.BOTTOM);
		axis.setLabels(new String[] {"A FRICKING LOT", "Awesome", "yay!", "hmm", "meh"});
		provider.addAxis(axis);

		axis = new ChartAxis(ChartAxisType.LEFT);
		axis.setLabels(new String[] {"no", "yes", "really yes"});
		provider.addAxis(axis);

		return provider;
	}

	public static ChartProvider getTestChartPie() {
		IChartData data = new AbstractChartData() {
			private static final long serialVersionUID = 7860488665107287476L;

			public double[][] getData() {
				return new double[][] {{34, 22}};
			}
		};

		ChartProvider provider = new ChartProvider(new Dimension(500, 400), 
				ChartType.PIE_3D, data);
		provider.setPieLabels(new String[] {"Hello", "World"});

		return provider;
	}

	public static ChartProvider getComponentDistributionPie() {

		IChartData data = new AbstractChartData() {
			private static final long serialVersionUID = 7860488665107287476L;

			public double[][] getData() {
				RestAPI rest = null;
				try {
					rest = new RestAPI("http://localhost:7474/db/data");
				} catch (URISyntaxException e) {
					e.printStackTrace();
				}
				double[][] chartData = new double[1][3];
				JSONObject object = rest.sendCypher("MATCH (cpu:CPU) RETURN count(cpu)");
				chartData[0][0] = Double.parseDouble(rest.json.getRowsFromQuery(object).get(0).get(0).toString());
				object = rest.sendCypher("MATCH (mother:Motherboard) RETURN count(mother)");
				chartData[0][1] = Double.parseDouble(rest.json.getRowsFromQuery(object).get(0).get(0).toString());
				object = rest.sendCypher("MATCH (gfx:GraphicsCard) RETURN count(gfx)");
				chartData[0][2] = Double.parseDouble(rest.json.getRowsFromQuery(object).get(0).get(0).toString());
				return chartData;
			}
		};

		ChartProvider provider = new ChartProvider(new Dimension(600, 500), ChartType.PIE_3D, data);
		provider.setLegend(new String[] {"CPU", "Motherboard", "Graphics Card"});
		provider.setTitle("Distribution of components");

		return provider;
	}

	public static ChartProvider getStoresWithMostComponents() {
		
		final List<String> storeNames = new ArrayList<String>();
		final ChartProvider provider = new ChartProvider(new Dimension(600, 500), ChartType.BAR_VERTICAL_SET, null);

		IChartData data = new AbstractChartData() {
			private static final long serialVersionUID = 7860488665107287476L;

			public double[][] getData() {
				
				RestAPI rest = null;
				try {
					rest = new RestAPI("http://localhost:7474/db/data");
				} catch (URISyntaxException e) {
					e.printStackTrace();
				}
				List<JSONArray> storeCounts = rest.json.getRowsFromQuery(rest.sendCypher("MATCH (n:Store)<-[:SOLD_AT]-(m) RETURN n, COUNT(n) ORDER BY COUNT(n)"));
				double[][] chartData = new double[1][storeCounts.size()];
				for(int i = 0; i < storeCounts.size(); i++) {
					JSONArray store = storeCounts.get(i);
					String storeName = ((JSONObject)store.get(0)).get("name").toString();
					long count = (Long) store.get(1);
					storeNames.add(storeName);
					chartData[0][i] = count;
				}
				provider.setLegend(storeNames.toArray(new String[storeNames.size()]));
				return chartData;
			}
		};
		provider.setData(data);
		provider.setTitle("Store with most components");

		return provider;
	}

}
