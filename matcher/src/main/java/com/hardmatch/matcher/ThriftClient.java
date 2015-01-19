package com.hardmatch.matcher;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.thrift.TException;
import org.apache.thrift.protocol.TBinaryProtocol;
import org.apache.thrift.protocol.TProtocol;
import org.apache.thrift.transport.TSocket;
import org.apache.thrift.transport.TTransport;
import org.apache.thrift.transport.TTransportException;

import com.hardmatch.matcher.thrift.Component;
import com.hardmatch.matcher.thrift.MatcherPHPHandler;

public class ThriftClient {

	public static void main(String[] args) {

		try {
			TTransport transport;

			transport = new TSocket("localhost", 9090);
			transport.open();

			TProtocol protocol = new TBinaryProtocol(transport);
			MatcherPHPHandler.Client client = new MatcherPHPHandler.Client(protocol);
			
			List<Component> components = new ArrayList<Component>();
			components.add(new Component("X99 KILLER", new HashMap<String, String>()));
			components.add(new Component("90-MIBGW0-G0EAY00Z", new HashMap<String, String>()));

			System.out.println(client.match(components));

			transport.close();
		} catch (TTransportException e) {
			e.printStackTrace();
		} catch (TException x) {
			x.printStackTrace();
		}
	}

}