from dataclasses import dataclass, field
from glob import iglob
import pickle
from os import PathLike
from re import compile
from secrets import choice
from typing import Any


@dataclass
class MarkovWord:
	"""A class for storing a word and its weight."""

	word: str
	weight: int = 1

	def __post_init__(self):
		self.word = self.word.lower()


class MarkovChain:
	"""A text Markov chain."""

	_word_regex = compile(r'[\w-]+(?:\'\w+)?')

	def __init__(self, ngram: int = 2, chain: dict = None) -> None:
		self.ngram = ngram
		self.chain = {} if chain is None else chain

	def train(self, src: str) -> None:
		"""Train Markov chain on src string."""

		# lower case and split src in to words, don't preserve whitespace or
		# punctuation (except hyphens and apostrophes)
		words = MarkovChain._word_regex.findall(src.lower())
		print(f'# words: {len(words)}')

		# count new keys
		new_keys = 0

		# loop over all words
		for i in range(len(words) - self.ngram):
			# create key of length self.ngram
			key = tuple(words[i : i + self.ngram])
			next_word = words[i + self.ngram]

			if key not in self.chain:
				self.chain[key] = []
				new_keys += 1

			# find existing MarkovWord for next_word and increment its weight
			nw_not_found = True
			for mw in self.chain[key]:
				if mw.word == next_word:
					mw.weight += 1
					nw_not_found = False
					break

			# if next_word is not found, add it with weight of 1
			if nw_not_found:
				mw = MarkovWord(word=next_word, weight=1)
				self.chain[key].append(mw)

		print(f'# new keys added: {new_keys}')

		# loop over all lists of next words in self.chain and sort them
		# by weight, descending. this is slow in training, but fast in
		# generation
		for mw_list in self.chain.values():
			mw_list.sort(key=lambda mw: mw.weight, reverse=True)

		print('Training complete\n')


	def train_on_file(self, file_path: PathLike) -> None:
		"""Read file_path and train chain on text.
		
		Absolute or relative path."""

		print(f'Training on "{file_path}"')

		with open(file=file_path, mode="r") as f:
			text = f.read()

		self.train(src=text)

	def train_on_dir(self, dir_path: PathLike, recursive: bool = False) -> None:
		"""Read every file in dir_path and train chain on text.

		Absolute or relative path. Can contain shell-style wildcards.
		ex: train_on_dir('./training_data/*.txt')"""

		for file_path in iglob(pathname=dir_path, recursive=recursive):
			self.train_on_file(file_path=file_path)

	def save(self, file_path: PathLike) -> None:
		"""Pickle Markov chain and save to file_path."""

		with open(file=file_path, mode="wb") as f:
			obj = {"ngram": self.ngram, "chain": self.chain}
			pickle.dump(obj=obj, file=f)

		print(f"Saved to: {file_path}")

	@classmethod
	def load(cls, file_path: PathLike) -> "MarkovChain":
		"""Load pickled Markov chain from file_path."""

		with open(file=file_path, mode="rb") as f:
			obj = pickle.load(file=f)

		return cls(ngram=obj["ngram"], chain=obj["chain"])

	def get_words(self, key: tuple) -> list[str]:
		"""Get a list of next words for a key."""

		# error handling
		if key not in self.chain:
			raise KeyError(f"Key {key} not in Markov chain.")

		return [mw.word for mw in self.chain[key]]

	def get_words_weighted(self, key: tuple) -> list[str]:
		"""Get a list of next words multiplied by weight for a key."""

		# error handling
		if key not in self.chain:
			raise KeyError(f"Key {key} not in Markov chain.")

		next_words = []

		for mw in self.chain[key]:
			for _ in range(mw.weight):
				next_words.append(mw.word)

		return next_words

	def generate(self, first_key: tuple[str] = None) -> Any:
		"""Generate text of longest length possible."""

		# error handling
		if first_key is not None and len(first_key) != self.ngram:
			raise KeyError(f"Key {first_key} must be of length {self.ngram}.")
		if first_key is not None and first_key not in self.chain:
			raise KeyError(f"Key {first_key} not in Markov chain.")

		# pick random first key if not provided
		if first_key is None:
			first_key = choice(list(self.chain.keys()))

		for word in first_key:
			yield word

		next_word = choice(self.get_words_weighted(key=first_key))
		yield next_word

		next_key = first_key[1:] + (next_word,)

		while next_key in self.chain:
			next_word = choice(self.get_words_weighted(key=next_key))
			yield next_word

			next_key = next_key[1:] + (next_word,)

	def gen_words(self, num_words: int, first_key: tuple[str] = None) -> str:
		"""Return up to num_words length of text."""

		words = []

		for word in self.generate(first_key=first_key):
			words.append(word)

			if len(words) >= num_words:
				break

		return " ".join(words)

	def gen_chars(self, num_chars: int = 280, first_key: tuple[str] = None) -> str:
		"""Return up to num_chars length of text."""

		words = []
		total_chars = 0

		for word in self.generate(first_key=first_key):
			total_chars += len(word)

			# account for 1 space between each word
			if total_chars + len(words) - 1 > num_chars:
				break

			words.append(word)

		return " ".join(words)
