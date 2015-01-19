package com.hardmatch.javaDashboard;

import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.markup.html.link.Link;

public abstract class DashboardPage extends WebPage {

	private static final long serialVersionUID = -465597321270465515L;

	public DashboardPage() {
		add(new Link<Object>("homeLink") {
			private static final long serialVersionUID = -2834332176756729379L;
			@Override
			public void onClick() {
				redirectToInterceptPage(new Dashboard());
			}
		});
		add(new Link<Object>("chartsLink") {
			private static final long serialVersionUID = -2834332176756729379L;
			@Override
			public void onClick() {
				redirectToInterceptPage(new Charts());
			}
		});
	}

}
