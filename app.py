import streamlit
from annotated_text import annotated_text
import spacy

annotated_text(
    "This ",
    ("is", "verb"),
    " some ",
    ("annotated", "adj"),
    ("text", "noun"),
    " for those of ",
    ("you", "pronoun"),
    " who ",
    ("like", "verb"),
    " this sort of ",
    ("thing", "noun"),
    "."
)


