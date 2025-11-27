from textblob import TextBlob
import spacy

class SpellCheckerModule:
    def __init__(self):
        # Load spaCy English model
        self.nlp = spacy.load("en_core_web_sm")

    def correct_spell(self, text):
        """
        Correct spelling errors using TextBlob
        """
        words = text.split()
        corrected_words = []
        for word in words:
            corrected_word = str(TextBlob(word).correct())
            corrected_words.append(corrected_word)
        return " ".join(corrected_words)

    def check_grammar(self, text):
        """
        Basic grammar checks using spaCy rules
        """
        doc = self.nlp(text)
        mistakes = []
        corrected_text = text

        # Rule 1: Capitalization
        for sent in doc.sents:
            first_token = sent[0]
            if first_token.is_lower:
                mistakes.append({
                    "rule": "Capitalization",
                    "message": f"Sentence should start with a capital letter: '{first_token.text}'"
                })
                corrected_text = corrected_text.replace(first_token.text, first_token.text.capitalize(), 1)

        # Rule 2: Subject-Verb agreement (simple heuristic)
        for token in doc:
            if token.pos_ == "VERB":
                subj = [w for w in token.lefts if w.dep_ in ("nsubj", "nsubjpass")]
                if subj:
                    subj = subj[0]
                    if subj.tag_ == "NN" and token.tag_ == "VBP":
                        mistakes.append({
                            "rule": "Subject-Verb Agreement",
                            "message": f"Singular subject '{subj.text}' with plural verb '{token.text}'"
                        })
                    elif subj.tag_ == "NNS" and token.tag_ == "VBZ":
                        mistakes.append({
                            "rule": "Subject-Verb Agreement",
                            "message": f"Plural subject '{subj.text}' with singular verb '{token.text}'"
                        })

        # Rule 3: Missing punctuation
        if not text.strip().endswith(('.', '!', '?')):
            mistakes.append({
                "rule": "Punctuation",
                "message": "Sentence should end with punctuation (. ! ?)"
            })
            corrected_text += '.'

        # Rule 4: Double spaces
        if "  " in text:
            mistakes.append({
                "rule": "Formatting",
                "message": "Extra spaces detected"
            })
            corrected_text = corrected_text.replace("  ", " ")

        return {
            "corrected_text": corrected_text,
            "mistakes": mistakes,
            "count": len(mistakes)
        }
