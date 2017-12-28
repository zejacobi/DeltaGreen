dgApp.controller('character', ['$scope', '$http', '$window', '$timeout', function($scope, $http, $window, $timeout) {
    $scope.loadDialogue = false;
    $scope.saveDialogue = false;
    $scope.alreadySaved = false;
    $scope.loadError = null;
    $scope.input = {
        id: null
    }; // we're using ng-if, so we need ng-model to go to objects

    var baseURL = $window.location.href;
    if (baseURL.slice(-1) !== '/') {
        baseURL += '/';
    }

    var path = $window.location.pathname;
    var charPathStr = '/character/';

    function getNewCharacter() {
        $scope.alreadySaved = false;
        return $http.get('/api/v1/characters')
    }

    function loadCharacter(id) {
        return $http.get('/api/v1/characters/' + id)
    }

    if (path.indexOf(charPathStr) >= 0 && path[charPathStr.length]) {
        // the length thing is a trick to avoid triggering on /character/
        var id = null;
        if (baseURL.slice(-1) === '/') {
            $scope.url = baseURL.slice(0, -1);
        } else {
            $scope.url = baseURL;
        }
        var urlBits = path.split('/');
        for (var i = urlBits.length - 1; i >= 0; i--) {
            if (urlBits[i] && urlBits[i].length === 24) {
                id = urlBits[i]
            }
        }
        if (id) {
            loadCharacter(id).then(function afterLoad(res) {
                $scope.character = res.data.Character;
                $scope.id = id;
                $scope.alreadySaved = true;
            }).catch(function withErr(err) {
                if (err && err.data && err.data.Error) {
                    $scope.loadError = err.data.Error;
                } else {
                    $scope.loadError = 'Something went wrong loading character'
                }
            });
        } else {
            $scope.loadError = 'Missing or invalid character ID'
        }
    } else {
        getNewCharacter().then(function attachToScope(res) {
            $scope.character = res.data.Character;
        });
    }

    $scope.newCharacter = function newCharacter() {
        $scope.alreadySaved = false;
        getNewCharacter().then(function attachToScope(res) {
            $scope.character = res.data.Character;
        });
    };

    $scope.loadModalOpen = function loadModalOpen() {
        $scope.error = null;
        $scope.loadDialogue = true;
        $scope.saveDialogue = false;
    };

    $scope.loadCharacter = function loadCharacterScope() {
        if ($scope.input.id && $scope.input.id.length === 24) {
            loadCharacter($scope.input.id).then(function afterLoad(res) {
                $scope.character = res.data.Character;
                $scope.id = $scope.input.id;
                $scope.alreadySaved = true;
                $timeout($scope.closeModal, 1000)
            }).catch(function withErr(err) {
                if (err && err.data && err.data.Error) {
                    $scope.error = err.data.Error;
                } else {
                    $scope.error = 'Something went wrong loading character'
                }
            });
        } else {
            $scope.error = "Invalid ID"
        }
    };

    $scope.save = function save() {
        $scope.saveDialogue = true;
        if ($scope.alreadySaved) {
            $scope.error = null;
        } else if ($scope.character) {
            $http.post('/api/v1/characters', $scope.character).then(function(res) {
                $scope.alreadySaved = true;
                $scope.id = res.data.ID;
                $scope.url = baseURL + res.data.ID;
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
        $scope.loadError = null;
        $scope.input.id = null;
    };
}]);