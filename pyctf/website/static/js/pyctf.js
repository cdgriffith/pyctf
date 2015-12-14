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
                    logged_in: false,
                    user: "",
                    roles: []};


    $scope.bound.message = function (message){
        alert(message);
    };

    $scope.bound.error = function(message){
        alert(message);
    };

    $scope.logout = function(){
        $cookies.put('pyctf.auth', null);
        $scope.bound.logged_in = false;
        $scope.bound.user = "";
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
                $scope.bound.user = response.user;
                $scope.bound.roles = response.roles;
                if (endsWith($window.location.href, "/web/login") == 0) {
                    $scope.bound.page_ready = true;
                } else {
                    document.location = "/web/home";
                }
            }).error(function(response){
                $scope.bound.logged_in = false;
                $scope.bound.user = "";
                $scope.bound.roles = [];
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
                        $scope.questionList.push({number: value[0],
                                                  title: value[1],
                                                  points: value[2],
                                                  tags: value[3]});
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
        $("#question-list").hide();
        $http.get("/question/"+ question_number)
            .success(function(response){
                $scope.currentQuestion = angular.copy(response);
                $scope.currentQuestion.number = question_number;
                $("#question-body").show();
            }).error(function(response){
                alert("Could not load question");
                $scope.backToList();
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

    $scope.questionListOrder = 'score';
    $scope.questionListOrderReverse = false;

    $scope.updateSort = function(field){
        if ($scope.questionListOrder == field) {
            $scope.questionListOrderReverse = ! $scope.questionListOrderReverse;
        } else {
            $scope.questionListOrderReverse = false;
            $scope.questionListOrder = field;
        };
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
                    $scope.answer = "";
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
                 $scope.bound.user = $scope.user;
                 $scope.bound.roles = response.roles;
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

        $scope.scoreboardListOrder = 'number';
    $scope.scoreboardListOrderReverse = false;

    $scope.updateSort = function(field){
        if ($scope.scoreboardListOrder == field) {
            $scope.scoreboardListOrderReverse = ! $scope.scoreboardListOrderReverse;
        } else {
            $scope.questionListOrderReverse = false;
            $scope.scoreboardListOrder = field;
        };
    };


}]);


pyctfApp.controller('adminController', ['$scope', '$http', function($scope, $http){

    $scope.userNames = [];
    $scope.questionList = [];

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();

            if ($scope.bound.roles.indexOf('admin') == -1){
                   document.location = "/web/home";
            } else {
                $http.post("/user/list", {auth_token: $scope.bound.auth})
                    .success(function(response){
                         angular.forEach(response.data, function (value) {
                             $scope.userNames.push({user: value[0], admin: value[1]});
                         });
                    });
            $http.get("/questions/list")
                .success(function (response) {
                    angular.forEach(response.data, function (value, key) {
                        $scope.questionList.push({number: value[0],
                                                  title: value[1],
                                                  points: value[2],
                                                  tags: value[3]});
                    });
                })
                .error(function (response) {
                    alert("Could not load questions!");
                });
            }

        }
    });

    $scope.addUser = function(){
        if ($scope.newUser == null || $scope.newPass == null){
            alert("Please enter username and password");
            return false;
        }

        var data = {user: $scope.newUser,
                    password: $scope.newPass,
                    auth_token: $scope.bound.auth,
                    admin: $scope.newAdmin};

            $http.post('/user/add', data)
             .success(function(response){
                 alert("User added");
             }).error(function(response){
                alert("Invalid Credentials");
             });
    };

    $scope.removeUser = function(){
        if(! $scope.userToRemove){
            alert("Must select a user!");
            return false;
        }

        var data = {user: $scope.userToRemove,
                    auth_token: $scope.bound.auth};

            $http.post('/user/remove', data)
             .success(function(response){
                 alert("User deleted");
             }).error(function(response){
                alert(response.error);
             });
    };

    $scope.removeQuestion = function(){
        if(! $scope.questionToRemove){
            alert("Must select a question!");
            return false;
        }

        var data = {question_number: $scope.questionToRemove,
                    auth_token: $scope.bound.auth};

            $http.post('/question/delete', data)
             .success(function(response){
                 alert("Question deleted");
             }).error(function(response){
                alert(response.error);
             });
    };




}]);


pyctfApp.controller('userController', ['$scope', '$http', function($scope, $http){

    $scope.$watch('bound.page_ready', function(value) {
        if (value == true) {
            $(".main-area").show();
            }
        });

    $scope.changePassword = function(){
        if ($scope.newPass != $scope.confirmNewPass){
            alert("Passwords do not match");
            return false;
        }

        var data = {
        "password": $scope.newPass,
        "old_password": $scope.currentPass,
        "auth_token": $scope.bound.auth
        }

        $http.post("/user/change_password", data)
            .success(function(response){
                alert("Password updated");
            })
            .error(function(response){
                alert(response.error);
            });
    }
}]);