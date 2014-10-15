var myApp = angular.module('myApp', ['datatables']);

myApp.controller('MyController', ['$scope', '$http', function($scope, $http) {
  $http.get('js/data.json').success(function(data) {
    $scope.artists = data;
  });
}]);

