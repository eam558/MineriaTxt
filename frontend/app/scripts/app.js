'use strict';

/**
 * @ngdoc overview
 * @name documentosApp
 * @description
 * # documentosApp
 *
 * Main module of the application.
 */
angular.module('documentosApp', [
    'ngAnimate',
    'ngCookies',
    'ngResource',
    'ngRoute',
    'ngSanitize',
    'ngTouch',
    'ui.bootstrap',
    'ngOboe',
    'rzModule'
  ])
  .config(function ($routeProvider) {
    $routeProvider
      .when('/', {
        redirectTo: '/main'
      })
      .when('/main', {
        templateUrl: 'views/main.html',
        controller: 'MainCtrl',
        controllerAs: 'main'
      })
      .when('/grafo_conocidos', {
        templateUrl: 'views/grafo_conocidos.html',
        controller: 'GrafoConocidosCtrl',
        controllerAs: 'grafo_conocidos'
      })
      .when('/actividades', {
        templateUrl: 'views/actividades.html',
        controller: 'ActividadesCtrl',
        controllerAs: 'actividades'
      })
      .when('/grafo_actividades', {
        templateUrl: 'views/grafo_actividades.html',
        controller: 'GrafoActividadesCtrl',
        controllerAs: 'grafo_actividades'
      })
      .when('/mapa', {
        templateUrl: 'views/mapa.html',
        controller: 'MapaCtrl',
        controllerAs: 'mapa'
      })
      .otherwise({
        redirectTo: '/main'
      });
  });
