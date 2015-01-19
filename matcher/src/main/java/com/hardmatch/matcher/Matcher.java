package com.hardmatch.matcher;

import java.net.URISyntaxException;
import java.util.HashMap;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.matcher.thrift.Component;
import com.hardmatch.matcher.thrift.ComponentPriced;
import com.hardmatch.matcher.thrift.Store;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Matcher {
	
	private RestAPI rest;
	private ThriftHandler handler;
	
	public Matcher(ThriftHandler handler) throws URISyntaxException {
    	rest = new RestAPI("http://149.210.188.74:7474/db/data");
    	this.handler = handler;
	}

    public MatchingResult getCheapestStoreForComponent(Component componentToBuy) {
    	String cypher = "MATCH (component:Component {ModelID:'"+componentToBuy.name+"'})-[relation:SOLD_AT]->(store) RETURN store, relation.Price ORDER BY relation.Price";
    	JSONObject response = rest.sendCypher(cypher);
    	JSONArray results = (JSONArray) response.get("results");
    	JSONObject rows = (JSONObject) results.get(0);
    	JSONArray moarRows = (JSONArray)rows.get("data");
    	JSONObject firstRow = (JSONObject)moarRows.get(0);
    	JSONArray firstRowData = (JSONArray)firstRow.get("row");
    	JSONObject firstRowDataRow = (JSONObject) firstRowData.get(0);
    	double componentPrice = Double.parseDouble(firstRowData.get(1).toString());
    	String storeName = firstRowDataRow.get("Name").toString();
    	Store store = handler.getOrCreateStore(storeName);
    	ComponentPriced priced = new ComponentPriced(componentToBuy.name, componentPrice);
    	store.soldItems.put(componentToBuy.name, priced);
    	return new MatchingResult(priced, store);
    }
    
    class MatchingResult {
    	public ComponentPriced componentPriced;
    	public Store store;
    	
    	public MatchingResult(ComponentPriced componentPriced, Store store) {
    		this.componentPriced = componentPriced;
    		this.store = store;
		}
    }

}
