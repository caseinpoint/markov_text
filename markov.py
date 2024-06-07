from collections import Counter
from dataclasses import dataclass, field


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
