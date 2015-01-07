package com.hardmatch.matcher;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadPoolServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

import com.hardmatch.matcher.packets.PacketHeartbeat;
import com.sirolf2009.networking.Packet;

public class ThriftServer {

	private static ThriftHandler handler;
	private static MatcherPHPHandler.Processor<ThriftHandler> processor;
	private static NetworkManagerMatcher networkManager;

	public static void main(String [] args) {
		try {
			handler = new ThriftHandler();
			processor = new MatcherPHPHandler.Processor<ThriftHandler>(handler);

			Runnable simple = new Runnable() {
				public void run() {
					simple(processor);
				}
			};

			new Thread(simple).start();
			
			networkManager = new NetworkManagerMatcher();
		} catch (Exception x) {
			x.printStackTrace();
		}
	}

	public static void simple(MatcherPHPHandler.Processor<ThriftHandler> processor) {
		try {
			TServerTransport serverTransport = new TServerSocket(9090);
			TServer server = new TThreadPoolServer(new TThreadPoolServer.Args(serverTransport).processor(processor));

			System.out.println("Starting the simple server...");
			server.serve();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	static {
		Packet.registerPacket(1, PacketHeartbeat.class);
	}

}
