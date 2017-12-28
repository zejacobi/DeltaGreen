dgApp.controller('character', ['$scope', '$http', '$window', function($scope, $http, $window) {
    $scope.loadDialogue = false;
    $scope.saveDialogue = false;
    $scope.alreadySaved = false;
    $scope.baseURL = $window.location.href;
    if ($scope.baseURL.slice(-1) !== '/') {
        $scope.baseURL += '/';
    }

    var path = $window.location.pathname;
    var charPathStr = '/character/';

    function getNewCharacter() {
        $scope.alreadySaved = false;
        return $http.get('/api/v1/characters')
    }

    if (path.indexOf(charPathStr) >= 0 && path[charPathStr.length]) {
        // the length thing is a trick to avoid triggering on /character/
        $scope.alreadySaved = true;
        console.log("I would load an existing character")
    } else {
        getNewCharacter().then(function attachToScope(res) {
            $scope.character = res.data.Character;
        });
    }

    $scope.save = function save() {
        $scope.saveDialogue = true;
        if ($scope.alreadySaved) {
            $scope.error = null;
        } else if ($scope.character) {
            $http.post('api/v1/characters', $scope.character).then(function(res) {
                $scope.alreadySaved = true;
                $scope.id = res.data.ID;
            }).catch(function(err) {
                $scope.id = null;
                if (err && err.data && err.data.Error) {
                    $scope.error = err.data.Error;
                } else {
                    $scope.error = 'Something went wrong saving character'
                }
            });
        } else {
            $scope.error = 'Please wait until the character has loaded to save it';
        }
    };

    $scope.closeModal = function closeModal() {
        $scope.loadDialogue = false;
        $scope.saveDialogue = false;
        $scope.error = null;
    };
}]);