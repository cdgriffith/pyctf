$(document).ready(on_page_load);

$("#go_home").click(go_home);
$("#go_questions").click(go_questions);
$("#go_scoreboard").click(go_scoreboard);


function on_page_load(){

	if (typeof $.cookie('pyctf_auth_token') === "undefined"){
		$("#login_button").click(login);
	}
	else {
		auth_refresh();
		$("#login").hide();
		show_user($.cookie('pyctf_auth_user'));
	}
};


function clear_top_menu(){
	$(".menuitem").removeClass("menu-select");
};

function clear_body(){
	$("#leftcol").children().hide();
};

function change_page(menu_item, body_id){
	clear_body();
	clear_top_menu();
	$(menu_item).addClass("menu-select");
	$(body_id).show();
};

function go_home(){
	change_page("#go_home", "#home_body");
};


function go_questions(){
	change_page("#go_questions", "#question_list_body");

	$('#question_table_area').html( '<table cellpadding="0" cellspacing="0" border="0" class="display cell-border" id="question_table"></table>' );

    var table = $('#question_table').DataTable( {
        "aoColumns": [
        { "sTitle": "Question",  "sWidth": "15%" },
        { "sTitle": "Title", "sWidth": "60%" },
        { "sTitle": "Tags", "sWidth": "25%" },
    ],
    	"table": ["cell-border"],
        "ajax": "/questions/list",
        "pageLength": 25

    } );

	$('#question_table tbody').on( 'click', 'tr', function () {
		var data = table.row(this).data();
		if (! data){
			return;
		}
		go_single_question(data[0]);
	} );

};

function go_scoreboard(){
	change_page("#go_scoreboard", "#scoreboard_body");

	$('#scoreboard_table_area').html( '<table cellpadding="0" cellspacing="0" border="0" class="display" id="scoreboard_table"></table>' );

    var table = $('#scoreboard_table').DataTable( {
        "ajax": "/scoreboard/list",
        "columns": [
            { "title": "User" },
            { "title": "Score" }],
        "order": [[ 1, "desc" ]],
        "pageLength": 10
    } );
};

function go_single_question(question_number){
	if (! question_number){
		return;
	};

	clear_body();
	$("#question_body").show();

	$.ajax({
		url: "/question/" + question_number,
		dataType: "json",
		success: function(data){set_question(question_number, data)},
		error: go_home
	});

};

function set_question(question_number, ajax_data){
	var title = ajax_data.title;
	var question = ajax_data.question;
	var data = ajax_data.data;
	var timeout = ajax_data.timeout;
	var media = ajax_data.media;
	var token = ajax_data.token;
	var answer_type  = ajax_data.answer_type;

	$("#bc_question_number").text(question_number);
	$("#answer_type").val(answer_type);

	if(! media || typeof media === "undefined"){
		$("#download_row").hide();
	}
	else {
		$("#download_row").show();
		$("#download_media").html("<a href='"+ media +"' target='_blank'><button>Download</button></a>");
	}

	$("#question_title").html("<h3>" + question_number+ " : " + title + "</h3>");
	$("#question_text").text(question);
	$("#token").val(token);
	$("#question_number").val(question_number);
	$("#bc_questions").off("click").click(go_questions);

	if(data){
		$("#data_text").text(JSON.stringify(data)).show();
		$("#data_row").show();
	}else{
		$("#data_row").hide();
	};

	if(typeof $.cookie("pyctf_auth_token") === "undefined"){
		$("#submit_answer").prop('disabled', true).val("Please login");
	}
	else {
		$("#answer_box").prop('disabled', false);
		$("#submit_answer").prop('disabled', false);
		$("#submit_answer").val("Submit");
		$("#submit_answer").off("click").click(answer_question);
	}

};

function answer_question(){

	$("#answer_box").prop('disabled', true);
	$("#submit_answer").prop('disabled', true);

	var token = $("#token").val();
	var question_number = $("#question_number").val();
	var answer_box = $("#answer_box").val();
	var answer_type = $("#answer_type").val();
	var answer = null;

	if (! answer_type || answer_type == "string"){
		answer = answer_box;
	}else if (answer_type == "int"){
		answer = parseInt(answer_box);
	}
	else{
		answer = JSON.parse(answer_box);
	}

	$.ajax({
		url: "/answer/"+ question_number,
		type: "POST",
		dataType: "json",
		data: JSON.stringify({"token": token, "answer": answer, "auth_token": $.cookie("pyctf_auth_token")}),
        contentType: "application/json; charset=utf-8",
		success: function(data){
			if (data.correct){
				message("Correct!");
				go_scoreboard();
				}
			else{
				error("Incorrect");
				go_single_question(question_number);
			};
		},
		error: function(jqXHR, textStatus, errorThrown){
			alert(textStatus);
			alert(errorThrown);
			go_single_question(question_number);

		}
	});

}

function show_user(username){
			$("#login").hide();
			$("#userinfo").show();
			$("#user_message").text("Welcome " + username);
			$("#logout_button").off("click").click(logout);
			$("#submit_answer").off("click").click(answer_question);
			$("#submit_answer").prop('disabled', false);
			$("#submit_answer").val("Submit");
}

function show_login(){
			$("#login").show();
			$("#userinfo").hide();
			$("#user_message").text("");
			$("#login_button").off("click").click(login);
}

function login(){
	username = $("#login_user").val();
	password = $("#login_password").val();
	if (username == "" || password == ""){
		alert("Please provide a username and password");
		return;
	}

	$.ajax({
		url: "/login",
		type: "POST",
		dataType: "json",
		data: JSON.stringify({"user": username, "password": password}),
        contentType: "application/json; charset=utf-8",
		success: function(data){
		 	var date = new Date();
 		 	var minutes = date.timeout;
 		 	date.setTime(date.getTime() + (minutes * 60 * 1000));
			$.cookie('pyctf_auth_token', data.auth_token, { expires: date });
			$.cookie('pyctf_auth_user', username);
			show_user(username);
		},
		error: function(jqXHR, textStatus, errorThrown){
			error("Could not login - please try again");
		}
	});

};

function logout(){
	$.removeCookie('pyctf_auth_token');
	$.removeCookie('pyctf_auth_user');
	show_login();
}


function auth_refresh(){
	$.ajax({
		url: "/user/auth_refresh",
		type: "POST",
		dataType: "json",
		data: JSON.stringify({"auth_token": $.cookie("pyctf_auth_token")}),
        contentType: "application/json; charset=utf-8",
		error: function(jqXHR, textStatus, errorThrown){
			logout();
		}
	});
}

function message(message, delay){
	$("#error").hide();
	if(typeof(delay)==='undefined') delay = 4000;
	$("#message").show().text(message).delay(delay).fadeOut("slow");
};

function error(message, delay){
	$("#message").hide();
	if(typeof(delay)==='undefined') delay = 4000;
	$("#error").show().text(message).delay(delay).fadeOut("slow");
};

