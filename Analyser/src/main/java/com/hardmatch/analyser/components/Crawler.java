package com.hardmatch.analyser.components;

import java.util.HashMap;
import java.util.Map;

import com.mongodb.BasicDBList;
import com.mongodb.BasicDBObject;
import com.mongodb.DBObject;

public class Crawler implements IComponent {
	
	private long amount;
	
	private long errorCount;
	private Map<String, Map<Long, Product>> productPriceHistory;
	
	public Crawler() {
		productPriceHistory = new HashMap<String, Map<Long,Product>>();
	}
	
	public void handleMetaDataObject(DBObject object) {
		System.out.println(object);
		double price = Double.parseDouble(object.get("price").toString());
		String productName = object.get("product").toString();
		long time = Long.parseLong(object.get("timeEnded").toString());
		System.out.println(price+" "+productName+" "+time);
		Product product = new Product();
		product.name = productName;
		product.price = price;
		product.time = time;
		
		if(!productPriceHistory.containsKey(productName)) {
			productPriceHistory.put(productName, new HashMap<Long, Crawler.Product>());
		}
		productPriceHistory.get(productName).put(time, product);
		
		errorCount += Long.parseLong(object.get("errorCount").toString());
		amount++;
	}
	
	public void finalize(DBObject root) {
		BasicDBObject doc = new BasicDBObject();
		doc.append("ErrorRatio", 1/(amount)*errorCount);
		root.put("CrawlerMetadata", doc);
		
		BasicDBObject neo4j = new BasicDBObject();
		root.put("Neo4jMetadata", neo4j);
		BasicDBList priceHistory = new BasicDBList();
		for(String key : productPriceHistory.keySet()) {
			DBObject product = new BasicDBObject();
			product.put("name", key);
			DBObject history = new BasicDBObject();
			for(long keyJ : productPriceHistory.get(key).keySet()) {
				history.put("time", productPriceHistory.get(key).get(keyJ).time);
				history.put("price", productPriceHistory.get(key).get(keyJ).price);
			}
			product.put("PriceHistory", history);
			priceHistory.add(product);
		}
		neo4j.put("PriceHistoryPerComponent", priceHistory);
	}
	
	public class Product {
		public double price;
		public String name;
		public long time;
	}

}
