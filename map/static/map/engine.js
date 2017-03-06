var down_x = down_y = 0;
var delta_x = delta_y = 0;
var move_x = move_y = 0
var svg_width = svg_height = 0;
var scale = 1;
var SCALE_MIN = 0.3;
var mapDoc, map_container, zoom_field;

var floors = {};
var active_floor = 2;

var CONST_LABEL_CLASS = 'lable-container';
var CONST_LABEL_PADDING = -15;


function getDelta(old, a1, a2) {
	return old + (a1 - a2) * (-1) / scale;
}

function mousemove(event) {
	if (event.type == 'mousemove') {
		move_x = getDelta(delta_x, down_x, event.clientX);
		move_y = getDelta(delta_y, down_y, event.clientY);
	} else {
		move_x = getDelta(delta_x, down_x, event.touches.item(0).clientX);
		move_y = getDelta(delta_y, down_y, event.touches.item(0).clientY);
	};
	map_container.style.transform = 'translate(' 
		+ move_x.toString() + 'px,' 
		+ move_y.toString() + 'px)';
}

function mouseup(event) {
	if (event.type == 'mouseup') {
		delta_x = getDelta(delta_x, down_x, event.clientX);
		delta_y = getDelta(delta_y, down_y, event.clientY);
		this.removeEventListener('mousemove', mousemove);
		this.removeEventListener('mouseup', mouseup);
	} else {
		delta_x = move_x;
		delta_y = move_y;
		this.removeEventListener('touchmove', mousemove);
		this.removeEventListener('touchend', mouseup);
	};  
}

function mousedown(event) {
	if (event.type == 'mousedown') {
		down_x = event.clientX;
		down_y = event.clientY;
		this.addEventListener('mousemove', mousemove); 
		this.addEventListener('mouseup', mouseup); 
	} else {
		down_x = event.touches.item(0).clientX;
		down_y = event.touches.item(0).clientY;
		this.addEventListener('touchmove', mousemove); 
		this.addEventListener('touchend', mouseup); 
	};
}

function zoom(value) {
	scale = scale - value;
	if (scale < SCALE_MIN ) scale = SCALE_MIN;
	zoom_field.style.transform = 'scale(' + scale.toString() + ')';
}

function zoom_mouse(event) {
	zoom(event.deltaY / 100);
}

function zoom_in(event) {
	zoom(-0.4);
}

function zoom_out(event) {
	zoom(0.4);
}


function createLabels(rooms_obj, label_obj) {
	var room;
	for (var i = 0; i < rooms_obj.childNodes.length; i++) {
		if (/^[Aabvgdlivz]+-[0-9]+.*$/.test(rooms_obj.childNodes[i].id)) {
			room = rooms_obj.childNodes[i];
		} else {
			continue;
		}
		try {
			label_text = rooms_info[room.id][0];
			switch (rooms_info[room.id][1]) {
				case 0:
					room.setAttribute('class','room_public');
					break;
				case 1:
					room.setAttribute('class','room_admin');
					break;
				case 2:
					room.setAttribute('class','room_cafe');
					break;
			};
		} catch (e) {
			continue
		};
		if (room.tagName == 'g') {
			var max_room = null;
			for (var j = 0; j < room.childNodes.length; j++) {
				try {
					subRect = room.childNodes[j].getBoundingClientRect();
					if (!max_room) {
						max_room = room.childNodes[j];
					}
					maxRect = max_room.getBoundingClientRect();
					if ((subRect.width + subRect.height) > (maxRect.width + maxRect.height)) {
						max_room = room.childNodes[j];				
					}
				} catch (e) {};
			}	
			if (max_room) {		
				room = max_room;
			} else continue;	
		}
		
		roomRect = room.getBoundingClientRect();
		label = document.createElement('div');
		label.style.width = Math.round(Number(roomRect.width)) + 'px';
		label.style.height = Math.round(Number(roomRect.height)) + 'px';
		label.style.left = roomRect.left + 'px';
		label.style.top = roomRect.top + 'px';
		text = document.createElement('span');
		text.innerHTML = label_text;
		label.appendChild(text);
		label_obj.appendChild(label);
	}
}

function init_floor (map_id) {
	map = document.getElementById(map_id);
	mapDoc = map.contentDocument;	
	svg_els = mapDoc.getElementsByTagName('svg');
	svg_scheme = svg_els[0];
	
	bbox = svg_scheme.getBoundingClientRect();
	if (svg_width == 0) {
		svg_width = bbox.width;
		svg_height = bbox.height;
	} else {
		svg_width = (svg_width + bbox.width) / 2;
		svg_height = (svg_height + bbox.height) / 2;
	};
	
	label_obj = document.createElement('div');
	label_obj.className = CONST_LABEL_CLASS;

	for (var i = 0; i < svg_scheme.childNodes.length; i++) {
		if (svg_scheme.childNodes[i].id == 'layer1') {
			window.setTimeout(createLabels(svg_scheme.childNodes[i], label_obj), 100);
			continue;
		}
	}

	floor_obj = document.createElement('div');
	floor_obj.id = map_id;
	floor_obj.appendChild(label_obj);
	floor_obj.appendChild(svg_scheme);
	floor_obj.style.display = 'none';
	map_container.appendChild(floor_obj);

	map.parentNode.removeChild(map);

	return floor_obj;
}

