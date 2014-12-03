package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentRAM extends AbstractComponent {
	
	public String memoryType;

	public ComponentRAM(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(MEMORY_TYPE_LABEL)) {
			memoryType = object.get(MEMORY_TYPE_LABEL).toString();
		}
	}

}
