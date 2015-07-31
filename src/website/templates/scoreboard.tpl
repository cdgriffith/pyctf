% include('header.tpl', scoreboard="active")

        <div class="main-area" ng-controller="scoreController">
            <div id="score-list">
                <div class="row">
                    <div class="col-md-6 title">Scoreboard</div>   <div class="col-md-6 filter-box"><form class="form-inline"><input ng-model="scoreListFilter" type="text" placeholder="Filter by" autofocus></form></div>
                </div>

                <div class="row">
                    <a class="list-group-item left-align" ng-repeat="score in scoreList | filter:scoreListFilter | orderBy: 'score'" >
                        <span ng-bind="score.score"></span>: <span ng-bind="score.name"></span>
                    </a>
                </div>
            </div>

        </div>

% include('footer.tpl')