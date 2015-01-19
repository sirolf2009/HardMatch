package com.hardmatch.javaDashboard;

import com.googlecode.wickedcharts.wicket6.highcharts.Chart;
import com.hardmatch.javaDashboard.chart.ComponentsPerStoreOptions;

public class Dashboard extends DashboardPage {

	private static final long serialVersionUID = -2823287985394545558L;

	public Dashboard() {
		add(new Chart("chart", new ComponentsPerStoreOptions()));
	}

}
