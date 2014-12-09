package com.hardmatch.javaDashboard;

import java.awt.Dimension;

import org.apache.wicket.PageParameters;
import org.wicketstuff.googlecharts.AbstractChartData;
import org.wicketstuff.googlecharts.Chart;
import org.wicketstuff.googlecharts.ChartAxis;
import org.wicketstuff.googlecharts.ChartAxisType;
import org.wicketstuff.googlecharts.ChartProvider;
import org.wicketstuff.googlecharts.ChartType;
import org.wicketstuff.googlecharts.IChartData;

public class HomePage extends PageHardMatch {

	private static final long serialVersionUID = 1L;

	public HomePage(final PageParameters parameters) {
		super(parameters);
		
		IChartData data = new AbstractChartData() {
			private static final long serialVersionUID = 6928598373088425091L;

			public double[][] getData() {
		        return new double[][] {{60, 60, 48, 38, 41, 22, 41, 44, 38, 1}};
		    }
		};
		 
		ChartProvider provider = new ChartProvider(new Dimension(600, 500), ChartType.LINE, data);
		 
		ChartAxis axis = new ChartAxis(ChartAxisType.BOTTOM);
		axis.setLabels(new String[] {"A FRICKING LOT", "Awesome", "yay!", "hmm", "meh"});
		provider.addAxis(axis);
		 
		axis = new ChartAxis(ChartAxisType.LEFT);
		axis.setLabels(new String[] {"no", "yes", "really yes"});
		provider.addAxis(axis);
		
		provider.setTitle("How much I love Wicket");
		 
		add(new Chart("venn", provider));
	}
}
