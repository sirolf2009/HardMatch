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

			new Twig_SimpleFunction("getNodeName", function ($node, $option=null) {
				if ($option === null){
					return $node->getProperty('name');					
				} else{
					return $node[$option]->getProperty('name');
				}
			}),

			new Twig_SimpleFunction("getNodeDesc", function ($node, $option=null) {
				if ($option === null){
					return $node->getProperty('description');
				} else {
					return $node[$option]->getProperty('description');
				}				
			}),

			new Twig_SimpleFunction("getNodeCat", function ($node, $option=null) {
				if ($option === null){
					return $node->getProperty('category');
				} else {
					return $node[$option]->getProperty('category');
				}				
			}),

			new Twig_SimpleFunction("getNodePrice", function ($node, $option=null) {
				if ($option === null){
					return $node->getProperty('price');
				} else {
					return $node[$option]->getProperty('price');
				}				
			}),
			);
}
}
?>