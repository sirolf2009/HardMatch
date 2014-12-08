package com.hardmatch.javaDashboard;

import org.apache.wicket.PageParameters;
import org.apache.wicket.markup.html.WebPage;

public class HomePage extends WebPage {

	private static final long serialVersionUID = 1L;

	public HomePage(final PageParameters parameters) {
		add(new Header("headerPanel"));
		
		
		
		add(new Footer("footerPanel"));
	}
}
