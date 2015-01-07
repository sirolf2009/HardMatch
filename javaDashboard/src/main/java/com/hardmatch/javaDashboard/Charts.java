package com.hardmatch.javaDashboard;

import org.apache.wicket.markup.html.basic.Label;

import com.googlecode.wickedcharts.wicket6.highcharts.Chart;
import com.hardmatch.javaDashboard.chart.ComponentDistributionOptions;
import com.hardmatch.javaDashboard.chart.ComponentsPerStoreOptions;
import com.hardmatch.javaDashboard.chart.AverageComponentPriceOptions;
import com.hardmatch.javaDashboard.chart.MostExpensiveComponentsOptions;

public class Charts extends DashboardPage {

	private static final long serialVersionUID = -3370404913253664770L;

	public Charts() {
		add(new Chart("chartComponentDistribution", new ComponentDistributionOptions()));
		add(new Chart("chartComponentsPerStore", new ComponentsPerStoreOptions()));
		add(new Chart("chartAverageComponentPrice", new AverageComponentPriceOptions()));
		add(new Chart("chartMostExpensiveComponents", new MostExpensiveComponentsOptions(10)));
		add(new Label("timeSinceMatcherHeartbeat", getTimeSinceMatcherHeartbeat()));
	}

	public String getTimeSinceMatcherHeartbeat() {
		WicketApplication app = (WicketApplication) getApplication();
		long time = System.currentTimeMillis();
		long delta = time - app.getLastMatcherHeartBeat();
		if(delta != time) {
			delta /= 1000;
			return delta+" seconds";
		} else {
			return "never";
		}
	}

}
