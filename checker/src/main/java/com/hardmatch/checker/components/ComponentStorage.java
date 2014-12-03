package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentStorage extends AbstractComponent {

	public double capacity;
	public String connectorInterface;

	public ComponentStorage(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(CAPACITY_LABEL)) {
			capacity = Double.parseDouble(object.get(CAPACITY_LABEL).toString());
		}
		if(object.containsKey(INTERFACE_STORAGE_LABEL)) {
			connectorInterface = object.get(INTERFACE_STORAGE_LABEL).toString();
		}
	}

}
