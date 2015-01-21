package com.hardmatch.matcher;

import java.io.File;
import java.io.IOException;
import java.net.URISyntaxException;
import java.nio.charset.Charset;
import java.nio.file.Files;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import com.hardmatch.matcher.thrift.Store;
import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Matcher {
	
	private RestAPI rest;
	
	public Matcher() throws URISyntaxException, NumberFormatException, IOException {
		int port = Integer.parseInt(Files.readAllLines(new File("/usr/local/bin/HardMatch/neo4JPort.txt").toPath(), Charset.defaultCharset()).get(0));
    	rest = new RestAPI("http://149.210.188.74:"+port+"/db/data");
	}

    public Store getCheapestStoreForComponent(String componentToBuy) {
    	String cypher = "MATCH (component:Component {ModelID:'"+componentToBuy+"'})-[relation:SOLD_AT]->(store) RETURN store, relation.Price, relation.productUrl, component.Name, labels(component), relation.inStock ORDER BY relation.Price";
    	JSONObject response = rest.sendCypher(cypher);
    	JSONArray results = (JSONArray) response.get("results");
    	JSONObject rows = (JSONObject) results.get(0);
    	JSONArray moarRows = (JSONArray)rows.get("data");
    	JSONObject firstRow = (JSONObject)moarRows.get(0);
    	JSONArray firstRowData = (JSONArray)firstRow.get("row");
    	JSONObject storeObject = (JSONObject) firstRowData.get(0);
    	
    	double componentPrice = Double.parseDouble(firstRowData.get(1).toString());
    	String storeName = storeObject.get("Name").toString();
    	String componentUrl = firstRowData.get(2).toString();
    	String componentName = firstRowData.get(3).toString();
    	JSONArray labels = (JSONArray) firstRowData.get(4);
    	String category = getLabel(labels);
    	String stock = firstRowData.get(5).toString();
    	
    	Store store = new Store(componentName, storeName, componentPrice, componentUrl, category, stock);
    	return store;
    }
    
    public String getLabel(JSONArray labels) {
    	for(Object string : labels) {
    		if(!string.equals("Component")) {
    			return string.toString();
    		}
    	}
    	return "UNKNOWN";
    }

}
