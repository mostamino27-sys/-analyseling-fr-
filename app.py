from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import requests

app = Flask(__name__)
CORS(app)

# قراءة المفتاح من Environment Variable
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
API_URL = 'https://openrouter.ai/api/v1/chat/completions'
MODEL = 'meta-llama/llama-3.2-3b-instruct:free'

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
    """كشف السرقة الأدبية والمقارنة"""
    try:
        data = request.get_json()
        text1 = data.get('text1', '').strip()
        text2 = data.get('text2', '').strip()
        
        if not text1 or not text2:
            return jsonify({'error': 'Deux textes requis', 'success': False}), 400
        
        result = call_ai([
            {
                'role': 'system',
                'content': 'Tu es un expert en détection de plagiat et analyse comparative de textes. Tu identifies les similitudes avec précision et objectivité.'
            },
            {
                'role': 'user',
                'content': f"""Compare ces deux textes français et analyse leurs similitudes:

**Texte 1:**
{text1}

**Texte 2:**
{text2}

**Analyse détaillée:**

1. **Score de similarité**: Donne un pourcentage précis (0-100%) avec justification
2. **Similitudes lexicales**: Liste les mots, expressions et phrases identiques ou très similaires
3. **Similitudes structurelles**: Compare la structure syntaxique, les schémas de phrases, et l'organisation
4. **Passages problématiques**: Cite les passages qui présentent des similitudes suspectes
5. **Différences notables**: Relève les différences significatives dans le style et le contenu
6. **Analyse du contexte**: Évalue si les similitudes peuvent être naturelles ou intentionnelles
7. **Conclusion finale**: Détermine le niveau de plagiat (Aucun/Faible/Modéré/Élevé/Critique)

Sois précis, objectif et professionnel. Réponds en français."""
            }
        ])
        
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f'Erreur plagiat: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/improve', methods=['POST'])
def improve_text():
    """تحسين وتصحيح النص"""
    try:
        data = request.get_json()
        text = data.get('text', '').strip()
        
        if not text:
            return jsonify({'error': 'Texte requis', 'success': False}), 400
        
        result = call_ai([
            {
                'role': 'system',
                'content': 'Tu es un expert correcteur et rédacteur français. Tu améliores les textes tout en préservant leur sens original.'
            },
            {
                'role': 'user',
                'content': f"""Améliore ce texte français de manière complète:

**Texte original:**
{text}

**Instructions détaillées:**
1. Corrige toutes les erreurs grammaticales, orthographiques, et de conjugaison
2. Enrichis le vocabulaire avec des synonymes appropriés et variés
3. Améliore la structure des phrases pour plus de fluidité et d'élégance
4. Renforce la cohérence et les transitions entre les idées
5. Respecte absolument le sens et l'intention originale du texte
6. Adapte le niveau de langue de manière cohérente et appropriée

**Format de réponse obligatoire:**

📝 **TEXTE AMÉLIORÉ:**
[Écris ici le texte entièrement corrigé et amélioré]

✨ **AMÉLIORATIONS PRINCIPALES:**
[Liste détaillée et numérotée des corrections et améliorations apportées avec explications]

📊 **STATISTIQUES:**
[Nombre total de corrections grammaticales, enrichissements lexicaux, améliorations structurelles]

💡 **RECOMMANDATIONS:**
[Conseils pour améliorer davantage la qualité rédactionnelle]

Réponds en français de manière structurée et professionnelle."""
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
        'model': MODEL,
        'provider': 'OpenRouter + Meta Llama 3.2'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('=' * 70)
    print('🚀 AnalyseLingFR Starting...')
    print('🤖 Powered by Advanced Linguistic Algorithms')
    print(f'📡 Port: {port}')
    print(f'🔑 API: {"✅ OK" if OPENROUTER_API_KEY else "❌ Missing"}')
    print('=' * 70)
    app.run(host='0.0.0.0', port=port, debug=False)
