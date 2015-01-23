package com.HardMatch.controlpanel;

import org.apache.wicket.request.mapper.parameter.PageParameters;
import org.apache.wicket.markup.html.WebPage;

import com.googlecode.wickedcharts.wicket6.highcharts.Chart;
import com.hardmatch.javaDashboard.chart.CPUWithMostCoresOptions;
import com.hardmatch.javaDashboard.chart.FormFactorDistribution;
import com.hardmatch.javaDashboard.chart.MotherboardDistributionOptions;
import com.hardmatch.javaDashboard.chart.MotherboardPricesOptions;

public class HomePage extends WebPage {
	
	private static final long serialVersionUID = 1L;

	public HomePage(final PageParameters parameters) {
		super(parameters);
		add(new Chart("MotherboardDistributionOptions", new MotherboardDistributionOptions()));
		add(new Chart("MotherboardPricesOptions", new MotherboardPricesOptions()));
		add(new Chart("CPUWithMostCoresOptions", new CPUWithMostCoresOptions()));
		add(new Chart("FormFactorDistributionOptions", new FormFactorDistribution()));
    }
}
