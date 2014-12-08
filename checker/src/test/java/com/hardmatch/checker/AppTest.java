package com.hardmatch.checker;

import org.junit.Assert;
import org.junit.Test;

public class AppTest {
	
	@Test
	public void testSynonymChecker() {
		SynonymChecker checker = new SynonymChecker();
		Assert.assertEquals(true, checker.areEqual("PCIe", "PCI-e"));
		Assert.assertEquals(true, checker.areEqual("SATA", "Serieel ATA"));
		Assert.assertEquals(false, checker.areEqual("PCIe", "SATA"));
	}

} 
