% include('header.tpl')
<div class="main-area" ng-controller="userController">
    <div id="user_area">

        <div class="row">
            <div class="col-md-4"></div>
            <div class="col-md-4">
                <h3>Change password</h3>
                <form  ng-submit="changePassword()">
                    <div class="form-group">
                        <label class="sr-only" for="currentPass">Current Password</label>
                        <input type="user" class="form-control" id="currentPass" ng-model="currentPass" placeholder="Current Password">
                    </div>

                    <div class="form-group">
                        <label class="sr-only" for="newPass">New Password</label>
                        <input type="password" class="form-control" id="newPass"  ng-model="newPass" placeholder="New Password">
                    </div>

                    <div class="form-group">
                        <label class="sr-only" for="confirmNewPass">Confirm New Password</label>
                        <input type="password" class="form-control" id="confirmNewPass"  ng-model="confirmNewPass" placeholder="Confirm Password">
                    </div>
                  <button type="submit" class="btn btn-success">Update Password</button>
                </form>
            </div>
            <div class="col-md-4"></div>
        </div>

    </div>

</div>
% include('footer.tpl')




