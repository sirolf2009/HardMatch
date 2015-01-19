package com.hardmatch.matcher;

import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.thrift.TException;

import com.hardmatch.matcher.thrift.Component;
import com.hardmatch.matcher.thrift.MatcherPHPHandler.Iface;
import com.hardmatch.matcher.thrift.Store;

public class ThriftHandler implements Iface {

	@Override
	public Map<String, Store> match(List<Component> components) throws TException {
		System.out.println("Matching");
		Map<String, Store> cheapyStores = new HashMap<String, Store>();
		Matcher matcher = null;
		try {
			matcher = new Matcher();
		} catch (URISyntaxException e1) {
			e1.printStackTrace();
		}

		for(Component component : components) {
			cheapyStores.put(component.getName(), matcher.getCheapestStoreForComponent(component));
		}
		System.out.println("Matched "+cheapyStores);
		return cheapyStores;
	}

}
