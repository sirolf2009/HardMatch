package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentCPUFan extends AbstractComponent {
	
	public String[] socket;

	public ComponentCPUFan(String labels, Long ID) {
		super(labels, ID);
	}
	
	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(CPUFAN_SOCKET)) {
			socket = object.get(CPUFAN_SOCKET).toString().split(", ");
		}
	}

}
