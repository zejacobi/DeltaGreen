dgApp.controller('landing', ['$scope', '$timeout', function($scope, $timeout) {
    var title = 'Delta Green Character Generator';
    $scope.title = title;

    var glitches = [
        "D̴e̸l̵t̶a̷ ̶G̸r̷e̵e̸n̷ ̸C̴h̶a̷r̸a̷c̶t̶e̴r̴ ̵G̸e̸n̶e̶r̸a̴t̴o̶r̶",
        "D__ta Gre_n Ch_RACTER gEn__ator",
        "��� ��� ����� ������",
        "Delta Green Character Crematory",
        "███ ███ █████ ██████",
        "Delta Green Character Generato",
        "Delta Green Character Generat",
        "Delta Green Character Genera",
        "Delta Green Character Gener",
        "Delta Green Character Gene",
        "Delta Green Character Gen",
        "Delta Green Character Ge",
        "Delta Green Character G",
        "Delta Green Character ",
        "Delta Green Character",
        "Delta Green Characte",
        "Delta Green Charact",
        "Delta Green Charac",
        "Delta Green Chara",
        "Delta Green Char",
        "Delta Green Cha",
        "Delta Green Ch",
        "Delta Green C",
        "Delta Green ",
        "Delta Green",
        "Delta Gree",
        "Delta Gre",
        "Delta Gr",
        "Delta G",
        "Delta ",
        "Delta",
        "Delt",
        "Del",
        "De",
        "D",
        "",
        "",
        "",
        "",
        "HARK",
        "HE RISES IN HIS GLORY",
        "PRAISE AND WORSHIP HIS INFINITE MAJESTY",
        "",
        "",
        "",
        "",
        "...",
        "save me...",
        "THIS WAS ALL A DREAM",
        "YOU MUST BELIEVE IT WAS ALL A DREAM",
        "OR YOU WILL BE FOREVER LOST"
    ];

    function glitch(id) {
        $timeout(function goCrazy() {
            if (id >= glitches.length) {
                id = id % (glitches.length - 1)
            }
            $scope.title = glitches[id];
            $timeout(function restore() {
                $scope.title = title;
                glitch(id + 1)
            }, 490)
        }, 13000)
    }

    glitch(0);
}]);