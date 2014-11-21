package com.hardmatch.matcher;

import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.apache.thrift.TException;
import org.neo4j.cypher.javacompat.ExecutionEngine;
import org.neo4j.cypher.javacompat.ExecutionResult;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.Relationship;

import com.sirolf2009.util.neo4j.cypher.CypherHelper;

public class ThriftHandler implements MatcherPHPHandler.Iface {
	
	private GraphDatabaseService graph;
	private ExecutionEngine engine;
	
	public ThriftHandler(GraphDatabaseService graph) {
		this.graph = graph;
		this.engine = new ExecutionEngine(graph);
	}

	@Override
	public Map<String, Store> match(List<Component> components) throws TException {
		System.out.println("let the matching...");
		System.out.println("BBEEEEGGGGGIIIIINNNN \\m/");
		
		Map<String, Store> cheapyStores = new HashMap<String, Store>();
		
		for(Component component : components) {
			cheapyStores.put(component.getName(), getCheapestStoreForComponent(component));
		}
		
		return cheapyStores;
	}
    
    public Store getCheapestStoreForComponent(Component componentToBuy) {
    	String cypher = "MATCH (component:Component {name:\""+componentToBuy.name+"\"})-[relation:SOLD_AT]->(store) RETURN component, relation, store ORDER BY relation.price";
    	ExecutionResult result = CypherHelper.Cypher(engine, cypher);
    	Iterator<Map<String, Object>> itr = result.iterator();
    	if(itr.hasNext()) {
    		Map<String, Object> row = itr.next();
    		Node component = (Node) row.get("component");
    		Relationship relation = (Relationship) row.get("relation");
    		Node store = (Node) row.get("store");
    		System.out.println("Cheapest store for "+component.getProperty("name")+" is "+store.getProperty("name")+" for a price of "+relation.getProperty("price"));
    		return new Store(store.getProperty("name").toString());
    	}
    	System.err.println("Could not find a store for component "+componentToBuy.name);
    	return null;
    }

}
