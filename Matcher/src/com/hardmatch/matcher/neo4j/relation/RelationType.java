package com.hardmatch.matcher.neo4j.relation;

import org.neo4j.graphdb.RelationshipType;

public enum RelationType implements RelationshipType {

	CONNECTED,
	
	SOLD_BY,
	SELLS
	
}
