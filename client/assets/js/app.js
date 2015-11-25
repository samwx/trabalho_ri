angular.module('tagboardApp', ['ngRoute', 'tagboardApp.controllers'])

.config(function( $routeProvider ){
  $routeProvider
    //route for the homepage
    .when('/', {
      templateUrl: 'home.html',
      controller: 'mainController'
    })

    //route for results page
    .when('/results/:hashtag/:resultsCount', {
      templateUrl: 'results.html',
      controller: 'resultsController'
    });
});
