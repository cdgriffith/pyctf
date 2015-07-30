% include('header.tpl', home='active')

    <div class="main-area" ng-controller="homeController">

        <div id="message_area">
            <div id="message"></div>
            <div id="error"></div>
            <div id="success"></div>
        </div>
        <div id="content">
            <div class="col-md-8">


                <div id="home_body">
                    <h1>Home</h1>
                    <div id="welcome_message"> </div>
                </div>

            </div>

            <div class="col-md-4">
                <div id="userinfo" style="display:none">
                    <div id="username"></div><div id="logout"><button id="logout_button">Logout</button></div>
                    <div id="user_message"></div>
                    <div id="user_score_area">Score: <span id="user_score">0</span></div>

                   <!--- <button id="admin_button">Admin Area</button> --->
                </div>
            </div>
        </div>

</div>

% include('footer.tpl')