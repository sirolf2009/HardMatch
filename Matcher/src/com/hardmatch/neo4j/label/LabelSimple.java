package com.hardmatch.neo4j.label;

import org.neo4j.graphdb.Label;

public class LabelSimple implements Label {

	private String name;
	
	public LabelSimple(String name) {
		this.name = name;
	}

	@Override
	public String name() {
		return name;
	}

}
