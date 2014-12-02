package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentFactory {

	private static final String CPU_LABEL = "CPU";
	private static final String MOTHERBOARD_LABEL = "Motherboard";

	public ComponentFactory() {
	}
	
	public static IComponent getComponent(JSONObject object, String labels, Long ID) throws UnknownComponentException {
		if(labels.contains(CPU_LABEL)) {
			ComponentCPU component = new ComponentCPU(labels, ID);
			component.populateProperties(object);
			return component;
		} else if(labels.contains(MOTHERBOARD_LABEL)) {
			ComponentMotherboard component = new ComponentMotherboard(labels, ID);
			component.populateProperties(object);
			return component;
		}
		throw new UnknownComponentException(object, labels);
	}
	
	public static class UnknownComponentException extends Exception {
		
		private static final long serialVersionUID = 1355992337700594514L;

		public UnknownComponentException(JSONObject object, String labels) {
			super("Could not create a component\n\tObject: "+object+"\n\tlabels: "+labels);
		}
	}

}
