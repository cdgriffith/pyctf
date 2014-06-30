<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <title>{{get('title', "PyCTF")}}</title>
    <link rel="stylesheet" type="text/css" href="/static/main.css">
</head>
<body>
    <div id="body">
        <div id="header">
            <div id="sitename">PyCTF</div>

            <div id="topmenu">
                <a href="/"><div class="menuitem">Home</div></a>
                <div class="menuitem">Questions</div>
                <div class="menuitem" style="border-right: none">Scoreboard</div>
            </div>
        </div>
        <div id="content">
            <div id="leftcol"> </div>
            <div id="rightcol">
                <div id="login">
                    <form>
                        <table>
                            <tr>
                                <td><label for="user">Username: </label> </td><td> <input type="text" name="user" /> </td>
                            </tr>
                            <tr>
                               <td> <label for="user">Password: </label> </td><td> <input type="password" name="password" /></td>
                            </tr>
                            <tr>
                                <td columnspan="2"> <input type="button" name="login" value="Login" /> </td>
                            </tr>
                        </table>
                    </form>
                </div>
                <div id="userinfo">

                </div>

            </div>

        </div>
    </div>
</body>
</html>