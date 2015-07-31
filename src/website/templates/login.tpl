% include('header.tpl')
<div ng-controller="loginController">
            <div class="col-md-4"></div>

            <div class="col-md-4" style="min-height: 100%; min-height: 100vh; align-items: center; display: flex;">

                <div class="login-box">
                    <form ng-submit="login()">
                        <div class="form-group">
                            <label class="white-text" for="login-user">Username </label>
                            <input ng-model="user" id="login-user" class="form-control" type="text" name="user" placeholder="Username" />
                        </div>
                        <div class="form-group">
                            <label class="white-text" for="login-password">Password </label>
                            <input ng-model="password" id="login-password" class="form-control" type="password" name="password" placeholder="Password" />
                        </div>
                            <input type="submit" id="login-button" type="button" name="login" value="Login" class="btn btn-default">Log in</input>
                    </form>
                </div>
            </div>

            <div class="col-md-4"></div>
</div>
% include('footer.tpl')