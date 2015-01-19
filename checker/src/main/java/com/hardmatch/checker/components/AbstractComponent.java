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

	public static final String MODEL_ID = "ModelID";

	public static final String MOTHERBOARD_SOCKET = "Socket";
	public static final String MOTHERBOARD_FORMFACTOR = "FormFactor";
	public static final String MOTHERBOARD_CARDINTERFACE = "CardInterface";
	public static final String MOTHERBOARD_MEMORYTYPE = "GeheugenType";

	public static final String CPU_SOCKET = "Socket";

	public static final String GFX_INTERFACE = "CardInterface";
	
	public static final String RAM_MEMORYTYPE = "GeheugenType";

	public static final String CPUFAN_SOCKET = "Socket";
	
	public static final String CASE_MOTHERBOARD_FORMFACTOR = "FormFactor";

	public static final String STORAGE_BAY = "BehuizingBayIntern";
	
}
