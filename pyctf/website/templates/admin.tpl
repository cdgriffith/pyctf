% include('header.tpl', admin="active")
<div class="main-area" ng-controller="adminController">
    <div id="admin_area">
        <div class="row">
            <div class="title col-md-2 left-align">Admin Area</div>

            <div class="col-md-4 btn-group pull-right" role="group" ng-init="selectedButton = 'general'">
                <button ng-class="{'active':selectedButton === 'general'}" ng-click="selectedButton = 'general'"
                        type="button" class="btn btn-default">General
                </button>
                <button ng-class="{'active':selectedButton === 'account'}" ng-click="selectedButton = 'account'"
                        type="button" class="btn btn-default">Accounts
                </button>
                <button ng-class="{'active':selectedButton === 'questions'}" ng-click="selectedButton = 'questions'"
                        type="button" class="btn btn-default">Questions
                </button>
                <button ng-class="{'active':selectedButton === 'score'}" ng-click="selectedButton = 'score'"
                        type="button" class="btn btn-default">Scoreboard
                </button>
            </div>

        </div>

        <div id="accounts" ng-show="selectedButton === 'account'">
            <div id="add-account" class="row sep">
                <div class="col-md-2 left-align"><b>Add Account</b></div>
                <form ng-submit="addUser()">
                    <div class=" col-md-3">
                        <div class="form-group">
                            <label class="sr-only" for="newUser">User</label>
                            <input type="text" class="form-control" id="newUser" ng-model="newUser"
                                   placeholder="username">
                        </div>
                    </div>
                    <div class=" col-md-3">
                        <div class="form-group">
                            <label class="sr-only" for="newPass">Password</label>
                            <input type="password" class="form-control" id="newPass" ng-model="newPass"
                                   placeholder="password">
                        </div>
                    </div>
                    <div class=" col-md-2">
                        <div class="form-group">
                            <label class="inline" for="newAdmin">Admin</label>
                            <input type="checkbox" class="inline" ng-model="newAdmin" id="newAdmin">
                        </div>
                    </div>
                    <div class="col-md-2 pull-right">
                        <button type="submit" style="width:125px" class="btn btn-success">Add User</button>
                    </div>
                </form>
            </div>

            <div id="remove-account" class="row sep">
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
                        <button type="submit" style="width:125px;" class="btn btn-danger">Remove User</button>
                    </div>
                </form>
            </div>
        </div>

        <div id="new-question" ng-show="selectedButton === 'questions'">

            <form class="form-horizontal" ng-submit="addQuestion()">
                <div style="width:100%" class="row left-align"><b>New Question</b></div>
                <div class="row sep">
                    <div class="col-md-6">
                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionTitle">Title</label>

                            <div class="col-md-10">
                                <input type="text" class="form-control" id="questionTitle" ng-model="questionTitle"
                                       placeholder="Title">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionBody">Question</label>

                            <div class="col-md-10">
                                <textarea class="form-control" id="questionBody" ng-model="questionBody"
                                          placeholder="Question"></textarea>
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionPoints">Points</label>

                            <div class="col-md-10">
                                <input type="text" class="form-control" id="questionPoints" ng-model="questionPoints"
                                       placeholder="Points">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionAnswer">Answer</label>

                            <div class="col-md-10">
                                <input type="text" class="form-control" id="questionAnswer" ng-model="questionAnswer"
                                       placeholder="Answer">
                            </div>
                        </div>
                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionTimeout">Time&nbsp;Limit</label>

                            <div class="col-md-10">
                                <input type="text" class="form-control" id="questionTimeout" ng-model="questionTimeout"
                                       placeholder="Timeout (seconds)">
                            </div>
                        </div>

                    </div>
                    <div class="col-md-6">


                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionMedia">Media</label>

                            <div class="col-md-10">
                                <input type="file" class="file" id="questionMedia" ng-model="questionMedia">
                            </div>

                        </div>

                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionScript">Script</label>

                            <div class="col-md-10">
                                <input type="file" class="file" id="questionScript" ng-model="questionScript">
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="col-md-3 control-label"
                                   for="questionScriptGenerate">Question&nbsp;Script</label>

                            <div class="col-md-9">
                                <input type="text" class="form-control" id="questionScriptGenerate"
                                       ng-model="questionScriptGenerate" placeholder="python example_script.py -q">
                            </div>
                        </div>

                        <div class="form-group">
                            <label class="col-md-3 control-label" for="questionScriptAnswer">Answer&nbsp;Script</label>

                            <div class="col-md-9">
                                <input type="text" class="form-control" id="questionScriptAnswer"
                                       ng-model="questionScriptAnswer" placeholder="python example_script.py -a">
                            </div>

                        </div>

                        <div class="form-group">
                            <label class="col-md-2 control-label" for="questionAnswerType">Answer&nbsp;Type</label>

                            <div class="col-md-10">
                                <input type="text" class="form-control" id="questionAnswerType"
                                       ng-model="questionAnswerType" placeholder="integer">
                            </div>
                        </div>
                        <div class="pull-right">
                            <button class="btn btn-success" type="submit">Add Question</button>
                        </div>
                    </div>

                </div>

            </form>

            <div id="remove-question" class="row sep">
                <div class="col-md-2 left-align"><b>Remove Question</b></div>
                <form class="form-inline" ng-submit="removeQuestion()">
                    <div class=" col-md-8">
                        <div class="form-group">
                            <label class="sr-only" for="questionToRemove">Question</label>
                            <select id="questionToRemove" ng-model="questionToRemove">
                                <option ng-selected="{{'{{question.number == questionToRemove}}'}}"
                                        ng-repeat="question in questionList | orderBy: question.number"
                                        value="{{'{{question.number}}'}}">
                                    {{'{{question.number}}: {{question.title}}'}}
                                </option>
                            </select>
                        </div>
                    </div>
                    <div class="col-md-2 pull-right">
                        <button type="submit" class="btn btn-danger">Remove Question</button>
                    </div>
                </form>
            </div>


        </div>

    </div>

</div>
% include('footer.tpl')




