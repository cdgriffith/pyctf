/*!
 * PyCTF custom Javascript
 */

var pyctfApp = angular.module('pyctfApp', []);

pyctfApp.controller('masterController', ['$scope', function($scope){
    $scope.bound = { test: 'stuff'
    };


}]);


pyctfApp.controller('questionController', ['$scope', '$http', function($scope, $http){
    $scope.questionList = [];
    $http.get("/questions/list")
        .success(function(response){
            angular.forEach(response.data, function(value, key){
                $scope.questionList.push({number: value[0], title: value[1], tags: value[2]});
            });
        })
        .error(function(response){
            alert("Could not load questions!");
        });

    $scope.selectQuestion = function(question_number){


    };

}]);


$( document ).ready(function() {
  /*  $('#navbar-items li').click(function(e) {
      var $this = $(this);
      $this.siblings().removeClass('active');
      if (!$this.hasClass('active')) {
        $this.addClass('active');
      }
    }); */
});