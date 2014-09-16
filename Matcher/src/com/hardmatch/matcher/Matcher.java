package com.hardmatch.matcher;

import java.util.List;

import org.neo4j.cypher.javacompat.ExecutionEngine;
import org.neo4j.cypher.javacompat.ExecutionResult;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.Label;
import org.neo4j.graphdb.Node;
import org.neo4j.graphdb.RelationshipType;
import org.neo4j.graphdb.Transaction;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;

import com.hardmatch.matcher.neo4j.cypher.CypherHelper;
import com.hardmatch.matcher.neo4j.label.LabelSimple;

public class Matcher {

	public Matcher() {
	}
	
	private GraphDatabaseService graph;
	private ExecutionEngine engine;
    private final String DB_PATH = "C:\\Program Files (x86)\\Neo4j Community";

    public void createDB() {
        this.graph = new GraphDatabaseFactory().newEmbeddedDatabase(DB_PATH);
        this.engine = new ExecutionEngine(graph);
    }
    
    public void vulDB() {
        try (Transaction tx = graph.beginTx()) {
            Node cc1 = graph.createNode(new LabelMatch("Node 1"));
            cc1.setProperty("Node Number", "1");

            Node cc2 = graph.createNode(new LabelMatch("Node 2"));
            cc2.setProperty("Node Number", "2");
            
            cc1.createRelationshipTo(cc2, RelationType.CONNECTED)
                    .setProperty("Relation Number", "1");
            tx.success();
        }
        System.out.println("vulDB()");
    }// vulDB()

    public String query() {
        String vraag = "";

        vraag = "MATCH (e:ID0) "
                + " RETURN e";
        
        System.out.println("method query\n"+vraag);
        
        ExecutionEngine engine = new ExecutionEngine(graph);
        ExecutionResult result = engine.execute(vraag);
        
        String dump=result.dumpToString();
        List<String> lijst=result.columns();
        for(String kol: lijst){
            System.out.println("-kol-"+kol);
        }
        return dump;

    }
    
    public void registerShutdownHook() {
        Runtime.getRuntime().addShutdownHook(new Thread() {
            @Override
            public void run() {
                graph.shutdown();
            }
        });

        System.out.println("graphDB shut down.");
    }
    
    
    public static void main(String[] args){
        Matcher db=new Matcher();
        db.createDB();
        
        try (Transaction tx = db.graph.beginTx()) {
            Node cc1 = db.graph.createNode(new LabelSimple("Hello"));

            Node cc2 = db.graph.createNode(new LabelSimple("World"));
            
            cc1.createRelationshipTo(cc2, RelationType.CONNECTED);
            tx.success();
        }
        
        System.out.println(CypherHelper.FindNode(db.engine, "Hello"));
        
        JNeoGUI gui = new JNeoGUI(db.graph);
        gui.frame.setVisible(true);
    }
    
    class LabelMatch implements Label {
    	
    	private String name;
    	
    	public LabelMatch(String name) {
    		this.name = name;
    	}

		@Override
		public String name() {
			return name;
		}
    	
    }
    
    enum RelationType implements RelationshipType {
    	CONNECTED
    }

}
