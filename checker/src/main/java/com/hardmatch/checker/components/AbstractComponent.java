package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

import com.hardmatch.checker.CompatibilityRules;

/**
* An abstract class that implements {@link IComponent}
*
* @author  Zara Ali
* @version 1.0
* @since   2014-03-31 
*/
public abstract class AbstractComponent implements IComponent {
	
	private Long ID;
	private String labels;
	private String modelID;

	public AbstractComponent(String labels, Long ID) {
		this.labels = labels;
		this.ID = ID;
	}

	public boolean isCompatibleWith(IComponent other) {
		boolean compatible = CompatibilityRules.AreComponentsCompatible(this, other);
		System.out.println("AbstractComponent.isCompatibleWith() "+compatible);
		return compatible;
	}

	public void populateProperties(JSONObject object) {
		modelID = object.get(MODEL_ID).toString();
	}
	
	public String getModelID() {
		return modelID;
	}

	public long getID() {
		return ID;
	}

	public String getLabels() {
		return labels;
	}

	public static final String MODEL_ID = "modelID";
	public static final String SOCKET_LABEL = "socket";
	public static final String CAPACITY_LABEL = "capacity";
	public static final String INTERFACE_STORAGE_LABEL = "interfaceStorage"; 
	public static final String INTERFACE_GRAPHICS_CARD_LABEL = "interfaceGraphics"; 
	public static final String MEMORY_TYPE_LABEL = "Geheugentype"; 

}
