package com.hardmatch.checker;

import java.util.Observable;

import com.sirolf2009.networking.AbstractClient;

public class NetworkManagerChecker extends AbstractClient {

	public NetworkManagerChecker() {
		this("localhost", 1200);
	}

	public NetworkManagerChecker(String host, int port) {
		super(host, port);
	}

	@Override
	public void onConnected() {
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
	public void disconnect() {
	}

	@Override
	public void update(Observable o, Object arg) {
	}

}
