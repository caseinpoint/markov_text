'use strict';

// regex for words with possible hyphens and apostrophes
const wordRegex = /[\w-]+('[\w]+)?/g;

const textNpt = document.getElementById('text_npt');

function handleKeyUp(evt) {
    console.log(evt);

    if (evt.key === 'Tab') {
        // don't tab out of textarea
        evt.preventDefault();
    }

    const value = evt.target.value;

    let words = value.match(wordRegex);
    if (words !== null) {
        // get last 2 words and lower case them
        words = words.slice(-2).map((w) => w.toLowerCase());
    }
    console.log(words);
}

textNpt.addEventListener('keyup', handleKeyUp);
