from flask import Flask, render_template, request
from model import SpellCheckerModule

app = Flask(__name__)
spell_checker = SpellCheckerModule()

@app.route("/", methods=["GET", "POST"])
def index():
    corrected_spelling = ""
    grammar_result = None
    original_text = ""

    if request.method == "POST":
        original_text = request.form.get("text_input", "")

        # Handle uploaded file
        uploaded_file = request.files.get("file_input")
        if uploaded_file and uploaded_file.filename.endswith(".txt"):
            file_content = uploaded_file.read().decode("utf-8")
            original_text = file_content

        if original_text.strip():
            corrected_spelling = spell_checker.correct_spell(original_text)
            grammar_result = spell_checker.check_grammar(corrected_spelling)

    return render_template(
        "index.html",
        original_text=original_text,
        corrected_spelling=corrected_spelling,
        grammar_result=grammar_result,
    )

if __name__ == "__main__":
    app.run(debug=True)
