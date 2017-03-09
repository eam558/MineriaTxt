'use strict';

angular.module('documentosApp').controller('MapaCtrl', function ($scope, $location, DataService) {
	
	var map = null;
	var heatlayer = null;
	//$scope.actividades = ["Kilos narcotráfico", "Valores narcotráfico", "Hectáreas fincas con título","Cantidad fincas con título","Hectáreas fincas sin título","Cantidad fincas sin título","Ganadería"]
	$scope.actividades = ['campamento', 'matar', 'retén', 'trinchera', 'alcalde', 'explosivos', 'dolar', 'inversión', 'chuzo', 'fierro', 'tienda', 'café', 'aporte', 'remesa', 'resguardo', 'desaparición', 'extorsión', 'boleteo', 'carbón', 'recolección', 'mortero', 'tatuco', 'mensual', 'robo', 'maíz', 'disparo', 'cruel', 'sueldo', 'deuda', 'cultivo', 'descuartizar', 'dinero', 'parcela', 'millón', 'tráficante', 'ecuador', 'droga', 'arma blanca', 'balacera', 'abuso', 'gatillo', 'torturar', 'fondos', 'incursión', 'tierra', 'puñal', 'bomba', 'concejo de guerra', 'marcha', 'clorhidrato', 'caza', 'maracachafa', 'porcentaje', 'navaja', 'caleta', 'cambuche', 'dotación', 'virgen', 'finca', 'animal', 'granada', 'cañón', 'corregimiento', 'oxidada', 'oleoducto', 'procesamiento', 'secuestro', 'presidente', 'minado', 'casa', 'acoso', 'lucro', 'maltrato', 'vacuna', 'policía', 'revólver', 'fuente', 'venezuela', 'empresa', 'pepas', 'fanegada', 'proveedores', 'cirugía', 'toma', 'pancoger', 'económico', 'cuartel', 'violación', 'machete', 'euro', 'antipersona', 'plata', 'cristal', 'peso', 'shotgun', 'cuchillo', 'coca', 'pisada', 'soborno', 'tráfico', 'aniquilar', 'ataque', 'remuneración', 'galil', 'entierro', 'política', 'sexo', 'monto', 'enterrar', 'coltan', 'combate', 'kilo', 'retención', 'laboratorio', 'metal', 'dar de baja', 'ganadería', 'paga', 'asesinar', 'oro', 'hectárea', 'ajusticia', 'marihuana', 'petardo', 'tiro', 'explosivo', 'vehículos', 'fusil', 'gobernador', 'desmembrar', 'fosa', 'municiones', 'mujer', 'bala', 'emboscada', 'raspachín', 'menor de edad', 'ong', 'minería', 'ejecutar', 'bazuca', 'narcotráfico', 'amapola', 'desaparecido', 'bisturí', 'negocio', 'tumba', 'ak-47', 'hostigar', 'mina quiebrapatas', 'organismo', 'armamento', 'milicias', 'refugio', 'venta', 'cartucho', 'frontera', 'prisionero', 'pistola', 'negociación', 'químico', 'rapto'];
	$scope.nombre_delito = '';
	var actividades_escogidas = [];
	var indice = 0;
	var points = [];
	var datos_heatmap = [];

	function onError(data){
		console.log(data);
	}

	function onSuccessMapa(data){ 
		console.log(data);
	

		if ($scope.tipo==="Marcadores"){
			drawMap2(data);
		} else {
			drawMap(data);
		}
	}

	$scope.darMapaCalor =function(x){
		//console.log(x);
		$scope.nombre_delito=x;
		if(actividades_escogidas.indexOf(x) === -1){
			actividades_escogidas.push(x);
			actividades_escogidas = actividades_escogidas.filter(function( element ) {
			   return element !== undefined;
			});
			var params;
			params = {
				actividad: x
			};
			DataService.getMapa(params, onSuccessMapa, onError);
		}
	};

	function drawMap2(data){
	  console.log(actividades_escogidas);
	  var color = d3.scaleOrdinal(d3.schemeCategory20)
  		  	.domain(actividades_escogidas);
  	  var paleta_colores = color.range();
	  d3.select(".svg_legend").remove();
		//map.remove()
		//map = L.map('map').setView([4.6097, -74.0817], 6);
		//map.setZoom(7);

	  // load a tile layer
	  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
	    {
	      attribution: 'OpenStreetMap',
	      maxZoom: 18,
	      minZoom: 5
	    }).addTo(map);
	  for (var i = 0; i < data["coordenadas"].length; i++){
	  	var coord=data["coordenadas"][i];
	  	var marker = L.circle(coord,{color: paleta_colores[indice]}).addTo(map);
	 	}
	  var svg = d3.select("#legend")
	  		.append("svg")
	  		.attr("class", "svg_legend")
	  		.attr("width", 125)
	  		.attr("height", 600);

	  var legend = svg.append("g")
	  				.attr("class", "legend1")
	  				.attr("transform", function(d, i){return 'translate(0,' + (i*30) + ')';});

	  legend.selectAll("rect")
	  		.data(color.domain())
	  		.enter()
	  		.append("rect")
	  		.attr("x", 10)
	  		.attr("y", function(d, i){ return (i-1)*20+32; })
	  		.attr("width", 12)
	  		.attr("height", 12)
	  		.style("fill", color);

	  legend.selectAll("text")
	  		.data(color.domain())
	  		.enter()
	  		.append("text")
	  		.attr("x", 75)
	  		.attr("y", function(d, i){ return (i-1)*20+40; })
	  		.text(function(d){ return d; });

	  indice += 1;

	  /*
	  for (var i = 0 ; i < vector.length ; i++){
		heatlayer.addLatLng(vector[i]);
	  }
	  */
	  
		}

	function drawMap(data){
		if(heatlayer){
			map.removeLayer(heatlayer);
		}
		datos_heatmap = datos_heatmap.concat(data["coordenadas"]);
		//map = L.map('map').setView([4.6097, -74.0817], 6);

	  // load a tile layer
	  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
	    {
	      attribution: 'OpenStreetMap',
	      maxZoom: 18,
	      minZoom: 5
	    }).addTo(map);


	   heatlayer = L.heatLayer(datos_heatmap, {
				minOpacity: 0.8,
				maxzoom: 18,
				max: 1.0,
				radius: 10,

			}).addTo(map);


	  /*
	  for (var i = 0 ; i < vector.length ; i++){
		heatlayer.addLatLng(vector[i]);
	  }
	  */
	  
		}

	function getRandomColor() {
	    var letters = '0123456789ABCDEF';
	    var color = '#';
	    for (var i = 0; i < 6; i++ ) {
	        color += letters[Math.floor(Math.random() * 16)];
	    }
	    return color;
	}

	function cambiarTipo(){

	}

	$scope.limpiarTodo =function(x){
		map.remove();
		map = L.map('map').setView([4.6097, -74.0817], 9);
		//map.setZoom(1);
		  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
		    {
		      attribution: 'OpenStreetMap',
		      maxZoom: 18,
		      minZoom: 5
		    }).addTo(map);
		d3.select(".svg_legend").remove();
		$scope.nombre_delito = '';
		actividades_escogidas = [];
		datos_heatmap = [];
		indice = 0;
	};

	$scope.init = function(){
	  console.log(actividades_escogidas);
		// initialize the map
	  map = L.map('map').setView([4.6097, -74.0817], 9);
	  map.setZoom(1);
	//var marker = L.marker([4.6097, -74.0817]).addTo(map);
	  // load a tile layer
	  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png',
	    {
	      attribution: 'OpenStreetMap',
	      maxZoom: 18,
	      minZoom: 5
	    }).addTo(map);
	 
	};

});