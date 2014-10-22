package com.hardmatch.matcher;

import java.util.Iterator;
import java.util.Map;

import org.neo4j.cypher.javacompat.ExecutionEngine;
import org.neo4j.cypher.javacompat.ExecutionResult;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;

import com.hardmatch.matcher.component.Component;
import com.hardmatch.matcher.component.ComponentMotherboard;
import com.sirolf2009.util.neo4j.cypher.CypherHelper;

public class Matcher {
	
	private GraphDatabaseService graph;
	private ExecutionEngine engine;
	private final String DB_PATH = "C:/Users/Floris/Documents/Neo4j/hardmatch.graphdb";

	public Matcher() {
		createDB();
		ComponentMotherboard board = new ComponentMotherboard();
		board.setName("MSI motherboard");
		getCheapestStoreForComponent(board);
	}
	
    public void createDB() {
        this.graph = new GraphDatabaseFactory().newEmbeddedDatabase(DB_PATH);
        engine = new ExecutionEngine(graph);
    }
    
    public void getCheapestStoreForComponent(Component componentToBuy) {
    	String cypher = "MATCH (component:Component {name:\"MSI motherboard\"})-[:SellsFor]->(price)-[:At]->(store) RETURN component, price, store ORDER BY price.value";
    	ExecutionResult result = CypherHelper.Cypher(engine, cypher);
    	Iterator<Map<String, Object>> itr = result.iterator();
    	if(itr.hasNext()) {
    		Map<String, Object> row = itr.next();
    		Node component = (Node) row.get("component");
    		Node price = (Node) row.get("price");
    		Node store = (Node) row.get("store");
    		System.out.println("Cheapest store for "+component.getProperty("name")+" is "+store.getProperty("name")+" for a price of "+price.getProperty("value"));
    	}
    }
    
    public static void main(String[] args){
        Matcher db=new Matcher();
        JNeoGUI gui = new JNeoGUI(db.graph);
        gui.frame.setVisible(true);
    }

}
