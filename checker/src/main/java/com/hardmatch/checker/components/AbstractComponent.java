package com.hardmatch.checker.components;

import org.json.simple.JSONObject;

import com.hardmatch.checker.CompatibilityChecker;

public abstract class AbstractComponent implements IComponent {
	
	private Long ID;
	private String labels;
	private String modelID;

	public AbstractComponent(String labels, Long ID) {
		this.labels = labels;
		this.ID = ID;
	}

	public boolean isCompatibleWith(IComponent other) {
		boolean compatible = CompatibilityChecker.AreComponentsCompatible(this, other);
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
	public static final String SOCKET_LABEL = "Socket";
	public static final String CAPACITY_LABEL = "capacity";
	public static final String INTERFACE_STORAGE_LABEL = "interfaceStorage"; 
	public static final String INTERFACE_GRAPHICS_CARD_LABEL = "Card Interface (Video)"; 
	public static final String MEMORY_TYPE_LABEL = "Geheugentype (moederbord)"; 

}
