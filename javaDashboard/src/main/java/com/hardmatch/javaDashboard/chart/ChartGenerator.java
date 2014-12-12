package com.hardmatch.javaDashboard.chart;

import java.awt.Dimension;
import java.net.URISyntaxException;

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
				JSONObject object = rest.sendCypher("MATCH (cpu:CPU), (motherboard:Motherboard), (gfx:GraphicsCard) RETURN count(cpu), count(motherboard), count(gfx)");
				JSONArray results = (JSONArray) object.get("results");
				JSONObject firstData = (JSONObject) results.get(0);
				JSONArray data = (JSONArray) firstData.get("data");
				JSONObject firstRow = (JSONObject) data.get(0);
				JSONArray row = (JSONArray) firstRow.get("row");
				double[][] chartData = new double[1][row.size()];
				for(int i = 0; i < row.size(); i++) {
					chartData[0][i] = Double.parseDouble(row.get(i).toString());
				}
				System.out.println(chartData);
		        return chartData;
		    }
		};
		 
		ChartProvider provider = new ChartProvider(new Dimension(600, 500), ChartType.PIE_3D, data);
		provider.setLegend(new String[] {"CPU", "Motherboard", "Graphics Card"});
		provider.setTitle("Distribution of components");
		
		return provider;
	}

}
