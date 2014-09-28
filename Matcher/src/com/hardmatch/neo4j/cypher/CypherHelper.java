package com.hardmatch.neo4j.cypher;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.neo4j.cypher.javacompat.ExecutionEngine;
import org.neo4j.cypher.javacompat.ExecutionResult;
import org.neo4j.graphdb.Node;
import org.neo4j.helpers.collection.IteratorUtil;

public abstract class CypherHelper {

	private static Logger log = Logger.getLogger("com.hardmatch.matcher.neo4j.cypher.CypherHelper");

	public static Node FindNode(ExecutionEngine engine, String label) {
		return FindNodeByProperties(engine, label, null);
	}

	public static List<Node> FindNodes(ExecutionEngine engine, String label) {
		return FindNodesByProperties(engine, label, null);
	}

	public static Node FindNodeByProperties(ExecutionEngine engine, String label, Map<String, Object> properties) {
		List<Node> nodes = FindNodesByProperties(engine, label, properties);
		if(nodes.size() > 0) {
			return FindNodesByProperties(engine, label, properties).get(0);
		}
		return null;
	}

	public static List<Node> FindNodesByProperties(ExecutionEngine engine, String label, Map<String, Object> properties) {
		return FindNodesByPropertiesRelation(engine, label, properties, null);
	}
	
	public static List<Node> FindNodesByRelation(ExecutionEngine engine, String label, String relation) {
		return FindNodesByPropertiesRelation(engine, label, null, relation);
	}
	
	public static Node FindNodeByRelation(ExecutionEngine engine, String label, String relation) {
		List<Node> nodes = FindNodesByPropertiesRelation(engine, label, null, relation);
		if(nodes.size() > 0) {
			return FindNodesByPropertiesRelation(engine, label, null, relation).get(0);
		}
		return null;
	}

	public static List<Node> FindNodesByPropertiesRelation(ExecutionEngine engine, String label, Map<String, Object> properties, String relation) {
		ExecutionResult result;
		if(properties != null) {
			String props = "";
			for(String key : properties.keySet()) {
				props += key+": "+properties.get(key);
			}
			if(relation != null && !relation.isEmpty()) {
				result = Cypher(engine, "MATCH (result:"+label+" {"+props+"})<-[:"+relation+"]-(actor) return result");
			} else {
				result = Cypher(engine, "MATCH (result:"+label+" {"+props+"}) return result");
			}
		} else {
			if(relation != null && !relation.isEmpty()) {
				result = Cypher(engine, "MATCH (result:"+label+")<-[:"+relation+"]-(actor) return result");
			} else {
				result = Cypher(engine, "MATCH (result:"+label+") return result");
			}
		}

		return GetNodesFromResult(result);
	}
	
	public static List<Node> GetAllNodes(ExecutionEngine engine) {
		return GetNodesFromResult(Cypher(engine, "MATCH(result) return result"));
	}

	public static ExecutionResult Cypher(ExecutionEngine engine, String cypher) {
		log.log(Level.INFO, "Sending Cypher: "+cypher);
		ExecutionResult result = engine.execute(cypher);
		//TODO send result.getQueryStatistics() to analyzer
		return result;
	}
	
	public static List<Node> GetNodesFromResult(ExecutionResult result) {
		List<Node> nodes = new ArrayList<Node>();
		Iterator<Node> columnResult = result.columnAs("result");
		for (Node node : IteratorUtil.asIterable(columnResult)) {
			nodes.add(node);
		}
		return nodes;
	}

}
