package com.hardmatch.matcher;

import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.thrift.TException;

public class ThriftHandler implements MatcherPHPHandler.Iface {

	@Override
	public Map<String, Store> match(List<Component> components) throws TException {
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

		return cheapyStores;
	}

}
