package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentCPU extends AbstractComponent {

	public String socket;

	public ComponentCPU(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(CPU_SOCKET)) {
			socket = object.get(CPU_SOCKET).toString();
		}
	}

}
