package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentStorage extends AbstractComponent {

	public String bay;

	public ComponentStorage(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(STORAGE_BAY)) {
			bay = object.get(STORAGE_BAY).toString();
		}
	}

}
