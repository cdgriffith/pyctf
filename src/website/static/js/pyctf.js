/*!
 * PyCTF custom Javascript
 */

function endsWith(str, suffix) {
    return str.indexOf(suffix, str.length - suffix.length) !== -1;
}

var pyctfApp = angular.module('pyctfApp', ['ngCookies', 'ngSanitize']);

pyctfApp.controller('masterController', ['$scope', '$http', '$cookies', '$window', function($scope, $http, $cookies, $window){
    $scope.bound = {auth: $cookies.get('pyctf.auth'),
                    location: "",
                    page_ready: false,
                    logged_in: false};

    $scope.bound.message = function (message){
        alert(message);
    };

    $scope.bound.error = function(message){
        alert(message);
    };

    $scope.logout = function(){
        $cookies.put('pyctf.auth', null);
        $scope.bound.logged_in = false;
        document.location = "/web/login";
    };

    if ($scope.bound.auth == null){
        if (endsWith($window.location.href, "/web/login") == 0) {
            document.location = "/web/login";
        } else {
            $scope.bound.page_ready = true;
        }

    } else {
        $http.post("/user/auth_refresh", {auth_token: $scope.bound.auth})
            .success(function(response){
                $scope.bound.logged_in = true;
                if (endsWith($window.location.href, "/web/login") == 0) {
                    $scope.bound.page_ready = true;
                } else {
                    document.location = "/web/home";
                }
            }).error(function(response){
                $scope.bound.logged_in = false;
                if (endsWith($window.location.href, "/web/login") == 0) {
                    document.location = "/web/login";
                } else {
                    $scope.bound.page_ready = true;
                }
            });
    }

}]);


pyctfApp.controller('questionController', ['$scope', '$http', function($scope, $http){
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
        data: null,
        number: 0
    };

    $scope.selectQuestion = function(question_number){
        $("#question-body").show();
        $("#question-list").hide();
        $http.get("/question/"+ question_number)
            .success(function(response){
                $scope.currentQuestion = angular.copy(response);
                $scope.currentQuestion.number = question_number;

            }).error(function(response){
                alert("Could not load question");
            });
    };

    $scope.backToList = function(){
        $("#question-body").hide();
        $("#question-list").show();
        $scope.answer = "";
        $http.post("/recover_token", {token: $scope.currentQuestion.token}).error(function(){
            console.log("Could not recover token!");
        });
    };

    $scope.answerQuestion = function(){

        var answer;
        if ($scope.currentQuestion.answer_type == "integer"){
            try {
                answer = parseInt($scope.answer);
            } catch(err){
                $scope.bound.error("Could not parse answer to integer");
            }
        } else if ($scope.currentQuestion.answer_type == "string"){
            answer = $scope.answer;
        } else if ($scope.currentQuestion.answer_type == "boolean"){
            if ($scope.answer.toLowerCase() == "true"){
                answer = true;
            } else if ($scope.answer.toLowerCase() == "false"){
                answer = false;
            }
            else {
                $scope.bound.error("Must be either 'true' or 'false'");
            }
        } else if ($scope.currentQuestion.answer_type == "list"){
            answer = $scope.answer.split(",");
        } else if ($scope.currentQuestion.answer_type == "dictionary"){
            try {
                answer = JSON.parse($scope.answer);
            } catch(err){
                $scope.bound.error("Must be a valid JSON string, error: "+ err.message)
            }
        } else {
            answer = $scope.answer;
        }

        var data = {auth_token: $scope.bound.auth,
                    token: $scope.currentQuestion.token,
                    answer: answer};

        $http.post("/answer/"+ $scope.currentQuestion.number, data)
            .success(function(response){
                if (response.correct == true){
                    alert("Congrats, correct answer!");
                    $("#question-body").hide();
                    $("#question-list").show();
                } else {
                    alert("wrong!");
                }
            }).error(function(response){});
    }

}]);



pyctfApp.controller('homeController', ['$scope', '$http', function($scope, $http){

    $scope.welcomeMessage = "<h3> Welcome to PyCTF!</h3>" +
        "<p> This is the default welcome screen, please feel free to customize it!</p>";

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();
        $http.get("/server_info").success(function(response){
            $scope.welcomeMessage = response.welcome_message;
        });
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
        if ($scope.user == null || $scope.password == null){
            alert("Please enter username and password");
            return false;
        }

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

pyctfApp.controller('scoreController', ['$scope', '$http', function($scope, $http){
    $scope.scoreList = [];

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();
            $http.get("/scoreboard/list")
                .success(function (response) {
                    angular.forEach(response.data, function (value, key) {
                        $scope.scoreList.push({score: value[1], name: value[0]});
                    });
                })
                .error(function (response) {
                    alert("Could not load scores!");
                });
        }
    });

}]);



$( document ).ready(function() {

});