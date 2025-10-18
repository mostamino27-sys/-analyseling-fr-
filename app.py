from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

# 🔑 قراءة المفتاح من Environment Variable
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')

if not OPENROUTER_API_KEY:
    print("❌ OPENROUTER_API_KEY not found in environment variables!")

# تكوين OpenAI client للاتصال بـ OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "https://analyseling-fr.up.railway.app",
        "X-Title": "AnalyseLingFR"
    }
)

MODEL = 'deepseek/deepseek-r1:free'

@app.route('/')
def index():
    """صفحة البداية"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """تحليل النص"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texte requis'}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({'error': 'Clé API non configurée'}), 500
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en linguistique française."
                },
                {
                    "role": "user",
                    "content": f"""Analyse détaillée de ce texte français:

1. Thème principal
2. Ton et style d'écriture
3. Richesse du vocabulaire
4. Structure et cohérence
5. Points forts
6. Suggestions d'amélioration
7. Niveau de langue

Texte:
{text}

Fournis une analyse structurée en français."""
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f"Erreur analyse: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/plagiarism', methods=['POST'])
def check_plagiarism():
    """كشف السرقة الأدبية"""
    try:
        data = request.get_json()
        text1 = data.get('text1', '')
        text2 = data.get('text2', '')
        
        if not text1 or not text2:
            return jsonify({'error': 'Deux textes requis'}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({'error': 'Clé API non configurée'}), 500
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en détection de plagiat."
                },
                {
                    "role": "user",
                    "content": f"""Compare ces deux textes français:

Texte 1:
{text1}

Texte 2:
{text2}

Fournis:
1. Score de similarité (0-100%)
2. Similitudes détectées
3. Passages similaires
4. Conclusion sur plagiat

Analyse en français."""
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f"Erreur plagiat: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/improve', methods=['POST'])
def improve_text():
    """تحسين النص"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texte requis'}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({'error': 'Clé API non configurée'}), 500
        
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un expert en amélioration de textes français."
                },
                {
                    "role": "user",
                    "content": f"""Améliore ce texte français:

{text}

Instructions:
1. Corrige les erreurs
2. Enrichis le vocabulaire
3. Améliore la structure
4. Garde le sens original

Format:
📝 TEXTE AMÉLIORÉ:
[texte]

✨ AMÉLIORATIONS:
[liste]"""
                }
            ],
            max_tokens=2000,
            temperature=0.7
        )
        
        result = response.choices[0].message.content
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f"Erreur amélioration: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 AnalyseLingFR started on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
