package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentMotherboard extends AbstractComponent {

	public String socket;
	public String connectorInterfaceStorage;
	public String connectorInterfaceGraphicsCard;
	public String memoryType;

	public ComponentMotherboard(String labels, Long ID) {
		super(labels, ID);
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		if(object.containsKey(SOCKET_LABEL)) {
			socket = object.get(SOCKET_LABEL).toString();
		}
		if(object.containsKey(INTERFACE_STORAGE_LABEL)) {
			connectorInterfaceStorage = object.get(INTERFACE_STORAGE_LABEL).toString();
		}
		if(object.containsKey(INTERFACE_GRAPHICS_CARD_LABEL)) {
			connectorInterfaceGraphicsCard= object.get(INTERFACE_GRAPHICS_CARD_LABEL).toString();
		}
		if(object.containsKey(MEMORY_TYPE_LABEL)) {
			memoryType = object.get(MEMORY_TYPE_LABEL).toString();
		}
	}
}
