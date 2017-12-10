var dgApp = angular.module('dgApp', []);

dgApp.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{!');
    $interpolateProvider.endSymbol('!}');
});