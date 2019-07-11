
let shorten_btn = document.getElementById('shorten_btn');
let url_input = document.getElementById('url_input');

shorten_btn.onclick.preventDefault();

shorten_btn.onclick = function() {
	url_link = url_input.value
	if (!url_link) {
		return;
	}
	let xhr = XMLHttpRequest();
	xhr.open('POST', '/process', false);
	let json_body = JSON.stringify({
		url: url_link,
		hours: '24'
	});
	xhr.send(json_body);

	// if (xhr.status != 200) {
		json_response = JSON.parse(xhr.responseText);
		alert(json_response);
	// }
};
