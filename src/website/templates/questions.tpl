% include('header.tpl', questions="active")

        <div class="main-area" ng-controller="questionController">
            <!--
                        <div id="question_body">
                            <div id="question_breadcrumbs"><span id="bc_questions">Questions</span> > <span id="bc_question_number"></span> </div>
                            <div id="question_title"></div>

                            <table>
                            <tr> <td width="100px"><b>Question</b></td> <td> <div id="question_text"></div></td> </tr>
                            <tr id="data_row"> <td><b>Data </b></td> <td> <div id="data_text"></div> </td> </tr>
                            <tr id="download_row"> <td><b>Media </b></td> <td><div id="download_media"></div> </td> </tr>
                            <tr id="timeout_row"> <td><b>Timeout </b></td> <td><div id="timeout"></div> </td> </tr>
                            <tr> <td> <b>Answer </b>  </td> <td> <textarea name="answer"  id="answer_box"></textarea><br /> </td> </tr>
                            <input type="hidden" id="token" value="" />
                            <input type="hidden" id="question_number" value="" />
                            <input type="hidden" id="answer_type" value="" />
                            <tr> <td colspan="2"> <input id="submit_answer" type="button" value="Answer" name="submit_answer" /> </td> </tr>
                            </table>
                        </div>
                        --->
            <div id="question-list">
                <a class="list-group-item" ng-repeat="question in questionList | orderBy: number" ng-click="selectQuestion(question[0])">
                    <span ng-bind="question.number"></span>: <span ng-bind="question.title"></span>
                </a>
            </div>



        </div>

% include('footer.tpl')