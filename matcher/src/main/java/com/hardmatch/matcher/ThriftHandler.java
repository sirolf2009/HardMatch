package com.hardmatch.matcher;

import java.net.URISyntaxException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.thrift.TException;

import com.hardmatch.matcher.Matcher.MatchingResult;
import com.hardmatch.matcher.thrift.Component;
import com.hardmatch.matcher.thrift.ComponentPriced;
import com.hardmatch.matcher.thrift.MatcherPHPHandler.Iface;
import com.hardmatch.matcher.thrift.Store;

public class ThriftHandler implements Iface {
	
	private Map<String, Store> stores;

	@Override
	public Map<String, Store> match(List<Component> components) throws TException {
		System.out.println("Matching "+components.size()+" components");
		Map<String, Store> cheapyStores = new HashMap<String, Store>();
		stores = new HashMap<String, Store>();
		Matcher matcher = null;
		try {
			matcher = new Matcher(this);
		} catch (URISyntaxException e1) {
			e1.printStackTrace();
		}

		for(Component component : components) {
			System.out.println("Matching "+component.name);
			MatchingResult result = matcher.getCheapestStoreForComponent(component);
			cheapyStores.put(result.componentPriced.getName(), result.store);
			System.out.println("Matched "+component.name);
		}
		stores = null;
		System.out.println("Matched stores");
		return cheapyStores;
	}
	
	public Store getOrCreateStore(String name) {
		if(!stores.containsKey(name)) {
			System.out.println("Creating new store for "+name);
			stores.put(name, new Store(name, new HashMap<String, ComponentPriced>()));
		}
		return stores.get(name);
	}

}
