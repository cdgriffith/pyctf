/*!
 * PyCTF custom Javascript
 */

var pyctfApp = angular.module('pycftApp', []);

pyctfApp.controller('masterController', ['$scope', function($scope){
    $scope.bound = { test: 'stuff'
    };


}]);


pyctfApp.controller('questionController', ['$scope', function($scope){
    $scope.questionList = ['1', '2'];


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