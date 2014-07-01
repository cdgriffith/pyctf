<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>{{get('title', "PyCTF")}}</title>
    <link rel="stylesheet" type="text/css" href="/static/css/main.css">
    <link rel="stylesheet" type="text/css" href="/static/css/jquery.dataTables.css">
</head>
<body>
    <div id="body">
        <div id="header">
            <div id="sitename">PyCTF</div>

            <div id="topmenu">
                <div id="go_home" class="menuitem">Home</div>
                <div id="go_questions" class="menuitem">Questions</div>
                <div id="go_scoreboard" class="menuitem" style="border-right: none">Scoreboard</div>
            </div>
        </div>
        <div id="content">
            <div id="leftcol">
                <div id="home_body">
                    <h1>Home</h1>

                </div>

                <div id="question_list_body">
                    <h1>Questions</h1>
                    <div id="question_table_area"> </div>
                </div>

                <div id="scoreboard_body">
                    <h1>Scoreboard</h1>
                    <div id="scoreboard_table_area"> </div>
                </div>

                <div id="question_body">
                    <div id="question_breadcrumbs"><span id="bc_questions">Questions</span> > <span id="bc_question_number"></span> </div>
                    <div id="question_title"></div>
                    <div id="question_text"></div>
                    <div id="data_text"></div>
                    <div id="download_media"></div>
                    <div id="answer_box"><textarea name="answer"></textarea><br />
                    <input id="submit_answer" type="button" value="Answer" name="submit_answer" />
                    </div>


                </div>

            </div>


            <div id="rightcol">
                <div id="login">
                    <form>
                        <table>
                            <tr>
                                <td><label for="login_user">Username: </label> </td><td> <input id="login_user" type="text" name="user" /> </td>
                            </tr>
                            <tr>
                               <td> <label for="login_password">Password: </label> </td><td> <input id="login_password" type="password" name="password" /></td>
                            </tr>
                            <tr>
                                <td columnspan="2"> <input id="login_button" type="button" name="login" value="Login" /> </td>
                            </tr>
                        </table>
                    </form>
                </div>


                <div id="userinfo">

                </div>

            </div>

        </div>
    </div>

    <script src="/static/js/jquery-2.1.1.min.js"></script>
    <script src="/static/js/jquery.dataTables.js"></script>
    <script src="/static/js/jquery.cookie.js"></script>
    <script src="/static/js/main.js"></script>
</body>
</html>