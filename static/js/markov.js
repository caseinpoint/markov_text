'use strict';


// DOM elements
const randomForm = document.querySelector('#random_form');
const authorSel = document.querySelector('#author_sel');
const numIpt = document.querySelector('#num_ipt');
const wordsRdo = document.querySelector('#words_radio');
const charsRdo = document.querySelector('#chars_radio');
const randomOpt = document.querySelector('#random_opt');


// event handlers
async function handleSubmit(evt) {
	evt.preventDefault();

	const author = authorSel.value;
	const formData = {
		words: wordsRdo.checked,
		num: Number(numIpt.value)
	}

	try {
		const response = await fetch(`/api/generate/${author}.json`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(formData)
		});

		const result = await response.json();

		if (result.success) {
			randomOpt.textContent = result.text;
		} else {
			console.error(result);
		}
	} catch (err) {
		console.error(err);
	}
}


randomForm.addEventListener('submit', handleSubmit);
