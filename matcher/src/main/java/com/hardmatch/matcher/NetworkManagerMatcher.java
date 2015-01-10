package com.hardmatch.matcher;

import java.util.Observable;

import com.hardmatch.matcher.packets.PacketHeartbeatMatcher;
import com.sirolf2009.networking.AbstractClient;

public class NetworkManagerMatcher extends AbstractClient {

	public NetworkManagerMatcher() {
		this("localhost", 1200);
	}
	
	public NetworkManagerMatcher(String host, int port) {
		super(host, port);
	}

	@Override
	public void onConnected() {
		new Thread(new Runnable() {
			public void run() {
				try {
					Thread.sleep(1000*60);
				} catch (InterruptedException e) {
					e.printStackTrace();
				}
				sendPacket(new PacketHeartbeatMatcher());
			}
		}).start();
	}

	@Override
	public void disconnect() {
		
	}

	@Override
	public void update(Observable o, Object arg) {
		
	}

}
