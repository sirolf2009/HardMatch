package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentMotherboard extends AbstractComponent {

	public String socket;
	public String connectorInterfaceGraphicsCard;
	public String memoryType;
	public String formFactor;

	public ComponentMotherboard(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(MOTHERBOARD_SOCKET)) {
			socket = object.get(MOTHERBOARD_SOCKET).toString();
		}
		if(object.containsKey(MOTHERBOARD_CARDINTERFACE)) {
			connectorInterfaceGraphicsCard= object.get(MOTHERBOARD_CARDINTERFACE).toString();
		}
		if(object.containsKey(MOTHERBOARD_MEMORYTYPE)) {
			memoryType = object.get(MOTHERBOARD_MEMORYTYPE).toString();
		}
		if(object.containsKey(MOTHERBOARD_FORMFACTOR)) {
			formFactor = object.get(MOTHERBOARD_FORMFACTOR).toString();
		}
	}
}
