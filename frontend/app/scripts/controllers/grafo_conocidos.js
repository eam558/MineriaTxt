'use strict';

angular.module('documentosApp').controller('GrafoConocidosCtrl', function ($scope, $location, DataService) {
	
	$scope.frente_conocidos = "";
	$scope.tipo_individuo_conocidos = "";
	$scope.individuo_conocidos = "";
	$scope.nombre_escogido = "Por favor, ingrese un nombre o un alias";
	$scope.frentes_relacionados = [""];
	$scope.individuo_nodo = "";
	$scope.entrevista_nodo = "";
	$scope.cargo_nodo = "";
	$scope.type_nodo = "";
	$scope.estructura_nodo = "";
	$scope.mostrarTabla = false;
	$scope.mostrarInfo = false;
	var grafoFrente = null;
	var div_grafo = document.getElementById('grafo');

	function fixAlias(word){
		if(word.split(" ")[0] === "alias"){
			return word;
		}
		else{
			return "alias "+word;
		}
	}

	function fixCargo(word){
		if(word === ""){
			return "No aplica";
		}
		else{
			return word;
		}
	}

	function fixTipo(word){
		if(word === "nombre_conocido"){
			return "Nombre referenciado en la entrevista";
		}
		else{
			return "Alias referenciado en la entrevista";
		}
	}

	function fixEstructura(word){
		if(word === ""){
			return "No se menciona en la entrevista";
		}
		else{
			return word;
		}
	}
	function onError(data){
		$scope.nombre_escogido = "No se han encontrado resultados";
		console.log(data);
	}

	$scope.mostrarGrafo = function(x){
		drawGraph(grafoFrente[x]);
	};

	function onSuccessGrafoConocidos(data){ 
		console.log(data);
		if(data["frentes_relacionados"].length === 0){
			$scope.mostrarTabla = false;
			$scope.nombre_escogido = "No se han encontrado resultados";
		}
		else{
			$scope.frentes_relacionados = data["frentes_relacionados"];
			grafoFrente = data["respuesta"];
			$scope.mostrarTabla = true;
		}
	}

	$scope.pintarGrafoConocidos = function(){
		var params;
		var frente_escogido = $scope.frente_conocidos;
		if($scope.tipo_individuo_conocidos === "Nombre" || $scope.tipo_individuo_conocidos === "Alias"){
			if($scope.tipo_individuo_conocidos === "Nombre"){
				$scope.nombre_escogido = "Grafo de frentes relacionados a: " + $scope.individuo_conocidos;
				params = {
					nombre: $scope.individuo_conocidos,
					alias: ""
				};
			}
			else{
				$scope.nombre_escogido = "Grafo de frentes relacionados a: " + fixAlias($scope.individuo_conocidos);
				params = {
					nombre: "",
					alias: fixAlias($scope.individuo_conocidos)
				};
			}
			//console.log(params);
			DataService.getGrafoConocidos(params, onSuccessGrafoConocidos, onError);
		}
		else{
			$scope.nombre_escogido = "Necesita ingresar un nombre o un alias";

			if(div_grafo.firstChild){
			  	$("#grafo").empty();
		    }
		}
	};

	$scope.limpiarConocidos = function(){
		$scope.frente_conocidos = "";
		$scope.tipo_individuo_conocidos = "";
		$scope.individuo_conocidos = "";
		$scope.nombre_escogido = "Por favor, ingrese un nombre o un alias";
		$scope.frentes_relacionados = [""];
		$scope.mostrarTabla = false;
		var grafoFrente = null;
		
		if(div_grafo.firstChild){
		  	$("#grafo").empty();
	    }
	};

	function drawGraph(graph){

	  var width = 860,
		  height = 600,
		  radius = 20

	  if(div_grafo.firstChild){
		  $("#grafo").empty();
	  }

	  var svg = d3.select("#grafo").append("svg")
			.attr("width", width)
			.attr("height", height)
	

	  var color = d3.scaleOrdinal(d3.schemeCategory10);;

	  //.force("collide",d3.forceCollide( function(d){return d.r + 5 }).iterations(16) )

	  var simulation = d3.forceSimulation()
	    .force("link", d3.forceLink().id(function(d) { return d.id; }).distance(30))
	    .force("collide",d3.forceCollide( function(d){return d.r + 4 }))
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
		  .attr("stroke-width", function(d) { return 2; });

	

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
		  .attr("r", function(d){ if(d.tipo_nodo === 'frente'){ return 30; } else { if(d.cargo==='CABECILLA'){ return 15;} else {return 5; } }})
		  .style("fill", function(d){ if(d.tipo_nodo ==='frente'){ return "green";} else if(d.tipo_nodo === 'nombre_conocido'){ return "blue";} else {return "red";}});

	  node.on("click", function(d){ console.log(d), $scope.individuo_nodo = d.nombre, $scope.entrevista_nodo = d.nombre_archivo, $scope.cargo_nodo = fixCargo(d.cargo), $scope.type_nodo = fixTipo(d.tipo_nodo), $scope.estructura_nodo = fixEstructura(d.estructura), $scope.mostrarInfo = true, $scope.$applyAsync(); })
		  .call(d3.drag()
			  .on("start", dragstarted)
			  .on("drag", dragged)
			  .on("end", dragended));

	  node.append("title")
		  .attr("dx", 12)
		  .attr("dy", ".35em")
		  .text(function(d) { if(d.cargo != ""){ return d.nombre + " (" + d.cargo + ")"; } else { return d.nombre; } });

	  simulation.on("tick", function() {
	  	node.attr("cx", function(d) { return d.x = Math.max(radius, Math.min(width - radius, d.x)); })
        	.attr("cy", function(d) { return d.y = Math.max(radius, Math.min(height - radius, d.y)); });

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

	};

});