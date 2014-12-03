package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

public class ComponentFactory {

	private static final String CPU_LABEL = "CPU";
	private static final String MOTHERBOARD_LABEL = "Motherboard";
	private static final String STORAGE_LABEL = "Storage";
	private static final String RAM_LABEL = "RAM";
	private static final String GRAPHICS_CARD_LABEL = "GraphicsCard";
	
	public static IComponent getComponent(JSONObject object, String labels, Long ID) throws UnknownComponentException {
		if(labels.contains(CPU_LABEL)) {
			ComponentCPU component = new ComponentCPU(labels, ID);
			component.populateProperties(object);
			return component;
		} else if(labels.contains(MOTHERBOARD_LABEL)) {
			ComponentMotherboard component = new ComponentMotherboard(labels, ID);
			component.populateProperties(object);
			return component;
		} else if(labels.contains(STORAGE_LABEL)) {
			ComponentStorage component = new ComponentStorage(labels, ID);
			component.populateProperties(object);
			return component;
		} else if(labels.contains(RAM_LABEL)) {
			ComponentRAM component = new ComponentRAM(labels, ID);
			component.populateProperties(object);
			return component;
		} else if(labels.contains(GRAPHICS_CARD_LABEL)) {
			ComponentGraphicsCard component = new ComponentGraphicsCard(labels, ID);
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
