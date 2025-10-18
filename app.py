from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# قراءة المفتاح من Environment Variable
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')

# تكوين Google AI
if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

def call_ai(prompt):
    """استدعاء Google Gemini API"""
    if not GOOGLE_API_KEY or not model:
        raise Exception('⚠️ Clé API Google non configurée')
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f'Erreur Google AI: {str(e)}')

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
        
        prompt = f"""Tu es un expert en linguistique française. Analyse ce texte en détail:

**Texte à analyser:**
{text}

**Fournis une analyse structurée:**
1. **Thème principal**: Identifie le sujet central
2. **Ton et style**: Caractérise le ton (formel, informel, neutre...)
3. **Richesse du vocabulaire**: Évalue la diversité lexicale
4. **Structure et cohérence**: Analyse l'organisation
5. **Points forts**: Mets en valeur les qualités
6. **Suggestions d'amélioration**: Propose des améliorations concrètes
7. **Niveau de langue**: Détermine le registre (familier, courant, soutenu, académique)

Réponds en français de manière claire et professionnelle."""

        result = call_ai(prompt)
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
        
        prompt = f"""Tu es un expert en détection de plagiat. Compare ces deux textes français:

**Texte 1:**
{text1}

**Texte 2:**
{text2}

**Fournis une analyse complète:**
1. **Score de similarité**: Donne un pourcentage (0-100%)
2. **Similitudes lexicales**: Identifie les mots et expressions identiques
3. **Similitudes structurelles**: Compare la structure des phrases
4. **Passages similaires**: Cite les passages qui se ressemblent
5. **Différences notables**: Relève les différences significatives
6. **Conclusion**: Détermine le risque de plagiat (Faible/Modéré/Élevé/Critique)

Réponds en français de manière objective et détaillée."""

        result = call_ai(prompt)
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
        
        prompt = f"""Tu es un expert en amélioration de textes français. Améliore ce texte:

**Texte original:**
{text}

**Instructions:**
1. Corrige toutes les erreurs grammaticales et orthographiques
2. Enrichis le vocabulaire avec des synonymes appropriés
3. Améliore la structure et la fluidité des phrases
4. Respecte le sens et l'intention originale
5. Adapte le niveau de langue de manière cohérente

**Format de réponse:**

📝 **TEXTE AMÉLIORÉ:**
[Écris ici le texte corrigé et amélioré complet]

✨ **PRINCIPALES AMÉLIORATIONS:**
[Liste les améliorations apportées avec explications]

📊 **STATISTIQUES:**
[Nombre de corrections effectuées]

Réponds en français."""

        result = call_ai(prompt)
        return jsonify({'result': result, 'success': True})
        
    except Exception as e:
        print(f'Erreur amélioration: {str(e)}')
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health')
def health():
    """Health check"""
    return jsonify({
        'status': 'ok',
        'api_configured': bool(GOOGLE_API_KEY),
        'model': 'gemini-1.5-flash'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print('=' * 50)
    print('🚀 AnalyseLingFR Starting...')
    print('🤖 Powered by Google Gemini AI')
    print(f'📡 Port: {port}')
    print(f'🔑 Google API: {"✅ Configured" if GOOGLE_API_KEY else "❌ Missing"}')
    print('=' * 50)
    app.run(host='0.0.0.0', port=port, debug=False)
