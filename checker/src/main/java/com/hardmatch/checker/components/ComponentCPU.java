package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentCPU extends AbstractComponent {
	
	public String socket;

	public ComponentCPU(String labels, Long ID) {
		super(labels, ID);
	}

	public boolean isCompatibleWith(IComponent other) {
		if(other instanceof ComponentMotherboard) {
			if(((ComponentMotherboard) other).socket == null || !((ComponentMotherboard) other).socket.equalsIgnoreCase(socket)) {
				return false;
			}
		}
		return true;
	}

	public void populateProperties(JSONObject object) {
		super.populateProperties(object);
		socket = object.get(SOCKET_LABEL).toString();
	}

}
