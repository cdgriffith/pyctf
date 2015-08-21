% include('header.tpl', admin="active")
<div class="main-area" ng-controller="adminController">
    <div id="admin_area">
        <div class="title">Admin Area</div>

        <div class="row sep">
            <div class="col-md-2 left-align"><b>Add Account</b></div>
            <form  class="form-inline" ng-submit="addUser()">
            <div class=" col-md-3">
                <div class="form-group">
                    <label class="sr-only" for="newUser">User</label>
                    <input type="user" class="form-control" id="newUser" ng-model="newUser" placeholder="username">
                </div>
            </div>
            <div class=" col-md-3">
                <div class="form-group">
                    <label class="sr-only" for="newPass">Password</label>
                    <input type="password" class="form-control" id="newPass"  ng-model="newPass" placeholder="password">
                </div>
            </div>
            <div class=" col-md-2">
                <div class="form-group">
                    <label for="newAdmin">Admin</label>
                    <input type="checkbox" class="form-control" ng-model="newAdmin" id="newAdmin">
                </div>
            </div>
            <div class="col-md-2 pull-right">
              <button type="submit" style="width:125px" class="btn btn-success">Add User</button>
            </div>
            </form>
        </div>

        <div class="row sep">
            <div class="col-md-2 left-align"><b>Remove Account</b></div>
            <form class="form-inline" ng-submit="removeUser()">
                <div class=" col-md-4">
                    <div class="form-group">
                        <label for="removeAccount">User</label>
                        <select id="removeAccount" ng-model="userToRemove">
                            <option ng-selected="{{'{{user.user == userToRemove}}'}}"
                                    ng-repeat="user in userNames"
                                    value="{{'{{user.user}}'}}">
                              {{'{{user.user}}'}}
                            </option>
                        </select>
                    </div>
                </div>
                <div class="col-md-2 pull-right">
                    <button type="submit" style="width:125px" class="btn btn-danger">Remove User</button>
                </div>
            </form>
        </div>

    </div>

</div>
% include('footer.tpl')




