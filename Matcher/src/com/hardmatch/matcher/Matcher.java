package com.hardmatch.matcher;

import org.neo4j.cypher.javacompat.ExecutionEngine;
import org.neo4j.graphdb.GraphDatabaseService;
import org.neo4j.graphdb.factory.GraphDatabaseFactory;

public class Matcher {

	public Matcher() {
	}
	
	private GraphDatabaseService graph;
	private final String DB_PATH = "C:\\Program Files (x86)\\Neo4j Community";

    public void createDB() {
        this.graph = new GraphDatabaseFactory().newEmbeddedDatabase(DB_PATH);
        new ExecutionEngine(graph);
    }
    
    public static void main(String[] args){
        Matcher db=new Matcher();
        db.createDB();
        JNeoGUI gui = new JNeoGUI(db.graph);
        gui.frame.setVisible(true);
    }

}
