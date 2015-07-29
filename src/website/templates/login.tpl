<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{get('title', "PyCTF")}}</title>
    <link rel="stylesheet" href="/static/css/bootstrap.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.css">
    <link rel="stylesheet" href="/static/css/pyctf.css">
</head>
    <!---<body style="background: linear-gradient(#2A7890, #2D3246)">-->
    <body style="background: #434545">

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
          </div>
        </nav>

            <div class="col-md-4"></div>

            <div class="col-md-4" style="min-height: 100%; min-height: 100vh; align-items: center; display: flex;">

                <div class="login-box">
                    <form>
                        <div class="form-group">
                            <label class="white-text" for="login_user">Username </label>
                            <input id="login_user" class="form-control" type="text" name="user" placeholder="Username" />
                        </div>
                        <div class="form-group">
                            <label class="white-text" for="login_password">Password </label>
                            <input id="login_password" class="form-control" type="password" name="password" placeholder="Password" />
                        </div>
                            <button id="login_button" type="button" name="login" value="Login" class="btn btn-default" >Log in</button>
                    </form>
                </div>
            </div>

            <div class="col-md-4"></div>

% include('footer.tpl')