package com.hardmatch.matcher;

import java.util.ArrayList;
import java.util.List;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

import com.hardmatch.matcher.thrift.MatcherPHPHandler;

public class ThriftClient {

	public static void main(String[] args) {

		try {
			TTransport transport;

			transport = new TSocket("localhost", 9090);
			transport.open();

			TProtocol protocol = new TBinaryProtocol(transport);
			MatcherPHPHandler.Client client = new MatcherPHPHandler.Client(protocol);
			
			List<String> components = new ArrayList<String>();
			components.add("X99 KILLER");
			components.add("90-MIBGW0-G0EAY00Z");

			System.out.println(client.match(components));

			transport.close();
		} catch (TTransportException e) {
			e.printStackTrace();
		} catch (TException x) {
			x.printStackTrace();
		}
	}

}