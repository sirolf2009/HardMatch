package com.hardmatch.checker.thrift;

import org.apache.thrift.TException;

import com.hardmatch.checker.Checker;

public class ThriftHandler implements CrawlerCheckerHandler.Iface {

	@Override
	public void check() throws TException {
		System.out.println("Checking...");
		new Checker();
		System.out.println("Done!");
	}

}
