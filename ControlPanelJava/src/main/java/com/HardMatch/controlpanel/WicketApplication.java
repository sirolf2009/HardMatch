package com.HardMatch.controlpanel;

import java.net.URISyntaxException;

import org.apache.wicket.markup.html.WebPage;
import org.apache.wicket.protocol.http.WebApplication;

import com.sirolf2009.util.neo4j.rest.RestAPI;

public class WicketApplication extends WebApplication {
	
	private static RestAPI rest;
	
	@Override
	public Class<? extends WebPage> getHomePage() {
		return HomePage.class;
	}

	@Override
	public void init() {
		super.init();
	}
	
	public static RestAPI getRest() {
		if(rest == null) {
			try {
				rest = new RestAPI("http://149.210.188.74:7474/db/data");
			} catch (URISyntaxException e) {
				e.printStackTrace();
			}
		}
		return rest;
	}
}
