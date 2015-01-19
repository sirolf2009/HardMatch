package com.hardmatch.javaDashboard.chart;

import java.util.Date;

import com.googlecode.wickedcharts.highcharts.options.Title;
import com.googlecode.wickedcharts.highcharts.options.livedata.LiveDataSeries;
import com.googlecode.wickedcharts.highcharts.options.livedata.LiveDataUpdateEvent;
import com.googlecode.wickedcharts.highcharts.options.series.Point;
import com.hardmatch.javaDashboard.WicketApplication;

public class CheckerHeartBeatOptions extends UpdatingLineChartOptions {
	private static final long serialVersionUID = -930358709662655780L;

	private LiveDataSeries series;

	private long lastHeartBeat;
	
	private boolean wasLastTickHigh;

	public CheckerHeartBeatOptions() {
		setTitle(new Title("Checker Heartbeat"));
		series = new LiveDataSeries(this, 5000) {
			private static final long serialVersionUID = -1424631228701752414L;

			@Override
			public Point update(LiveDataUpdateEvent event) {
				long currentHeartBeat = WicketApplication.instance.getLastCheckerHeartBeat();
				if(currentHeartBeat == lastHeartBeat) {
					if(wasLastTickHigh) {
						wasLastTickHigh = false;
						return new Point(new Date().getTime(), -1);
					} else {
						return new Point(new Date().getTime(), 0);
					}
				} else {
					lastHeartBeat = currentHeartBeat;
					wasLastTickHigh = true;
					return new Point(new Date().getTime(), 1);
				}
			}
		};
		series
		.setData(emptyData(20))
		.setName("HeartBeat");
		addSeries(series);
	}

}
