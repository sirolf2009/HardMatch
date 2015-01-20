<?php
class NodeExtension extends Twig_Extension
{
	public function getName()
	{
		return 'NodeExtension';
	}

	public function getFunctions()
	{
		return array(
			new Twig_SimpleFunction("getNodeID", function ($node, $option=null) {
				if ($option === null){
					return $node->getId();
				} else {
					return $node[$option]->getId();
				}				
			}),

			new Twig_SimpleFunction("getNodeProperty", function ($node, $property, $option=null) {
				if ($option === null){
					return $node->getProperty($property);					
				} else{
					return $node[$option]->getProperty($property);
				}
			}),

			);
	}
}
?>