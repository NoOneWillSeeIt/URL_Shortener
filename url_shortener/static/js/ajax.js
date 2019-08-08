let range = document.getElementById('form_range');
let label = document.getElementById('label_form_range');

let shorten_btn = document.getElementById('shorten_btn');
let old_url_input_value = '';
let old_range_value = 0;

let duration = [
	{label: l10n.hours_24, hours: 24},
	{label: l10n.week_1, hours: 168},
	{label: l10n.week_2, hours: 336},
	{label: l10n.month_1, hours: 720},
	{label: l10n.month_2, hours: 1440}
]

shorten_btn.onclick = function() {
	url_link = document.getElementById('url_input').value;
	if (!url_link) {
		let report_div = document.getElementById('report');
		report_div.innerHTML = l10n.warning_paste_link;
		report_div.classList.remove('invisible');
		return;
	}

	if (old_url_input_value == url_link && range.value == old_range_value) {
		let report_div = document.getElementById('report');
		report_div.innerHTML = l10n.warning_paste_new_link;
		report_div.classList.remove('invisible');
		return;
	}

	document.getElementById('report').classList.add('invisible');
	old_url_input_value = url_link;
	old_range_value = range.value;
	
	let xhr = new XMLHttpRequest();
	xhr.open('POST', 'shrink', true);

	let body = new FormData();
	body.append('url', url_link);
	let hours = duration[range.value]['hours'];
	body.append('hours', hours.toString());

	xhr.onload = function() {
		if (xhr.status == 200 && xhr.readyState == 4) {
			let json_response = JSON.parse(xhr.responseText);
			let url_shortened = document.getElementById('url_shortened');
			url_shortened.innerHTML = json_response.shortened;
			document.getElementById('url_container').classList.remove('invisible');
		}
		else {
			let report_div = document.getElementById('report');
			let json_response = '';
			if (xhr.responseText && (xhr.responseType == 'json')) {
				json_response = JSON.parse(xhr.responseText)['error'];
			}
			else {
				if (xhr.status == 500)
					json_response = 'internal server error'
			}
			report_div.innerHTML = l10n.error_text + json_response;
			report_div.classList.remove('invisible');
		}
	};
	xhr.send(body);
};

let copy_btn = document.getElementById('copy_btn');

copy_btn.onclick = function() {
	let selection_range = document.createRange();
    selection_range.selectNode(document.getElementById('url_shortened'));
    let sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(selection_range);
    document.execCommand('copy');
}


function updateRangeInput() {
	label.innerHTML = duration[range.value]['label'];
}

range.addEventListener('change', updateRangeInput);
range.addEventListener('input', updateRangeInput);

range.value = 0;
updateRangeInput();