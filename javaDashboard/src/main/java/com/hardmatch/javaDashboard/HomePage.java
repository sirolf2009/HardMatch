package com.hardmatch.javaDashboard;

import org.apache.wicket.PageParameters;
import org.wicketstuff.googlecharts.Chart;
import com.hardmatch.javaDashboard.chart.ChartGenerator;

public class HomePage extends PageHardMatch {

	private static final long serialVersionUID = 1L;

	public HomePage(final PageParameters parameters) {
		super(parameters);
		add(new Menu("menu"));
		 
		add(new Chart("venn", ChartGenerator.getStoresWithMostComponents()));
	}
}
