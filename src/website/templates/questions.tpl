% include('header.tpl', questions="active")

        <div class="main-area" ng-controller="questionController">
            <div id="question-list">
                <div class="row">
                    <div class="col-md-6 title">Questions</div>   <div class="col-md-6 filter-box"><form class="form-inline"><input ng-model="questionListFilter" type="text" placeholder="Filter by" autofocus></form></div>
                </div>

                <div class="row">
                    <a class="list-group-item left-align" ng-repeat="question in questionList | filter:questionListFilter | orderBy: 'number'" ng-click="selectQuestion(question.number)">
                        <span ng-bind="question.number"></span>: <span ng-bind="question.title"></span>
                    </a>
                </div>
            </div>

            <div id="question-body" class="left-align">
                <div class="row">
                    <div class="title col-md-10" ng-bind="currentQuestion.title"></div>
                    <div class="col-md-2 pull-right"><button class="btn btn-success pull-right" ng-click="backToList()">Back to Questions</button> </div>
                </div>
                <div class="row">
                    <div class="col-md-1">Question: </div>
                    <div class="col-md-11" ng-bind="currentQuestion.question"></div>
                </div>
                <div class="row" ng-hide="! currentQuestion.data">
                    <div class="col-md-1">Data: </div>
                    <div class="col-md-11" ng-bind="currentQuestion.data"></div>
                </div>
                <div class="row" ng-hide="! currentQuestion.media">
                    <div class="col-md-1">Media: </div>
                    <div class="col-md-11"> <a class="btn btn-success" href="{{'{{currentQuestion.media}}'}}" target="_blank" >Download</a></div>
                </div>
                <div class="row"  ng-hide="currentQuestion.time_limit == 0">
                    <div class="col-md-1">Time Limit: </div>
                    <div class="col-md-11" ng-bind="currentQuestion.time_limit"></div>
                </div>

                <div class="row">
                    <form ng-submit="answerQuestion()">
                        <div class="form-group">
                           <div class="col-md-1"> <label for="answer-box">Answer: </label></div>
                            <div class="col-md-11"> <textarea ng-model="answer" class="form-control" id="answer-box"></textarea></div>
                        </div>
                        <div class="col-md-1 pull-right"><input type="submit" id="submit-answer" class="btn btn-primary pull-right" /></div>
                    </form>
                </div>

            </div>


        </div>

% include('footer.tpl')