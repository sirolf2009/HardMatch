package com.hardmatch.javaDashboard.packets;

import com.hardmatch.javaDashboard.NetworkManager;
import com.sirolf2009.networking.IHost;
import com.sirolf2009.networking.Packet;

public class PacketHeartbeatChecker extends Packet {

	public PacketHeartbeatChecker() {}
	
	@Override
	public void receivedOnServer(IHost host) {
		NetworkManager server = (NetworkManager) host.getServer();
		server.getApplication().onHeartBeatChecker();
	}

}
