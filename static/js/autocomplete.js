"use strict";

// regex for words with possible hyphens and apostrophes
const wordRegex = /[\w-]+('[\w]+)?/g;

// DOM elements
const authorSel = document.getElementById("author_sel");
const textNpt = document.getElementById("text_npt");
const wordsDiv = document.getElementById("words_res");
const moreDiv = document.getElementById("more_res");
const noResBtn = document.getElementById('no_res_btn');

// utilities for button elements
const primaryClasses = ['col-3', 'btn', 'btn-outline-primary', 'res_btn'];
const primarySups = ['TAB', 'CTRL+2', 'CTRL+3', 'CTRL+4'];
const secondClasses = ['col-2', 'btn', 'btn-outline-secondary', 'res_btn'];


function handleClick(evt) {
	// insert a space before the word if there isn't one already
	const insertSpace = textNpt.value.match(/\s$/) === null ? ' ' : '';

	// add word to text area
	textNpt.value += insertSpace + evt.target.value;

	// focus text area and fire event to update suggestions
	textNpt.focus()
	textNpt.dispatchEvent(new Event('input', {bubbles: true}));
}


function createBtns(words) {
	if (words.length > 4) {
		moreDiv.classList.remove('d-none');
	} else {
		moreDiv.classList.add('d-none');
	}

	for (let [i, word] of words.entries()){
		const newBtn = document.createElement('button');
		newBtn.type = 'button';
		newBtn.id = `w_btn_${i}`;
		newBtn.textContent = word;
		newBtn.value = word;
		newBtn.addEventListener('click', handleClick);

		if (i < 4) {
			newBtn.classList.add(...primaryClasses);
			newBtn.insertAdjacentHTML('beforeend',
				` <sup class="text-secondary">${primarySups[i]}</sup>`
			);
			wordsDiv.append(newBtn);
		} else {
			newBtn.classList.add(...secondClasses);
			moreDiv.append(newBtn);
		}
	}
}


async function handleInput(evt) {
	const value = evt.target.value;

	let words = value.match(wordRegex);
	if (words !== null && words.length >= 2) {
		// get last 2 words and lower-case them
		words = words.slice(-2).map((w) => w.toLowerCase());

		// get author from select
		const author = authorSel.value.toLowerCase();

		// send last 2 words and author to server
		const response = await fetch(`/api/suggest/${author}.json`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({key: words})
		});

		const result = await response.json();

		// remove any previous suggestions
		for (let btn of document.querySelectorAll('.res_btn')) {
			btn.remove();
		}

		if (result.success) {
			// hide no results button
			noResBtn.classList.add('d-none');

			createBtns(result.words);
		} else {
			// show the no results button
			noResBtn.classList.remove('d-none');
		}
	} else {
		// show the no results button
		noResBtn.classList.remove('d-none');

		// remove any previous suggestions
		for (let btn of document.querySelectorAll('.res_btn')) {
			btn.remove();
		}
	}
}


function handleKeyDown(evt) {
	let btn;

	if (evt.key === "Tab") {
		// don't tab out of textarea
		evt.preventDefault();

		btn = document.querySelector('#w_btn_0');
	} else if (evt.ctrlKey && evt.key === '2') {
		btn = document.querySelector('#w_btn_1');
	} else if (evt.ctrlKey &&evt.key === '3') {
		btn = document.querySelector('#w_btn_2');
	} else if (evt.ctrlKey && evt.key === '4') {
		btn = document.querySelector('#w_btn_3');
	}

	if (btn !== undefined) {
		btn.click();
	}
}

textNpt.addEventListener('input', handleInput);
textNpt.addEventListener("keydown", handleKeyDown);
