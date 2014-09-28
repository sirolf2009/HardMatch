package com.hardmatch.matcher.component;

public abstract class Component {
	
	private float price;
	private String name;
	private ComponentType type;

	public Component() {
	}
	
	public boolean isCompitableWith(Component component) {
		return false;
	}

	public float getPrice() {
		return price;
	}

	public void setPrice(float price) {
		this.price = price;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public ComponentType getComponentType() {
		return type;
	}

	public void setComponentType(ComponentType type) {
		this.type = type;
	}

}
