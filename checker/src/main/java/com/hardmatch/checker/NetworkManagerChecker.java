package com.hardmatch.checker;

import java.io.IOException;
import java.util.Observable;

import org.apache.commons.logging.impl.SimpleLog;

import com.sirolf2009.networking.AbstractClient;
import com.sirolf2009.networking.Packet;

public class NetworkManagerChecker extends AbstractClient {
	
	private static SimpleLog log = new SimpleLog("Network Manager Checker");

	public NetworkManagerChecker() {
		this("localhost", 1200);
	}

	public NetworkManagerChecker(String host, int port) {
		super(host, port);
	}

	@Override
	public void onConnected() {
		log.info("Connected to the dashboard");
		new Thread(new Runnable() {
			public void run() {
				while(true) {
					sendPacket(new PacketHeartbeatChecker());
					try {
						Thread.sleep(1000*30);
					} catch (InterruptedException e) {
						e.printStackTrace();
					}
				}
			}
		}).start();
	}
	
	@Override
	public void onConnectFailed(Exception e) {
		log.error("Could not connect to the dashboard. Retrying in 60 seconds...", e);
		try {
			Thread.sleep(1000*60);
			connect("localhost", 1200);
		} catch (IOException e1) {
			onConnectFailed(e1);
		} catch (InterruptedException e1) {
		}
	}

	@Override
	public void disconnect() {
	}

	@Override
	public void update(Observable o, Object arg) {
	}
	
	static {
		Packet.registerPacket(2, PacketHeartbeatChecker.class);
	}

}
