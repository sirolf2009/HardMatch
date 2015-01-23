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

			new Twig_SimpleFunction("getNodePrice", function ($node, $option=null) {
				if ($option === null){
					$relations = $node->getRelationships(array('SOLD_AT'));					
				} else{
					$relations = $node[$option]->getRelationships(array('SOLD_AT'));
				}
				return "€".$relations[0]->getProperty('Price');
			}),

			);
	}
}
?>