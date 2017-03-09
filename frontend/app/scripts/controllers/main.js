'use strict';

angular.module('documentosApp').controller('MainCtrl', function ($scope, $location, DataService) {
	/*
	function onError(data){
		console.log(data);
	}

	function onSuccessResumen(data){
		$scope.resumen = [""];
		$scope.resumen = data["resumen"].split("\n"); 
		//console.log(data);
	}

	function onSuccessTopicos(data){
		$scope.topicos = "";
		$scope.topicos = data["topicos"];
	}

	var convertLevelResumen = function(text){
		if (text === 'Alto') {
			return 1 
		} else if (text === 'Medio') { 
			return 2
		} else { 
			return 3 
		}
	};

	var convertLevelTopicos = function(text){
		if (text === 'Cinco') { 
			return 1 
		} else if (text === 'Siete') { 
			return 2 
		} else { 
			return 3 
		}
	};

	$scope.mostrarResumen = function(){
	
		if($scope.pointSelectResumen && $scope.levelSelectResumen){

			var params;
			if($scope.pointSelectResumen === 'Documento completo'){
				params = {
					punto: 0,
					nivel:convertLevelResumen($scope.levelSelectResumen)
				}
			}
			else{
				params = {
					punto: parseInt($scope.pointSelectResumen.replace("Punto ", "")),
					nivel:convertLevelResumen($scope.levelSelectResumen)
				}
			}
			console.log(params);	
			DataService.getResumen(params, onSuccessResumen, onError);
		}
	};

	$scope.mostrarTopicos = function(){
		var params;
		if($scope.pointSelectTopicos === 'Documento completo'){
			params = {
				punto: 0,
				numero: convertLevelTopicos($scope.numberSelectTopicos)
			}
		}
		else{
			params = {
				punto: parseInt($scope.pointSelectTopicos.replace("Punto ", "")),
				numero:convertLevelTopicos($scope.numberSelectTopicos)
			}
		}
		//console.log(params);	
		DataService.getTopicos(params, onSuccessTopicos, onError);
	};

	function onSuccessFrecuencias(data){

		
		var chart = c3.generate({
		    data: {
		        columns: [
		            ['politica'].concat(data["politica"]),
		            ['justicia'].concat(data["justicia"]),
		            ['tierras'].concat(data["tierras"]),
		            ['posconflicto'].concat(data["posconflicto"]),
		            ['reparacion'].concat(data["reparacion"])
		        ],
		        type: 'bar',
		        groups: [
		            ['politica', 'justicia', 'tierras', 'posconflicto', 'reparacion']
		        ]
		    },
		    axis: {
			    x: {
			        type: 'category',
			        categories: ['Documento completo', 'Punto 1: Reforma Rural Integral', 'Punto 2: Participación política', 'Punto 3: Fin del Conflicto', 'Punto 4: Problema de las Drogas Ilícitas', 'Punto 5: Reparación de víctimas', 'Punto 6: Implementación, verificación y refrendación']
			    }
			},
			legend: {
				position: 'right'
			}
		});
		
		chart.resize({height:500});


	}

	$scope.mostrarNube = function(){

		$scope.showAll = false;
		$scope.showPunto1 = false;
		$scope.showPunto2 = false;
		$scope.showPunto3 = false;
		$scope.showPunto4 = false;
		$scope.showPunto5 = false;
		$scope.showPunto6 = false;

		var point_chosen = $scope.pointSelectNube;
		switch(point_chosen){
			case "Documento completo":
				$scope.showAll = true;
				break;
			case "Punto 1":
				$scope.showPunto1 = true;
				break;
			case "Punto 2":
				$scope.showPunto2 = true;
				break;
			case "Punto 3":
				$scope.showPunto3 = true;
				break;
			case "Punto 4":
				$scope.showPunto4 = true;
				break;
			case "Punto 5":
				$scope.showPunto5 = true;
				break;
			case "Punto 6":
				$scope.showPunto6 = true;
				break;
			default:
				$scope.showAll = true;
		}

	};

	function drawGraph(){

		// Define the dimensions of the visualization. We're using
		// a size that's convenient for displaying the graphic on
		// http://jsDataV.is

		var width = 640,
		    height = 480;

		// Define the data for the example. In general, a force layout
		// requires two data arrays. The first array, here named `nodes`,
		// contains the object that are the focal point of the visualization.
		// The second array, called `links` below, identifies all the links
		// between the nodes. (The more mathematical term is "edges.")

		// For the simplest possible example we only define two nodes. As
		// far as D3 is concerned, nodes are arbitrary objects. Normally the
		// objects wouldn't be initialized with `x` and `y` properties like
		// we're doing below. When those properties are present, they tell
		// D3 where to place the nodes before the force layout starts its
		// magic. More typically, they're left out of the nodes and D3 picks
		// random locations for each node. We're defining them here so we can
		// get a consistent application of the layout which lets us see the
		// effects of different properties.

		var nodes = [
		    { x:   width/3, y: height/2 },
		    { x: 2*width/3, y: height/2 }
		];

		// The `links` array contains objects with a `source` and a `target`
		// property. The values of those properties are the indices in
		// the `nodes` array of the two endpoints of the link.

		var links = [
		    { source: 0, target: 1 }
		];

		// Here's were the code begins. We start off by creating an SVG
		// container to hold the visualization. We only need to specify
		// the dimensions for this container.

		var svg = d3.select('body').append('svg')
		    .attr('width', width)
		    .attr('height', height);

		// Now we create a force layout object and define its properties.
		// Those include the dimensions of the visualization and the arrays
		// of nodes and links.

		var force = d3.layout.force()
		    .size([width, height])
		    .nodes(nodes)
		    .links(links);

		// There's one more property of the layout we need to define,
		// its `linkDistance`. That's generally a configurable value and,
		// for a first example, we'd normally leave it at its default.
		// Unfortunately, the default value results in a visualization
		// that's not especially clear. This parameter defines the
		// distance (normally in pixels) that we'd like to have between
		// nodes that are connected. (It is, thus, the length we'd
		// like our links to have.)

		force.linkDistance(width/2);

		// Next we'll add the nodes and links to the visualization.
		// Note that we're just sticking them into the SVG container
		// at this point. We start with the links. The order here is
		// important because we want the nodes to appear "on top of"
		// the links. SVG doesn't really have a convenient equivalent
		// to HTML's `z-index`; instead it relies on the order of the
		// elements in the markup. By adding the nodes _after_ the
		// links we ensure that nodes appear on top of links.

		// Links are pretty simple. They're just SVG lines, and
		// we're not even going to specify their coordinates. (We'll
		// let the force layout take care of that.) Without any
		// coordinates, the lines won't even be visible, but the
		// markup will be sitting inside the SVG container ready
		// and waiting for the force layout.

		var link = svg.selectAll('.link')
		    .data(links)
		    .enter().append('line')
		    .attr('class', 'link');

		// Now it's the nodes turn. Each node is drawn as a circle.

		var node = svg.selectAll('.node')
		    .data(nodes)
		    .enter().append('circle')
		    .attr('class', 'node');

		// We're about to tell the force layout to start its
		// calculations. We do, however, want to know when those
		// calculations are complete, so before we kick things off
		// we'll define a function that we want the layout to call
		// once the calculations are done.

		force.on('end', function() {

		    // When this function executes, the force layout
		    // calculations have concluded. The layout will
		    // have set various properties in our nodes and
		    // links objects that we can use to position them
		    // within the SVG container.

		    // First let's reposition the nodes. As the force
		    // layout runs it updates the `x` and `y` properties
		    // that define where the node should be centered.
		    // To move the node, we set the appropriate SVG
		    // attributes to their new values. We also have to
		    // give the node a non-zero radius so that it's visible
		    // in the container.

		    node.attr('r', width/25)
		        .attr('cx', function(d) { return d.x; })
		        .attr('cy', function(d) { return d.y; });

		    // We also need to update positions of the links.
		    // For those elements, the force layout sets the
		    // `source` and `target` properties, specifying
		    // `x` and `y` values in each case.

		    link.attr('x1', function(d) { return d.source.x; })
		        .attr('y1', function(d) { return d.source.y; })
		        .attr('x2', function(d) { return d.target.x; })
		        .attr('y2', function(d) { return d.target.y; });

		});

		// Okay, everything is set up now so it's time to turn
		// things over to the force layout. Here we go.

		force.start();

		// By the time you've read this far in the code, the force
		// layout has undoubtedly finished its work. Unless something
		// went horribly wrong, you should see two light grey circles
		// connected by a single dark grey line. If you have a screen
		// ruler (such as [xScope](http://xscopeapp.com) handy, measure
		// the distance between the centers of the two circles. It
		// should be somewhere close to the `linkDistance` parameter we
		// set way up in the beginning (480 pixels). That, in the most
		// basic of all nutshells, is what a force layout does. We
		// tell it how far apart we want connected nodes to be, and
		// the layout keeps moving the nodes around until they get
		// reasonably close to that value.

		// Of course, there's quite a bit more than that going on
		// under the hood. We'll take a closer look starting with
		// the next example.

	}

	$scope.init = function(){

		$scope.pointSelectResumen = "Punto 1";
		$scope.pointSelectTopicos = "Punto 1";
		$scope.pointSelectNube = "Punto 1";
		$scope.levelSelectResumen = "Alto";
		$scope.numberSelectTopicos = "Cinco";

		$scope.showAll = true;
		$scope.showPunto1 = false;
		$scope.showPunto2 = false;
		$scope.showPunto3 = false;
		$scope.showPunto4 = false;
		$scope.showPunto5 = false;
		$scope.showPunto6 = false;

		var params;
		params = {
			punto: 1,
			nivel: 1
		};
		DataService.getResumen(params, onSuccessResumen, onError);

		params = {
			punto: 1,
			numero: 1
		};
		DataService.getTopicos(params, onSuccessTopicos, onError);

		DataService.getFrecuencias(onSuccessFrecuencias, onError);

	};
	*/

});