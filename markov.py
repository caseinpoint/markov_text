from collections import Counter
from dataclasses import dataclass, field
from glob import iglob
from os import PathLike


@dataclass
class MarkovLink:
	"""Class for storing the values for each key in a Markov chain."""

	is_cap: bool = False
	# count number of times each word follows the key in source text
	word_weights: Counter = field(default_factory=Counter)


class MarkovChain:
	def __init__(self, ngram: int = 2) -> None:
		self.ngram = ngram
		self.chain = {}

	def train(self, src: str) -> None:
		"""Train Markov chain on src string."""

		# split src in to words, preserve punctuation but not whitespace
		words = src.split()

		for i in range(len(words) - self.ngram):
			key = tuple(words[i : i + self.ngram])

			if key not in self.chain:
				is_cap = key[0][0].isupper()
				self.chain[key] = MarkovLink(is_cap=is_cap)

			self.chain[key].word_weights.update({words[i + self.ngram]: 1})

	def train_on_file(self, file_path: PathLike) -> None:
		"""Read file_path and train chain on text."""

		with open(file=file_path, mode='r') as f:
			text = f.read()

		self.train(src=text)

	def train_on_directory(self, dir_path: PathLike, recursive: bool = False) -> None:
		"""Read every file in dir_path and train chain on text."""

		for file_path in iglob(pathname=dir_path, recursive=recursive):
			print(file_path)
			self.train_on_file(file_path=file_path)

	def capital_keys(self) -> list:
		"""Get all keys that begin with a capital letter."""

		return [key for key,link in self.chain.items() if link.is_cap]
