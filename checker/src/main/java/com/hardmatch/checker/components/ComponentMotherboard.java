package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentMotherboard extends AbstractComponent {

	public String socket;

	public ComponentMotherboard(String labels, Long ID) {
		super(labels, ID);
	}

	public boolean isCompatibleWith(IComponent other) {
		if(other instanceof ComponentCPU) {
			if(((ComponentCPU) other).socket == null || !((ComponentCPU) other).socket.equalsIgnoreCase(socket)) {
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
