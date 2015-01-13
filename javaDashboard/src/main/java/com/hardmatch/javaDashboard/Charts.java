package com.hardmatch.javaDashboard;

import org.apache.wicket.ajax.AjaxRequestTarget;
import org.apache.wicket.ajax.AjaxSelfUpdatingTimerBehavior;
import org.apache.wicket.markup.html.basic.Label;
import org.apache.wicket.util.time.Duration;

import com.googlecode.wickedcharts.wicket6.highcharts.Chart;
import com.hardmatch.javaDashboard.chart.AverageComponentPriceOptions;
import com.hardmatch.javaDashboard.chart.CheckerHeartBeatOptions;
import com.hardmatch.javaDashboard.chart.CompatibilityDistributionOptions;
import com.hardmatch.javaDashboard.chart.ComponentDistributionOptions;
import com.hardmatch.javaDashboard.chart.ComponentsPerStoreOptions;
import com.hardmatch.javaDashboard.chart.MatcherHeartBeatOptions;
import com.hardmatch.javaDashboard.chart.MostExpensiveComponentsOptions;
import com.hardmatch.javaDashboard.chart.StorePerComponentsOptions;

public class Charts extends DashboardPage {

	private static final long serialVersionUID = -3370404913253664770L;

	private Label timeSinceCheckerHeartbeat;
	private Label timeSinceMatcherHeartbeat;

	public Charts() {
		setVersioned(false);
		
		add(new Chart("chartComponentDistribution", new ComponentDistributionOptions()));
		add(new Chart("chartComponentsPerStore", new ComponentsPerStoreOptions()));
		add(new Chart("chartStorePerComponents", new StorePerComponentsOptions(5)));
		add(new Chart("chartAverageComponentPrice", new AverageComponentPriceOptions()));
		add(new Chart("chartMostExpensiveComponents", new MostExpensiveComponentsOptions(10)));
		add(new Chart("chartMatcherHeartbeat", new MatcherHeartBeatOptions()));
		add(new Chart("chartCheckerHeartbeat", new CheckerHeartBeatOptions()));
		add(timeSinceMatcherHeartbeat = getTimeSinceMatcherHearbeat());
		add(timeSinceCheckerHeartbeat = getTimeSinceCheckerHearbeat());
		add(new Chart("chartCompatibilityDistribution", new CompatibilityDistributionOptions()));
	}
	
	public Label getTimeSinceCheckerHearbeat() {
		Label label = (Label) new Label("timeSinceCheckerHeartbeat", getTimeSinceCheckerHeartbeat()).setOutputMarkupId(true);
		label.add(new AjaxSelfUpdatingTimerBehavior(Duration.ONE_SECOND) {
			private static final long serialVersionUID = -3720966170218934081L;
			protected void onPostProcessTarget(final AjaxRequestTarget target) {
				timeSinceCheckerHeartbeat.setDefaultModelObject(getTimeSinceCheckerHeartbeat());
			}
		});
		return label;
	}
	
	public Label getTimeSinceMatcherHearbeat() {
		Label label = (Label) new Label("timeSinceMatcherHeartbeat", getTimeSinceMatcherHeartbeat()).setOutputMarkupId(true);
		label.add(new AjaxSelfUpdatingTimerBehavior(Duration.ONE_SECOND) {
			private static final long serialVersionUID = -3720966170218934081L;
			protected void onPostProcessTarget(final AjaxRequestTarget target) {
				timeSinceMatcherHeartbeat.setDefaultModelObject(getTimeSinceMatcherHeartbeat());
			}
		});
		return label;
	}

	public String getTimeSinceMatcherHeartbeat() {
		WicketApplication app = (WicketApplication) getApplication();
		return getTimeSinceHeartbeat(app.getLastMatcherHeartBeat());
	}

	public String getTimeSinceCheckerHeartbeat() {
		WicketApplication app = (WicketApplication) getApplication();
		return getTimeSinceHeartbeat(app.getLastCheckerHeartBeat());
	}
	
	public String getTimeSinceHeartbeat(long lastBeat) {
		long time = System.currentTimeMillis();
		long delta = time - lastBeat;
		if(delta != time) {
			delta /= 1000;
			return delta+" seconds";
		} else {
			return "never";
		}
	}

}
