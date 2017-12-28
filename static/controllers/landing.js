dgApp.controller('landing', ['$scope', '$window', function($scope, $window) {
    $scope.loadDialogue = false;
    $scope.error = null;
    $scope.input = {
        id: null
    }; // we're using ng-if, so we need ng-model to go to objects

    $scope.goToCharacter = function goToCharacter() {
        if ($scope.input.id && $scope.input.id.length === 24) {
            $window.location.pathname = '/character/' + $scope.input.id
        } else {
            $scope.error = true;
        }
    };

    $scope.openModal = function openModal() {
        $scope.input.id = null;
        $scope.error = null;
        $scope.loadDialogue = true;
    };

    $scope.closeModal = function openModal() {
        $scope.error = null;
        $scope.loadDialogue = false;
    };
}]);