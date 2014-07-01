$(document).ready(on_page_load);

$("#go_home").click(go_home);
$("#go_questions").click(go_questions);
$("#go_scoreboard").click(go_scoreboard);


function on_page_load(){

	if (typeof $.cookie('pyctf_auth_token') === "undefined"){
		$("#login_button").click(login);
	}
	else {
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
            { "title": "Score" }]
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
		success: function(data){set_question(question_number, data.title, data.question, data.data, data.timeout, data.media)},
		failure: function(){}
	});

};

function set_question(question_number, title, question, data, timeout, media){
	$("#bc_question_number").text(question_number);

	if(! title || typeof tile === "undefined"){
		title = "";
	}

	if(! media || typeof media === "undefined"){
		$("#download_media").html("").hide();
	}
	else {
		$("#download_media").show();
		$("#download_media").html("<a href='"+ media +"' target='_blank'><button>Download Media</button></a>");
	}

	$("#question_title").html("<h3>" + question_number+ " : " + title + "</h3>");
	$("#question_text").text(question);

	$("#bc_questions").click(go_questions);

	if(data){
		$("#data_text").text(JSON.stringify(data));
	};

	if(typeof $.cookie("pyctf_auth_token") === "undefined"){
		$("#submit_answer").prop('disabled', true).val("Please login");
	};

};


function show_user(username){
			$("#login").hide();
			$("#userinfo").show();
			$("#userinfo").text("Welcome " + username);
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
		failure: function(){}
	});


};