package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentRAM extends AbstractComponent {
	
	public String memoryType;

	public ComponentRAM(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(RAM_MEMORYTYPE)) {
			memoryType = object.get(RAM_MEMORYTYPE).toString();
		}
	}

}
