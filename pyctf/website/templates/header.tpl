<!DOCTYPE html>
<html lang="en" ng-app="pyctfApp">
<head>
    <meta charset="UTF-8">
    <title>{{get('title', "PyCTF")}}</title>
    <link rel="stylesheet" href="/static/css/bootstrap.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.css">
    <link rel="stylesheet" href="/static/css/pyctf.css">
</head>
    <body ng-controller="masterController">

        <nav class="navbar navbar-inverse navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">PyCTF</a>
            </div>
            <div id="navbar" class="collapse navbar-collapse" style="width: 100%">
              <ul id="navbar-items" class="nav navbar-nav">
                <li class="{{get('home', '')}}"><a href="/web/home">Home</a></li>
                <li class="{{get('questions', '')}}"><a href="/web/questions">Questions</a></li>
                <li class="{{get('scoreboard', '')}}"><a href="/web/scoreboard">Scoreboard</a></li>
              </ul>


              <div ng-hide="! bound.logged_in || ! bound.page_ready" class="col-md-2 pull-right">
                 <div class="dropdown">
                      <button class="btn btn-primary dropdown-toggle" type="button" data-toggle="dropdown">
                      <span class="glyphicon glyphicon-user" style="color: white">
                      {{'{{bound.user}}'}}
                      <span class="caret"></span></button>
                      <ul class="dropdown-menu">
                        <li><a href="/web/user">Change Password</a></li>
                        <li ng-hide="bound.roles.indexOf('admin') == -1" class="{{get('admin', '')}}" ><a href="/web/admin">Admin Controls</a></li>
                        <li class="divider"></li>
                        <li><a ng-click="logout()" href="#">Logout</a></li>
                      </ul>
                 </div>




              </div>


            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container" style="padding-top: 40px">