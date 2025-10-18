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
            error_text = response.text
            raise Exception(f'Erreur API {response.status_code}: {error_text}')
        
        data = response.json()
        return data['choices'][0]['message']['content']
        
    except requests.exceptions.Timeout:
        raise Exception('⏱️ Délai d\'attente dépassé. Réessayez.')
    except requests.exceptions.RequestException as e:
        raise Exception(f'❌ Erreur de connexion: {str(e)}')
    except Exception as e:
        raise Exception(f'Erreur: {str(e)}')

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
                'content': 'Tu es un expert en linguistique française spécialisé dans l\'analyse de textes.'
            },
            {
                'role': 'user',
                'content': f"""Analyse ce texte français de manière détaillée:

**Texte:**
{text}

**Fournis une analyse structurée:**

1. **Thème principal**: Identifie le sujet central
2. **Ton et style**: Caractérise le ton (formel, informel, neutre, lyrique...)
3. **Richesse du vocabulaire**: Évalue la diversité lexicale et le niveau de langue
4. **Structure et cohérence**: Analyse l'organisation du texte
5. **Points forts**: Mets en valeur les qualités linguistiques
6. **Suggestions d'amélioration**: Propose des améliorations concrètes
7. **Niveau de langue**: Détermine le registre (familier, courant, soutenu, académique)

Réponds en français de manière claire et professionnelle."""
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
                'content': 'Tu es un expert en détection de plagiat et analyse comparative de textes.'
            },
            {
                'role': 'user',
                'content': f"""Compare ces deux textes français et détecte les similitudes:

**Texte 1:**
{text1}

**Texte 2:**
{text2}

**Analyse:**

1. **Score de similarité**: Pourcentage précis (0-100%)
2. **Similitudes lexicales**: Mots et expressions identiques ou similaires
3. **Similitudes structurelles**: Structure des phrases et paragraphes
4. **Passages similaires**: Cite les passages qui se ressemblent
5. **Différences notables**: Relève les différences significatives
6. **Conclusion**: Niveau de plagiat (Faible/Modéré/Élevé/Critique)

Sois précis et objectif. Réponds en français."""
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
                'content': 'Tu es un expert en correction et amélioration de textes français.'
            },
            {
                'role': 'user',
                'content': f"""Améliore ce texte français:

**Texte original:**
{text}

**Instructions:**
1. Corrige toutes les erreurs (grammaire, orthographe, conjugaison)
2. Enrichis le vocabulaire avec des synonymes appropriés
3. Améliore la structure et la fluidité
4. Respecte le sens original
5. Adapte le niveau de langue de manière cohérente

**Format:**

📝 **TEXTE AMÉLIORÉ:**
[Texte corrigé complet]

✨ **AMÉLIORATIONS APPORTÉES:**
[Liste détaillée des corrections et améliorations]

📊 **STATISTIQUES:**
[Nombre de corrections]

Réponds en français de manière structurée."""
            }
        ])
        
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f'Erreur amélioration: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'api_configured': bool(OPENROUTER_API_KEY),
        'model': MODEL
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('=' * 60)
    print('🚀 AnalyseLingFR Starting...')
    print('🤖 Powered by DeepSeek AI via OpenRouter')
    print(f'📡 Port: {port}')
    print(f'🔑 API Key: {"✅ Configured" if OPENROUTER_API_KEY else "❌ Missing"}')
    print('=' * 60)
    app.run(host='0.0.0.0', port=port, debug=False)
