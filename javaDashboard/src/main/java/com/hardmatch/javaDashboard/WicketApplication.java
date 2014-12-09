package com.hardmatch.javaDashboard;

import org.apache.wicket.protocol.http.WebApplication;

public class WicketApplication extends WebApplication {
	
	public Class<?> getHomePage() {
		return HomePage.class;
	}

}
