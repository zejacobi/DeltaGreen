dgApp.controller('character', ['$scope', '$http', function($scope, $http) {
    $http.get('/api/v1/characters').then(function attachToScope(res) {
        $scope.character = res.data.Character;
        console.log(res.data.Character);
    });
}]);