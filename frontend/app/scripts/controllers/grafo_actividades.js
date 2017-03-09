'use strict';

angular.module('documentosApp').controller('GrafoActividadesCtrl', function ($scope, $location, DataService, RedirectService) {
	



	var frente_escogido = "";
	$scope.frente_actividades = "";
	$scope.actividad_actividades = "";
	$scope.contexto = "";
	var div = document.getElementById('grafo2');
	$scope.mostrarContexto=false;
	$scope.excepcion="";



	function onError(data){
		$scope.excepcion="No se encontraron resultados";
		if(div.firstChild){
		  $("#grafo2").empty();
	  	}
		console.log(data);
	}

	function onSuccessGrafoActividades(data){ 
		console.log(data);
		drawGraph2(data);

	}

	$scope.pintarGrafoActividades = function(){

		var params;
		params = {
			frente: $scope.frente_actividades,
			actividad: $scope.actividad_actividades
		};
		if($scope.frente_actividades==="" )
		{
			$scope.excepcion="Introduzca el frente";
		}
		else{
			console.log(params);
			DataService.getGrafoActividades(params, onSuccessGrafoActividades, onError);
		}
	};

	$scope.limpiarActividades = function(){
		$scope.frente_actividades = "";
		$scope.actividad_actividades = "";
		$scope.contexto = "";
		if(div.firstChild){
		  $("#grafo2").empty();
	  	}
	  	$scope.mostrarContexto=false;
	  	$scope.excepcion="";
	};

	function drawGraph2(graph){

	  var width = 945,
		  height = 800

	  	$scope.excepcion="";
	  if(div.firstChild){
		  $("#grafo2").empty();
		  	}

	  var svg = d3.select("#grafo2").append("svg")
			.attr("width", width)
			.attr("height", height)
	

	  var color = d3.scaleOrdinal(d3.schemeCategory20);

	  
	  var simulation = d3.forceSimulation()
	    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(50))
	    .force("collide",d3.forceCollide( function(d){return d.r + 8 }))
	    .force("charge", d3.forceManyBody())
	    .force("center", d3.forceCenter(width / 2, height / 2));

	  simulation
		.nodes(graph.nodos);
	  
	  simulation
		.force("link")
		.links(graph.aristas);

	  var link = svg.selectAll(".link")
		  .data(graph.aristas)
		  .enter().append("line")
		  .attr("class", "link")
		  .attr("stroke-width", function(d) { return 1; });

	

	  var node = svg.selectAll(".node")
		  .data(graph.nodos)
		.enter().append("g")
		  .attr("class", "node");
/*	  
	
	  var linkText = svg.selectAll(".gLink")
		  .data(graph.aristas)
		  .enter().append("text")
		  .attr("font-family", "Arial, Helvetica, sans-serif")
		  .attr("x", function(d) {
			  return (d.source.x + d.target.x)/2;
		  })
		  .attr("y", function(d) {
			  return (d.source.y + d.target.y)/2;
		  })
		  .attr("fill", "Black")
		  .style("font", "normal 12px Arial")
		  .attr("dy", ".35em")
		  .text(function(d) { return "link"; });
*/
  	  node.append("circle")
	  .attr("r", function(d){ if(d.tipo_de_nodo === 'frente'){ return 30; } else { if(d.tipo_de_nodo==='actividad'){ return 15;} else {return 5; } }})
	  .style("fill", function(d){ if(d.tipo_de_nodo ==='frente'){ return "#641e16" ;} else if(d.tipo_de_nodo === 'actividad'){ return " #21618c ";}else if(d.tipo_de_nodo === 'característica'){ return "black";} else {return "#28b463";}})
	  .style("stroke", function(d){ if(d.tipo_de_nodo ==='frente'){ return "#641e16" ;} else if(d.tipo_de_nodo === 'actividad'){ return " #21618c ";}else if(d.tipo_de_nodo === 'característica'){ return "black";} else {return "#28b463";}});

		  
	  node.on("click", function(d){ $scope.contexto = d.contexto, $scope.mostrarContexto=true, $scope.$applyAsync(), console.log(d); })
		  .call(d3.drag()
			  .on("start", dragstarted)
			  .on("drag", dragged)
			  .on("end", dragended));

	  node.append("title")
		  .attr("dx", 12)
		  .attr("dy", ".35em")
		  .text(function(d) { return d.id });

	  simulation.on("tick", function() {
		link.attr("x1", function(d) { return d.source.x; })
			.attr("y1", function(d) { return d.source.y; })
			.attr("x2", function(d) { return d.target.x; })
			.attr("y2", function(d) { return d.target.y; });
			/*
		linkText.attr("x", function(d) { return (d.source.x + d.target.x)/2; })
				.attr("y", function(d) { return (d.source.y + d.target.y)/2; });
			*/
		node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
	  });

	  

	  function dragstarted(d) {
		if (!d3.event.active) simulation.alphaTarget(0.3).restart();
		d.fx = d.x;
		d.fy = d.y;
	  }

	  function dragged(d) {
		d.fx = d3.event.x;
		d.fy = d3.event.y;
	  }

	  function dragended(d) {
		if (!d3.event.active) simulation.alphaTarget(0);
		d.fx = null;
		d.fy = null;
	  }

	}

	

	$scope.init = function(){
		frente_escogido = RedirectService.getMessage();
		if(frente_escogido != ""){
			var params;
			params = {
				frente: frente_escogido,
				actividad: ""
			};
			console.log(params);
			DataService.getGrafoActividades(params, onSuccessGrafoActividades, onError);
		}
	};

});