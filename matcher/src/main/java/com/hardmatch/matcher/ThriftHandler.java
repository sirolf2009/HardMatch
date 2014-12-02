package com.hardmatch.matcher;

import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.thrift.TException;

public class ThriftHandler implements MatcherPHPHandler.Iface {
	
	private Matcher matcher;
	
	public ThriftHandler() {
		try {
			matcher = new Matcher();
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
	}

	@Override
	public Map<String, Store> match(List<Component> components) throws TException {
		System.out.println("let the matching...");
		System.out.println("BBEEEEGGGGGIIIIINNNN \\m/");
		
		Map<String, Store> cheapyStores = new HashMap<String, Store>();
		
		for(Component component : components) {
			cheapyStores.put(component.getName(), matcher.getCheapestStoreForComponent(component));
		}
		
		return cheapyStores;
	}

}
