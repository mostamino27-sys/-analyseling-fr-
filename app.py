from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# قراءة المفتاح من Environment Variable
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'meta-llama/llama-3.2-3b-instruct:free'  # ✅ Llama 3.2!

def call_ai(messages):
    """استدعاء Llama 3.2 عبر OpenRouter API"""
    if not OPENROUTER_API_KEY:
        raise Exception('⚠️ Clé API OpenRouter non configurée')
    
    try:
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
            timeout=60
        )
        
        if response.status_code != 200:
            error_data = response.json()
            error_msg = error_data.get('error', {}).get('message', 'Erreur inconnue')
            raise Exception(f'Erreur API {response.status_code}: {error_msg}')
        
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except requests.exceptions.Timeout:
        raise Exception('⏱️ Délai d\'attente dépassé. Veuillez réessayer.')
    except requests.exceptions.RequestException as e:
        raise Exception(f'❌ Erreur de connexion: {str(e)}')
    except Exception as e:
        raise Exception(str(e))

@app.route('/')
def index():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_text():
    """تحليل النص اللغوي"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Texte requis', 'success': False}), 400
        
        result = call_ai([
            {
                'role': 'system',
                'content': 'Tu es un expert linguiste français spécialisé dans l\'analyse détaillée de textes. Réponds toujours en français de manière structurée et professionnelle.'
            },
            {
                'role': 'user',
                'content': f"""Analyse ce texte français en profondeur:

**Texte:**
{text}

**Fournis une analyse complète avec ces sections:**

1. **Thème principal**: Identifie le sujet central et les thèmes secondaires
2. **Ton et style**: Caractérise le ton (formel, informel, neutre, lyrique, satirique...)
3. **Richesse du vocabulaire**: Évalue la diversité lexicale, les champs sémantiques, et le registre
4. **Structure et cohérence**: Analyse l'organisation, les connecteurs logiques, et la progression
5. **Points forts**: Mets en valeur les qualités linguistiques et stylistiques
6. **Suggestions d'amélioration**: Propose des améliorations concrètes et constructives
7. **Niveau de langue**: Détermine le registre linguistique (familier, courant, soutenu, académique)

Réponds en français avec clarté et précision professionnelle."""
            }
        ])
        
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f'Erreur analyse: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/plagiarism', methods=['POST'])
def check_plagiarism():
    """
