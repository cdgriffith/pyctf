% include('header.tpl', scoreboard="active")

<div class="main-area" ng-controller="scoreController">
    <div id="score-list">
        <div class="row">
            <div class="col-md-6 title">Scoreboard</div>

            <div class="col-md-6 filter-box">
                <form class="form-inline"><input ng-model="scoreListFilter" type="text" placeholder="Filter by"
                                                 autofocus></form>
            </div>
        </div>

        <div class="row">
            <div class="col-md-2 left-align" style="cursor: pointer" ng-click="updateSort('score')"><b>Score</b>

                <div ng-class="{'glyphicon-triangle-bottom': scoreboardListOrder=='score' && ! scoreboardListOrderReverse, 'glyphicon-triangle-top': scoreboardListOrder=='score' && scoreboardListOrderReverse}"
                     class="glyphicon"></div>
            </div>
            <div class="col-md-3" style="cursor: pointer" ng-click="updateSort('user')"><b>User</b>

                <div ng-class="{'glyphicon-triangle-bottom': scoreboardListOrder=='user' && ! scoreboardListOrderReverse, 'glyphicon-triangle-top': scoreboardListOrder=='user' && scoreboardListOrderReverse}"
                     class="glyphicon"></div>
            </div>
        </div>

        <div class="row">
            <div class="row list-group-item"
                 ng-repeat="score in scoreList | filter:scoreListFilter | orderBy: scoreboardListOrder: scoreboardListOrderReverse">
                <div class="col-md-2 left-align" ng-bind="score.score"></div>
                <div class="col-md-3 left-align" ng-bind="score.name"></div>

            </div>
        </div>
    </div>

</div>

% include('footer.tpl')