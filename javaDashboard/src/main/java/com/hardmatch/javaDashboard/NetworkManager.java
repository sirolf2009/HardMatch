package com.hardmatch.javaDashboard;

import java.io.IOException;
import java.util.Observable;

import com.hardmatch.javaDashboard.packets.PacketHeartbeatMatcher;
import com.sirolf2009.networking.AbstractServer;
import com.sirolf2009.networking.Events.EventPacketReceived;

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
		if(arg instanceof EventPacketReceived) {
			EventPacketReceived event = (EventPacketReceived) arg;
			if(event.getPacket() instanceof PacketHeartbeatMatcher) {
				getApplication().onHeartBeatMatcher();
			}
		}
		log.info(o+": "+arg);
	}

	public WicketApplication getApplication() {
		return application;
	}

	public void setApplication(WicketApplication application) {
		this.application = application;
	}

}
