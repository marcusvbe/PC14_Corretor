# app.py
from flask import Flask, request, jsonify, render_template
from corretor import Corretor

app = Flask(__name__)
sc = Corretor(corpus_path="vocab.txt")

# Adicionar rota para página inicial
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/check', methods=['POST'])
def check_text():
    text = request.json['text']
    corrected, changes = sc.correct_sentence(text)
    
    response = {
        'original': text,
        'corrected': corrected,
        'changes': changes,
        'is_correct': len(changes) == 0
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)