package com.hardmatch.matcher;

import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.thrift.TException;

import com.hardmatch.matcher.thrift.MatcherPHPHandler.Iface;
import com.hardmatch.matcher.thrift.Store;

public class ThriftHandler implements Iface {

	@Override
	public Map<String, Store> match(List<String> components) throws TException {
		System.out.println("Matching "+components.size()+" components");
		Map<String, Store> cheapyStores = new HashMap<String, Store>();
		Matcher matcher = null;
		try {
			matcher = new Matcher();
		} catch (URISyntaxException e1) {
			e1.printStackTrace();
		}

		for(String component : components) {
			System.out.println("Matching "+component);
			Store result = matcher.getCheapestStoreForComponent(component);
			cheapyStores.put(component, result);
			System.out.println("Matched "+component);
		}
		System.out.println("Matched stores");
		return cheapyStores;
	}

}
