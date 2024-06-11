# gramformer_demo.py

from annotated_text import annotated_text
from bs4 import BeautifulSoup
from gramformer import Gramformer
import pandas as pd
import torch
import math
import re

class GramformerDemo:

    def __init__(self):
        self.model_map = {
            'Corrector': 1,
            'Detector - coming soon': 2
            }
        self.examples = [
            "what be the reason for everyone leave the company",
            "He are moving here.",
            "I am doing fine. How is you?",
            "How is they?",
            "Matt like fish",
            "the collection of letters was original used by the ancient Romans",
            "We enjoys horror movies",
            "Anna and Mike is going skiing",
            "I walk to the store and I bought milk",
            " We all eat the fish and then made dessert",
            "I will eat fish for dinner and drink milk",
            ]
        self.gf = self.load_gf(1)  # Load the Gramformer model

    def load_gf(self, model: int):
        """
        Load Gramformer model
        """
        gf = Gramformer(models=model, use_gpu=False)
        return gf

    def correct_text(self, input_text: str):
        """
        Correct the input text using Gramformer model
        """
        results = self.gf.correct(input_text)
        corrected_sentence, _ = results[0]
        return corrected_sentence
