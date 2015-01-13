package com.hardmatch.javaDashboard;

import java.io.IOException;
import java.util.Observable;

import com.sirolf2009.networking.AbstractServer;

public class NetworkManager extends AbstractServer {
	
	private WicketApplication application;

	public NetworkManager(WicketApplication application) throws IOException {
		this(application, 1200);
	}
	
	public NetworkManager(WicketApplication application, int port) throws IOException {
		super(port);
		setApplication(application);
	}

	public void update(Observable o, Object arg) {
		super.update(o, arg);
		log.info(o+": "+arg);
	}

	public WicketApplication getApplication() {
		return application;
	}

	public void setApplication(WicketApplication application) {
		this.application = application;
	}

}
