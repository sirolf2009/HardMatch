package com.hardmatch.javaDashboard;

import org.apache.wicket.PageParameters;
import org.apache.wicket.behavior.HeaderContributor;
import org.apache.wicket.markup.html.WebPage;

public class PageHardMatch extends WebPage {

	public PageHardMatch(final PageParameters parameters) {
		add(HeaderContributor.forCss(getClass(), "hardmatch.css"));
		
		add(new Header("headerPanel"));
		add(new Footer("footerPanel"));
	}

}
