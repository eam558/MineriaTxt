'use strict';

angular.module('documentosApp').factory('DataService', ['$resource', function ($resource) {

  	var defaultParams = {};
  	var url = 'http://127.0.0.1:5000/';
  	var actions= {
  		getActividades: {method: 'GET', url: url + 'actividades'},
  		getGrafoConocidos: {method: 'GET', url: url + 'grafo_conocidos'},
  		getGrafoActividades: {method: 'GET', url: url + 'frente_actividades'},
  		getMapa: {method: 'GET', url: url + 'mapa'}
  	};

  	return $resource(url, defaultParams, actions);
}]);
