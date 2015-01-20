package com.hardmatch.matcher;

import java.net.URISyntaxException;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.matcher.thrift.Store;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Matcher {
	
	private RestAPI rest;
	
	public Matcher() throws URISyntaxException {
    	rest = new RestAPI("http://149.210.188.74:7474/db/data");
	}

    public Store getCheapestStoreForComponent(String componentToBuy) {
    	String cypher = "MATCH (component:Component {ModelID:'"+componentToBuy+"'})-[relation:SOLD_AT]->(store) RETURN store, relation.Price ORDER BY relation.Price";
    	JSONObject response = rest.sendCypher(cypher);
    	JSONArray results = (JSONArray) response.get("results");
    	JSONObject rows = (JSONObject) results.get(0);
    	JSONArray moarRows = (JSONArray)rows.get("data");
    	JSONObject firstRow = (JSONObject)moarRows.get(0);
    	JSONArray firstRowData = (JSONArray)firstRow.get("row");
    	JSONObject firstRowDataRow = (JSONObject) firstRowData.get(0);
    	double componentPrice = Double.parseDouble(firstRowData.get(1).toString());
    	String storeName = firstRowDataRow.get("Name").toString();
    	
    	Store store = new Store(storeName, componentPrice);
    	return store;
    }

}
