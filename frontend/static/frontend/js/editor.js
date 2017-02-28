var fields_name = ['name', 'rec_id', 'id_hash', 'day', 'numb', 'teacher', 'week', 'room'];

function showForm(event) {
	event = event || window.event;
	lesson_div = event.target;
	while (!(lesson_div.className == 'event' || lesson_div.className == 'new_event')) {
		lesson_div = lesson_div.parentNode;
	};
	
	container_pos 	= lesson_div.getBoundingClientRect();
	form 			= document.getElementById('form_edit');
	form_title 		= document.getElementById('title');
	form_hide 		= document.getElementById('input_hide');
	field_hide 		= document.getElementById('hide');
	form_delete 	= document.getElementById('input_delete');
	
   	form_hide.style.display = 'none';
	field_hide.checked = '';
	form_delete.style.display = 'none';
	document.getElementById('delete').checked	= '';
	form_title.innerHTML = 'Добавление';
	for (var i = 0; i < fields_name.length;i++) {
		document.getElementById(fields_name[i]).value 	= '';
	}
		 
	if (lesson_div.className == 'event') {
		form_title.innerHTML = 'Изменение';
		for (var i = 0; i < fields_name.length;i++) {
			document.getElementById(fields_name[i]).value = schedule_full[lesson_div.id][fields_name[i]];
		};
		form_hide.style.display = 'block';
		if (schedule_full[lesson_div.id]['hide'] == 'True') {
			field_hide.checked = 'checked';
		}
		if (schedule_full[lesson_div.id]['is_user'] == 'True') {
			form_delete.style.display = 'block';
		}
    } else {
		document.getElementById('day').value = lesson_div.dataset.day;
		document.getElementById('numb').value = lesson_div.dataset.numb;
    };
    
	form.style.width = lesson_div.offsetWidth.toString() + 'px';
	form.style.left = (container_pos.left + window.scrollX ).toString() + 'px';
	form.style.top = (container_pos.top + window.scrollY).toString() + 'px';
	form.style.display = 'inline-block';
}

function hideForm(event) {
	document.getElementById('form_edit').style.display = 'none';
}

function switchByID(event) {
	event = event || window.event;
	switcher = event.target;
	var xhr = new XMLHttpRequest();
	xhr.open('GET', 'http://botpage.ru/switcher/' + switcher.id, false);
	xhr.send();
	location.href = location.href;
}

function setListenerByIds(ids, listener,  event = 'click') {
	for (var i=0; i<ids.length; i++) {	
		document.getElementById(ids[i]).addEventListener(event, listener);
	}
}

function init() {
	var btns = document.getElementsByClassName('show');
	for (var i=0; i<btns.length; i++) {
		btns[i].addEventListener('click', showForm);
	}
	btns = document.getElementsByClassName('new_event');
	for (var i=0; i<btns.length; i++) {
		btns[i].addEventListener('click', showForm);
	}
	setListenerByIds(['close'], hideForm);
	
	panel_ids = ['mode_base', 'mode_user', 'view_teacher', 'view_weekroom', 'notice_today', 'notice_tomorrow', 'notice_week', 'notice_map'];
	setListenerByIds(panel_ids, switchByID);
}

window.onload = function() {
	init();
}
