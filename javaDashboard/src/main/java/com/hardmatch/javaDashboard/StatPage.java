package com.hardmatch.javaDashboard;

import org.apache.wicket.PageParameters;
import org.apache.wicket.markup.html.WebPage;

public class StatPage extends WebPage {

	public StatPage(PageParameters parameters) {
		super(parameters);
		add(new Header("headerPanel"));
	}

}
