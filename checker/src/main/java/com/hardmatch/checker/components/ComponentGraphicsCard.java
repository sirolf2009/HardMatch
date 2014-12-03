package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentGraphicsCard extends AbstractComponent {

	public String connectorInterface;

	public ComponentGraphicsCard(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(INTERFACE_GRAPHICS_CARD_LABEL)) {
			connectorInterface = object.get(INTERFACE_GRAPHICS_CARD_LABEL).toString();
		}
	}
}
