package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentCase extends AbstractComponent {
	
	public String[] formFactor;

	public ComponentCase(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(CASE_MOTHERBOARD_FORMFACTOR)) {
			formFactor = object.get(CASE_MOTHERBOARD_FORMFACTOR).toString().split(", ");
		}
	}
}
