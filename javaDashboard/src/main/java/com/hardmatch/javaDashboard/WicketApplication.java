package com.hardmatch.javaDashboard;

import java.io.IOException;
import java.net.URISyntaxException;

import org.apache.commons.logging.impl.SimpleLog;
import org.apache.wicket.Page;
import org.apache.wicket.protocol.http.WebApplication;

import com.hardmatch.javaDashboard.packets.PacketHeartbeatChecker;
import com.hardmatch.javaDashboard.packets.PacketHeartbeatMatcher;
import com.sirolf2009.networking.Packet;
import com.sirolf2009.util.neo4j.NeoUtil;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class WicketApplication extends WebApplication {
	
	private static RestAPI rest;
	private NetworkManager server;

	private long lastMatcherHeartBeat;
	private long lastCheckerHeartBeat;
	
	public static WicketApplication instance;
	
	public WicketApplication() {
		instance = this;
		try {
			setServer(new NetworkManager(this));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void onHeartBeatMatcher() {
		setLastMatcherHeartBeat(System.currentTimeMillis());
	}
	
	public void onHeartBeatChecker() {
		setLastCheckerHeartBeat(System.currentTimeMillis());
	}
	
	public Class<? extends Page> getHomePage() {
		return Dashboard.class;
	}
	
	public static RestAPI getRest() {
		if(rest == null) {
			try {
				rest = new RestAPI("http://149.210.188.74:7474/db/data");
				NeoUtil.log.setLevel(SimpleLog.LOG_LEVEL_ERROR);
			} catch (URISyntaxException e) {
				e.printStackTrace();
			}
		}
		return rest;
	}
	
	public long getLastMatcherHeartBeat() {
		return lastMatcherHeartBeat;
	}

	public void setLastMatcherHeartBeat(long lastMatcherHeartBeat) {
		this.lastMatcherHeartBeat = lastMatcherHeartBeat;
	}

	public NetworkManager getServer() {
		return server;
	}

	public void setServer(NetworkManager server) {
		this.server = server;
	}

	public long getLastCheckerHeartBeat() {
		return lastCheckerHeartBeat;
	}

	public void setLastCheckerHeartBeat(long lastCheckerHeartBeat) {
		this.lastCheckerHeartBeat = lastCheckerHeartBeat;
	}

	static {
		Packet.registerPacket(1, PacketHeartbeatMatcher.class);
		Packet.registerPacket(2, PacketHeartbeatChecker.class);
	}

}
