package com.hardmatch.checker;

import com.hardmatch.checker.components.ComponentCPU;
import com.hardmatch.checker.components.ComponentCPUFan;
import com.hardmatch.checker.components.ComponentCase;
import com.hardmatch.checker.components.ComponentGraphicsCard;
import com.hardmatch.checker.components.ComponentMotherboard;
import com.hardmatch.checker.components.ComponentRAM;
import com.hardmatch.checker.components.IComponent;

public class CompatibilityChecker {
	
	public static SynonymChecker synonymChecker = new SynonymChecker();

	public static boolean AreComponentsCompatible(IComponent component1, IComponent component2) {
		if(checkComponents(component1, component2)) {
			return true;
		} else {
			return checkComponents(component2, component1);
		}
	}
	
	private static boolean checkComponents(IComponent component1, IComponent component2) {
		if(component1 instanceof ComponentMotherboard) {
			if(component2 instanceof ComponentCPU) {
				if(((ComponentMotherboard) component1).socket == null || ((ComponentCPU) component2).socket == null || 
						checkStrings(((ComponentMotherboard) component1).socket, ((ComponentCPU)component2).socket)) {
					return true;
				} else {
					return false;
				}
			}
			if(component2 instanceof ComponentRAM) {
				if(((ComponentMotherboard) component1).memoryType == null || ((ComponentRAM) component2).memoryType == null || 
						checkStrings(((ComponentMotherboard) component1).memoryType, ((ComponentRAM)component2).memoryType)) {
					return true;
				} else {
					return false;
				}
			}
			if(component2 instanceof ComponentGraphicsCard) {
				if(((ComponentMotherboard) component1).connectorInterfaceGraphicsCard == null || ((ComponentGraphicsCard) component2).connectorInterface == null || 
						checkStrings(((ComponentMotherboard) component1).connectorInterfaceGraphicsCard, ((ComponentGraphicsCard)component2).connectorInterface)) {
					return true;
				} else {
					return false;
				}
			}
			if(component2 instanceof ComponentCase) {
				if(((ComponentMotherboard) component1).formFactor == null || ((ComponentCase) component2).formFactor == null || 
						checkStrings(((ComponentMotherboard) component1).formFactor, ((ComponentCase)component2).formFactor)) {
					return true;
				} else {
					return false;
				}
			}
			if(component2 instanceof ComponentCPUFan) {
				if(((ComponentMotherboard) component1).socket == null || ((ComponentCPUFan) component2).socket == null || 
						checkStrings(((ComponentMotherboard) component1).socket, ((ComponentCPUFan)component2).socket)) {
					return true;
				} else {
					return false;
				}
			}
		}
		if(component1 instanceof ComponentCPU) {
			if(component2 instanceof ComponentCPUFan) {
				if(((ComponentCPU) component1).socket == null || ((ComponentCPUFan) component2).socket == null || 
						checkStrings(((ComponentCPU) component1).socket, ((ComponentCPUFan)component2).socket)) {
					return true;
				} else {
					return false;
				}
			}
		}
		return false;
	}
	
	public static boolean checkStrings(String string1, String string2) {
		if(string1.equalsIgnoreCase(string2) || synonymChecker.areEqual(string1, string2)) {
			return true;
		}
		return false;
	}
	
	public static boolean checkStrings(String string1, String[] string2) {
		for(String string : string2) {
			if(checkStrings(string1, string)) {
				return true;
			}
		}
		return false;
	}

}
