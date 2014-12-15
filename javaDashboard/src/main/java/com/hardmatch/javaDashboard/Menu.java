package com.hardmatch.javaDashboard;

import org.apache.wicket.markup.html.form.Button;
import org.apache.wicket.markup.html.form.Form;
import org.apache.wicket.markup.html.panel.Panel;
import org.wicketstuff.googlecharts.Chart;
import org.wicketstuff.googlecharts.ChartProvider;

import com.hardmatch.javaDashboard.chart.ChartGenerator;

public class Menu extends Panel {

	private static final long serialVersionUID = 1L;

	public Menu(String id) {
		super(id);

		Form form = new Form("form"){
			private static final long serialVersionUID = 5581649189293082609L;
			protected void onSubmit() {
			}
		};
		add(form);

		Button button = new Button("button1") {
			private static final long serialVersionUID = -1868174593205054995L;
			@Override
			public void onSubmit() {
				getPage().replace(new Chart("venn", ChartGenerator.getStoresWithMostComponents()));
			}
		};
		form.add(button);
		Button button2 = new Button("button2") {
			private static final long serialVersionUID = 942599678549826681L;
			@Override
			public void onSubmit() {				
				ChartProvider provider = ChartGenerator.getComponentDistributionPie();
				getPage().replace(new Chart("venn", provider));
			}
		};
		form.add(button2);
	}

}
