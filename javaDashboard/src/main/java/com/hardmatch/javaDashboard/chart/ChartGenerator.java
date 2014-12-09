package com.hardmatch.javaDashboard.chart;

import java.awt.Dimension;

import org.wicketstuff.googlecharts.AbstractChartData;
import org.wicketstuff.googlecharts.ChartAxis;
import org.wicketstuff.googlecharts.ChartAxisType;
import org.wicketstuff.googlecharts.ChartProvider;
import org.wicketstuff.googlecharts.ChartType;
import org.wicketstuff.googlecharts.IChartData;

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

}
