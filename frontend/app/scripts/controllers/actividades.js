'use strict';

angular.module('documentosApp').controller('ActividadesCtrl', function ($scope, $location, DataService, RedirectService) {
	
	$scope.mostrarBoton = false;

	function onError(data){
		console.log(data);
	}

	function onSuccessActividades(data){ 
		//console.log(data);
		drawCircles(data);
	}

	$scope.redirect = function(){
		$location.path('/grafo_actividades');
	};

	function drawCircles(root){

	  var svg = d3.select("svg"),
	    margin = 20,
	    diameter = +svg.attr("width"),
	    g = svg.append("g").attr("transform", "translate(" + diameter / 2 + "," + diameter / 2 + ")");



	  var pack = d3.pack()
	    .size([diameter - margin, diameter - margin])
	    .padding(2);


	  root = d3.hierarchy(root)
	      .sum(function(d) { return d.size; })
	      .sort(function(a, b) { return b.value - a.value; });

	  var focus = root,
	      nodes = pack(root).descendants(),
	      view;

	  var circle = g.selectAll("circle")
	    .data(nodes)
	    .enter().append("circle")
	      .attr("class", function(d) { return d.parent ? d.children ? "node" : "node node--leaf" : "node node--root"; })
	      .style("fill", function(d) { return "  green "; })
	      .style("stroke", function(d) { return " green "; })	      
	       .style("stroke-width", function(d) { return "0.3"; })	     
	      .on("click", function(d) { if (focus !== d) zoom(d), $scope.mostrarBoton = true, console.log($scope.mostrarBoton), d3.event.stopPropagation(); });

	  var text = g.selectAll("text")
	    .data(nodes)
	    .enter().append("text")
	      .attr("class", "label")
	      .style("font-size", function(d) { return "15px"; })
	     .style("stroke", function(d) { return " green "; })
	       //.style("fill", function(d) { return "white"; })  	      
	      .style("font-family", function(d) { return "Impact"; })
	      .style("fill-opacity", function(d) { return d.parent === root ? 1 : 0; })
	      .style("display", function(d) { return d.parent === root ? "inline" : "none"; })
	      .text(function(d) { return d.data.name; });

	  var node = g.selectAll("circle,text");

	  svg
	      .style("background", "white")
	      .on("click", function() { zoom(root), $scope.mostrarBoton = false, $scope.$applyAsync();});

	  zoomTo([root.x, root.y, root.r * 2 + margin]);

	  function zoom(d) {
	  	
	    var focus0 = focus; focus = d;

	    var transition = d3.transition()
	        .duration(d3.event.altKey ? 7500 : 750)
	        .tween("zoom", function(d) {
	          var i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2 + margin]);
	          return function(t) { zoomTo(i(t)); };
	        });

	    transition.selectAll("text")
	      .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
	        .style("fill-opacity", function(d) { return d.parent === focus ? 1 : 0; })
	        .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
	        .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });

	    RedirectService.setMessage(d.data.name);
	    $scope.mostrarBoton = true;
	    $scope.$applyAsync();
	  }

	  function zoomTo(v) {
	    var k = diameter / v[2]; view = v;
	    node.attr("transform", function(d) { return "translate(" + (d.x - v[0]) * k + "," + (d.y - v[1]) * k + ")"; });
	    circle.attr("r", function(d) { return d.r * k; });
	  }


	}


	$scope.init = function(){

		DataService.getActividades({}, onSuccessActividades, onError);
	};

});