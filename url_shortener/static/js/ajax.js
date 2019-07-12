
let shorten_btn = document.getElementById('shorten_btn');
let copy_btn = document.getElementById('copy_btn');

shorten_btn.onclick = function() {
	url_link = document.getElementById('url_input').value;
	if (!url_link) {
		return;
	}
	let xhr = new XMLHttpRequest();
	xhr.open('POST', 'process', true);

	let body = new FormData();
	body.append('url', url_link);
	body.append('hours', '24');
	
	xhr.onload = function() {
		if (xhr.status == 200 && xhr.readyState == 4) {
			let json_response = JSON.parse(xhr.responseText);
			let url_shortened = document.getElementById('url_shortened');
			let link = window.location.protocol + '//' + window.location.host + '/' + json_response.shortened;
			url_shortened.innerHTML = link;
			document.getElementById('url_container').style.display = 'block';
		}
		else {
			let report_div = document.getElementById('report');
			let json_response = '';
			if (xhr.responseText) {
				let json_response = JSON.parse(xhr.responseText)['error'];
			}
			report_div.setText('error ' + json_response);
			report_div.style.display = 'block';
		}
	};
	xhr.send(body);
};

copy_btn.onclick = function() {
	let range = document.createRange();
    range.selectNode(document.getElementById('url_shortened'));
    let sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
    document.execCommand("copy");
}