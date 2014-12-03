package com.hardmatch.checker;

import com.hardmatch.checker.components.ComponentCPU;
import com.hardmatch.checker.components.ComponentGraphicsCard;
import com.hardmatch.checker.components.ComponentMotherboard;
import com.hardmatch.checker.components.ComponentRAM;
import com.hardmatch.checker.components.ComponentStorage;
import com.hardmatch.checker.components.IComponent;

public class CompatibiltyRules {

	public static boolean AreComponentsCompatible(IComponent component1, IComponent component2) {
		if(checkComponents(component1, component2)) {
			System.out.println("CompatibiltyRules.AreComponentsCompatible() true");
			return true;
		} else {
			boolean compatible = checkComponents(component2, component1);
			System.out.println("CompatibiltyRules.AreComponentsCompatible() "+compatible);
			return checkComponents(component2, component1);
		}
	}
	
	private static boolean checkComponents(IComponent component1, IComponent component2) {
		if(component1 instanceof ComponentMotherboard) {
			if(component2 instanceof ComponentCPU) {
				if(((ComponentMotherboard) component1).socket == null || ((ComponentCPU) component2).socket == null || 
						((ComponentMotherboard) component1).socket.equalsIgnoreCase(((ComponentCPU)component2).socket)) {
					System.out.println("CompatibiltyRules.checkComponents() true "+((ComponentMotherboard) component1).socket + " " + ((ComponentCPU) component2).socket);
					return true;
				} else {
					System.out.println("CompatibiltyRules.checkComponents() false");
					return false;
				}
			}
			if(component2 instanceof ComponentStorage) {
				if(((ComponentMotherboard) component1).connectorInterfaceStorage == null || ((ComponentStorage) component2).connectorInterface == null || 
						((ComponentMotherboard) component1).connectorInterfaceStorage.equalsIgnoreCase(((ComponentStorage)component2).connectorInterface)) {
					return true;
				} else {
					return false;
				}
			}
			if(component2 instanceof ComponentRAM) {
				if(((ComponentMotherboard) component1).memoryType == null || ((ComponentRAM) component2).memoryType == null || 
						((ComponentMotherboard) component1).memoryType.equalsIgnoreCase(((ComponentRAM)component2).memoryType)) {
					return true;
				} else {
					return false;
				}
			}
			if(component2 instanceof ComponentGraphicsCard) {
				if(((ComponentMotherboard) component1).connectorInterfaceGraphicsCard == null || ((ComponentGraphicsCard) component2).connectorInterface == null || 
						((ComponentMotherboard) component1).connectorInterfaceGraphicsCard.equalsIgnoreCase(((ComponentGraphicsCard)component2).connectorInterface)) {
					return true;
				} else {
					return false;
				}
			}
		}
		return false;
	}

}
