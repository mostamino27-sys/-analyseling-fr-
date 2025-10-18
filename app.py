from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# قراءة المفتاح من Environment Variable
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'deepseek/deepseek-r1:free'

def call_ai(messages):
    """استدعاء OpenRouter API"""
    if not OPENROUTER_API_KEY:
        raise Exception('Clé API non configurée')

    response = requests.post(
        API_URL,
        headers={
            'Authorization': f'Bearer {OPENROUTER_API_KEY}',
            'Content-Type': 'application/json',
            'HTTP-Referer': 'https://analyseling-fr.up.railway.app',
            'X-Title': 'AnalyseLingFR'
        },
        json={
            'model': MODEL,
            'messages': messages,
            'max_tokens': 2000,
            'temperature': 0.7
        },
        timeout=30
    )

    if response.status_code != 200:
        raise Exception(f'Erreur API: {response.status_code}')

    data = response.json()
    return data['choices'][0]['message']['content']

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """تحليل النص"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()

        if not text:
            return jsonify({'error': 'Texte requis', 'success': False}), 400

        result = call_ai([
            {
                'role': 'system',
                'content': 'Tu es un expert en linguistique française. Tu analyses les textes avec précision.'
            },
            {
                'role': 'user',
                'content': f"""Analyse linguistique détaillée de ce texte français:

1. **Thème principal**: Identifie le sujet
2. **Ton et style**: Caractérise le ton
3. **Richesse vocabulaire**: Évalue la diversité
4. **Structure**: Analyse l'organisation
5. **Points forts**: Mets en valeur
6. **Suggestions**: Propose des améliorations
7. **Niveau de langue**: Détermine le registre

Texte à analyser:
{text}

Fournis une analyse structurée en français."""
            }
        ])

        return jsonify({'result': result, 'success': True})

    except Exception as e:
        print(f'Erreur analyse: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/plagiarism', methods=['POST'])
def check_plagiarism():
    """كشف السرقة الأدبية"""
    try:
        data = request.get_json()
        text1 = data.get('text1', '').strip()
        text2 = data.get('text2', '').strip()

        if not text1 or not text2:
            return jsonify({'error': 'Deux textes requis', 'success': False}), 400

        result = call_ai([
            {
                'role': 'system',
                'content': 'Tu es un expert en détection de plagiat.'
            },
            {
                'role': 'user',
                'content': f"""Compare ces deux textes français:

**Texte 1:**
{text1}

**Texte 2:**
{text2}

Fournis:
1. Score de similarité (0-100%)
2. Similitudes détectées
3. Passages similaires
4. Conclusion sur plagiat

Analyse en français."""
            }
        ])

        return jsonify({'result': result, 'success': True})

    except Exception as e:
        print(f'Erreur plagiat: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/improve', methods=['POST'])
def improve_text():
    """تحسين النص"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()

        if not text:
            return jsonify({'error': 'Texte requis', 'success': False}), 400

        result = call_ai([
            {
                'role': 'system',
                'content': 'Tu es un expert en amélioration de textes français.'
            },
            {
                'role': 'user',
                'content': f"""Améliore ce texte français:

**Texte original:**
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
        ])

        return jsonify({'result': result, 'success': True})

    except Exception as e:
        print(f'Erreur amélioration: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'api_configured': bool(OPENROUTER_API_KEY)
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('=' * 50)
    print('🚀 AnalyseLingFR Starting...')
    print(f'📡 Port: {port}')
    print(f'🔑 API Key: {"✅ Configured" if OPENROUTER_API_KEY else "❌ Missing"}')
    print('=' * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
