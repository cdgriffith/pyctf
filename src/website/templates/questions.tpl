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
                <!-- <div id="question_breadcrumbs"><span id="bc_questions">Questions</span> > <span id="bc_question_number"></span> </div> -->
                <div class="row">
                    <div class="title col-md-12" ng-bind="currentQuestion.title"></div>
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
                    <div class="col-md-11"> <a href="{{'{{currentQuestion.media}}'}}" target="_blank" >Download</a></div>
                </div>
                <div class="row"  ng-hide="currentQuestion.time_limit == 0">
                    <div class="col-md-1">Time Limit: </div>
                    <div class="col-md-11" ng-bind="currentQuestion.time_limit"></div>
                </div>

                <div class="row">
                    <form ng-submit="answerQuestion()">
                        <div class="form-group">
                            <label for="answer-box">Answer: </label><textarea ng-model="answer" class="form-control" id="answer-box"></textarea>
                        </div>
                        <input type="submit" id="submit-answer" class="btn-primary" />
                    </form>
                </div>



                            <!--<table>
                            <tr> <td width="100px"><b>Question</b></td> <td> <div id="question_text"></div></td> </tr>
                            <tr id="data_row"> <td><b>Data </b></td> <td> <div id="data_text"></div> </td> </tr>
                            <tr id="download_row"> <td><b>Media </b></td> <td><div id="download_media"></div> </td> </tr>
                            <tr id="timeout_row"> <td><b>Timeout </b></td> <td><div id="timeout"></div> </td> </tr>
                            <tr> <td> <b>Answer </b>  </td> <td> <textarea name="answer"  id="answer_box"></textarea><br /> </td> </tr>
                            <input type="hidden" id="token" value="" />
                            <input type="hidden" id="question_number" value="" />
                            <input type="hidden" id="answer_type" value="" />
                            <tr> <td colspan="2"> <input id="submit_answer" type="button" value="Answer" name="submit_answer" /> </td> </tr>
                            </table>-->
            </div>


        </div>

% include('footer.tpl')