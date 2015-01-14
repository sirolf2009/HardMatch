package com.hardmatch.checker.thrift;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadPoolServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

import com.hardmatch.checker.NetworkManagerChecker;
import com.hardmatch.checker.PacketHeartbeatChecker;
import com.sirolf2009.networking.Packet;

public class ThriftServer {

	private static ThriftHandler handler;
	private static CrawlerCheckerHandler.Processor<ThriftHandler> processor;

	public static void main(String [] args) {
		try {
			handler = new ThriftHandler();
			processor = new CrawlerCheckerHandler.Processor<ThriftHandler>(handler);

			Runnable simple = new Runnable() {
				public void run() {
					simple(processor);
				}
			};

			new Thread(simple).start();
		} catch (Exception x) {
			x.printStackTrace();
		}
	}

	public static void simple(CrawlerCheckerHandler.Processor<ThriftHandler> processor) {
		try {
			TServerTransport serverTransport = new TServerSocket(9091);
			TServer server = new TThreadPoolServer(new TThreadPoolServer.Args(serverTransport).processor(processor));
			System.out.println("Server started. Waiting for connections");
			server.serve();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
	
	static {
		Packet.registerPacket(2, PacketHeartbeatChecker.class);
	}


}
