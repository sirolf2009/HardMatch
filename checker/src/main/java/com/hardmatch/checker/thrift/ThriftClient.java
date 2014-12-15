package com.hardmatch.checker.thrift;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

public class ThriftClient {

	public static void main(String[] args) {

		try {
			TTransport transport;

			transport = new TSocket("localhost", 9091);
			transport.open();

			TProtocol protocol = new TBinaryProtocol(transport);
			CrawlerCheckerHandler.Client client = new CrawlerCheckerHandler.Client(protocol);
			client.check();
			transport.close();
		} catch (TTransportException e) {
			e.printStackTrace();
		} catch (TException x) {
			x.printStackTrace();
		}
	}

}