function adjustLabel(label_objs, i) {
	var tmp_field;
	for (var j=0; j<label_objs[i].childNodes.length;j++) {
		textRect = label_objs[i].childNodes[j];
		textNode = textRect.childNodes[0];
		width = Number(textRect.style.width.slice(0, -2));
		height = Number(textRect.style.height.slice(0, -2));	

		tmp_field  = document.createElement('div');
		tmp_field.style.position = 'absolute';
		map_container.appendChild(tmp_field);
		tmp_field.innerHTML = textNode.innerHTML;	
		fontSize = 1;
		if (Number(tmp_field.clientWidth) - width > CONST_LABEL_PADDING) {
			if (width - height > (-5) ) {
				while (Number(tmp_field.clientWidth) - width > CONST_LABEL_PADDING) {
					fontSize = (fontSize - 0.01).toFixed(2);
					tmp_field.style.fontSize = fontSize + 'em';
				}
			} else {
				while (Number(tmp_field.clientWidth) - height > CONST_LABEL_PADDING) {
					fontSize = (fontSize - 0.01).toFixed(2);
					tmp_field.style.fontSize = fontSize + 'em';
				};				

				deg = '-90';
				textRect.style.width	= height + 'px';
				textRect.style.height	= width + 'px';
				textRect.style.top		= (Number(textRect.style.top.slice(0, -2))+height)+'px';
				textRect.style.transformOrigin = '0 0'; 
				textRect.style.webkitTransform 	= 'rotate('+deg+'deg)'; 	
				textRect.style.mozTransform    	= 'rotate('+deg+'deg)'; 
				textRect.style.msTransform     	= 'rotate('+deg+'deg)'; 
				textRect.style.oTransform      	= 'rotate('+deg+'deg)'; 
				textRect.style.transform       	= 'rotate('+deg+'deg)'; 
			};	
			textNode.style.fontSize = fontSize + 'em';
		};				
		map_container.removeChild(tmp_field);			
	}
}

function adjustLabels() {
	label_objs = document.getElementsByClassName(CONST_LABEL_CLASS);
	for(var i=0; i<label_objs.length; i++) {
		// Give time to loader image for running
		window.setTimeout(adjustLabel(label_objs, i), 100);
	}
}

function showFloor(numb) {
	for (var i in floors) {
		floors[i].style.display = 'none';	
	}

	floors[numb].style.display = 'block';
	document.getElementById('floor_numb').innerHTML = numb;
}

function btnUp(event) {
	if (active_floor+1 in floors) {
		active_floor += 1;
		showFloor(active_floor);
	};
}

function btnDown(event) {
	if (active_floor-1 in floors) {
		active_floor -= 1;
		showFloor(active_floor);
	};
}

function putVertMid(element) {
	field_height = Number(document.getElementById('field').clientHeight);
	top_px = Math.round((field_height - Number(element.clientHeight))/2 );
	element.style.top = top_px.toString() + 'px';
}

function centerMapOnXY(x,y) {
	delta_x = (svg_width - x) * (-1); 
	delta_y = (svg_height - y) * (-1); 
	map_container.style.transform = 'translate(' 
		+ delta_x.toString() + 'px,' 
		+ delta_y.toString() + 'px)';
}

function init() {
	map_container = document.getElementById('map-container');
	zoom_field = document.getElementById('zoom-field');

	document.addEventListener('wheel', zoom_mouse);
	document.addEventListener('mousedown', mousedown);
	document.addEventListener('touchstart', mousedown);
	document.addEventListener('dragstart', null);

	floors[0] = init_floor('floor0');
	floors[1] = init_floor('floor1');
	floors[2] = init_floor('floor2');
	floors[3] = init_floor('floor3');
	floors[4] = init_floor('floor4');
	adjustLabels();
	showFloor(active_floor);
	centerMapOnXY((svg_width + window.innerWidth)/2+80 , (svg_height + window.innerHeight)/2-270);

	document.getElementById('btn_up').addEventListener('click', btnUp);
	document.getElementById('btn_down').addEventListener('click', btnDown);
	document.getElementById('zoom_in').addEventListener('click', zoom_in);
	document.getElementById('zoom_out').addEventListener('click', zoom_out);

	putVertMid(document.getElementById('btns_floor'));
	putVertMid(document.getElementById('btns_zoom'));

	load_img = document.getElementById('loader');
	load_img.parentNode.removeChild(load_img);
}

window.onload = function() {
	init();
}
