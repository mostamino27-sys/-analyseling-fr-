from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'deepseek/deepseek-r1:free'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'Texte requis'}), 400
        
        if not OPENROUTER_API_KEY:
            return jsonify({'error': 'Clé API non configurée'}), 500
        
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
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Tu es un expert en linguistique française.'
                    },
                    {
                        'role': 'user',
                        'content': f"""Analyse détaillée de ce texte français:

1. Thème principal
2. Ton et style
3. Richesse du vocabulaire
4. Structure
5. Points forts
6. Suggestions
7. Niveau de langue

Texte:
{text}"""
                    }
                ]
            }
        )
        
        result = response.json()
        return jsonify({'result': result['choices'][0]['message']['content'], 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/plagiarism', methods=['POST'])
def check_plagiarism():
    try:
        data = request.get_json()
        text1 = data.get('text1', '')
        text2 = data.get('text2', '')
        
        response = requests.post(
            API_URL,
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Expert en détection de plagiat.'
                    },
                    {
                        'role': 'user',
                        'content': f"Compare:\nTexte 1: {text1}\nTexte 2: {text2}"
                    }
                ]
            }
        )
        
        result = response.json()
        return jsonify({'result': result['choices'][0]['message']['content'], 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/improve', methods=['POST'])
def improve_text():
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        response = requests.post(
            API_URL,
            headers={
                'Authorization': f'Bearer {OPENROUTER_API_KEY}',
                'Content-Type': 'application/json'
            },
            json={
                'model': MODEL,
                'messages': [
                    {
                        'role': 'system',
                        'content': 'Expert en amélioration de textes français.'
                    },
                    {
                        'role': 'user',
                        'content': f"Améliore ce texte:\n{text}"
                    }
                ]
            }
        )
        
        result = response.json()
        return jsonify({'result': result['choices'][0]['message']['content'], 'success': True})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 AnalyseLingFR started")
    app.run(host='0.0.0.0', port=port)
