% include('header.tpl', home='active')

        <div class="main-area" ng-controller="homeController">

            <div ng-bind-html="welcomeMessage">
            </div>

        </div>

% include('footer.tpl')