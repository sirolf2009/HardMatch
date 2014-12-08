package com.hardmatch.javaDashboard;

import org.apache.wicket.ResourceReference;
import org.apache.wicket.markup.html.image.Image;
import org.apache.wicket.markup.html.link.PageLink;
import org.apache.wicket.markup.html.panel.Panel;

public class Header extends Panel {

	private static final long serialVersionUID = 1L;

	public Header(String id) {
		super(id);
		PageLink linkHome = new PageLink("HomeLink", HomePage.class);
		linkHome.add(new Image("Img", new ResourceReference(getClass(), "home.png")));
		add(linkHome);
		PageLink linkStats = new PageLink("StatsLink", StatPage.class);
		linkStats.add(new Image("Img", new ResourceReference(getClass(), "button.png")));
		add(linkStats);
	}

}
