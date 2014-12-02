package com.hardmatch.matcher;

import org.apache.thrift.server.TServer;
import org.apache.thrift.server.TThreadPoolServer;
import org.apache.thrift.transport.TServerSocket;
import org.apache.thrift.transport.TServerTransport;

public class ThriftServer {

	private static ThriftHandler handler;
	private static MatcherPHPHandler.Processor<ThriftHandler> processor;

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

}
