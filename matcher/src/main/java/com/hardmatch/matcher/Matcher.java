package com.hardmatch.matcher;

import java.net.URISyntaxException;

import org.json.simple.JSONObject;

import com.sirolf2009.util.neo4j.rest.RestAPI;

public class Matcher {
	
	private RestAPI rest;

	public Matcher() throws URISyntaxException {
		createDB();
	}
	
    public void createDB() throws URISyntaxException {
    	rest = new RestAPI("http://localhost:7474/db/data");
    }
    
    public Store getCheapestStoreForComponent(Component componentToBuy) {
    	String cypher = "MATCH (component:Component {name:\""+componentToBuy.name+"\"})-[relation:SOLD_AT]->(store) RETURN store ORDER BY relation.price";
    	JSONObject rows = rest.sendCypher(cypher);
    	JSONObject firstRow = (JSONObject) rows.get(0);
    	JSONObject store = (JSONObject) firstRow.get(0);
    	System.out.println(store);
    	return new Store(store.toJSONString());
    }
    
    public static void main(String[] args){
        try {
			new Matcher();
		} catch (URISyntaxException e) {
			e.printStackTrace();
		}
    }

}
