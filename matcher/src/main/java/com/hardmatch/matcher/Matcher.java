package com.hardmatch.matcher;

import java.net.URISyntaxException;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.matcher.thrift.Component;
import com.hardmatch.matcher.thrift.Store;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Matcher {
	
	private RestAPI rest;
	
	public Matcher() throws URISyntaxException {
    	rest = new RestAPI("http://149.210.188.74:7474/db/data");
	}

    public Store getCheapestStoreForComponent(Component componentToBuy) {
    	String cypher = "MATCH (component:Component {ModelID:'"+componentToBuy.name+"'})-[relation:SOLD_AT]->(store) RETURN store ORDER BY relation.price";
    	JSONObject response = rest.sendCypher(cypher);
    	JSONArray results = (JSONArray) response.get("results");
    	JSONObject rows = (JSONObject) results.get(0);
    	JSONArray moarRows = (JSONArray)rows.get("data");
    	JSONObject firstRow = (JSONObject)moarRows.get(0);
    	JSONArray firstRowData = (JSONArray)firstRow.get("row");
    	JSONObject firstRowDataRow = (JSONObject) firstRowData.get(0);
    	String store = firstRowDataRow.get("Name").toString();
    	return new Store(store);
    }
    
    public static void main(String[] args) {
		Component component = new Component("xyz1", null);
		try {
			new Matcher().getCheapestStoreForComponent(component);
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
	}

}
