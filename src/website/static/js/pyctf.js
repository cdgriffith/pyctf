/*!
 * PyCTF custom Javascript
 */

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

var pyctfApp = angular.module('pyctfApp', ['ngCookies']);

pyctfApp.controller('masterController', ['$scope', '$http', '$cookies', '$window', '$location', function($scope, $http, $cookies, $window, $location){
    $scope.bound = {auth: $cookies.get('pyctf.auth'),
                    location: "",
                    page_ready: false};

    //console.log($window.location.href);

    if ($scope.bound.auth == null){
        if (endsWith($window.location.href, "/web/login") == 0) {
            document.location = "/web/login";
        } else {
            $scope.bound.page_ready = true;
        }

    } else {
        $http.post("/user/auth_refresh", {auth_token: $scope.bound.auth})
            .success(function(response){
                if (endsWith($window.location.href, "/web/login") == 0) {
                    $scope.bound.page_ready = true;
                } else {
                    document.location = "/web/home";
                }
            }).error(function(response){
                if (endsWith($window.location.href, "/web/login") == 0) {
                    document.location = "/web/login";
                } else {
                    $scope.bound.page_ready = true;
                }
            });
    }

}]);


pyctfApp.controller('questionController', ['$scope', '$http', '$location', function($scope, $http, $location){
    $scope.questionList = [];

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();
            $http.get("/questions/list")
                .success(function (response) {
                    angular.forEach(response.data, function (value, key) {
                        $scope.questionList.push({number: value[0], title: value[1], tags: value[2]});
                    });
                })
                .error(function (response) {
                    alert("Could not load questions!");
                });
        }
    });


    $scope.currentQuestion = {
        answer_type: "",
        token: "",
        title: "",
        question: "",
        time_limit: 0,
        media: null,
        data: null
    };

    $scope.selectQuestion = function(question_number){
        $("#question-body").show();
        $("#question-list").hide();
        $http.get("/question/"+ question_number)
            .success(function(response){
                $scope.currentQuestion = angular.copy(response);

            }).error(function(response){
                alert("Could not load question");
            });

    };

}]);



pyctfApp.controller('homeController', ['$scope', '$http', function($scope, $http){

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();
        }
    });

}]);


pyctfApp.controller('loginController', ['$scope', '$http', '$cookies', function($scope, $http, $cookies){
    $scope.bound.location = "login";

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();
        }
    });

    $scope.login = function(){
         $http.post('/login', {user: $scope.user, password: $scope.password})
             .success(function(response){
                 $scope.bound.auth = response.auth_token;
                 $scope.bound.auth_timeout = response.timeout;
                 $cookies.put("pyctf.auth", response.auth_token);
                 document.location = "/web/home";
             }).error(function(response){
                alert("Invalid Credentials");
             });
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