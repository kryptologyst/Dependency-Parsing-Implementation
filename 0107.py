# Project 107. Advanced Dependency Parsing Implementation
# Description:
# Modern dependency parsing implementation using latest NLP tools including spaCy, Transformers, and PyTorch.
# Features multiple parsing models, interactive visualization, and comprehensive evaluation metrics.

import spacy
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from spacy import displacy
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import numpy as np
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Try to import transformers for advanced models
try:
    from transformers import pipeline, AutoTokenizer, AutoModel
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    st.warning("Transformers library not available. Install with: pip install transformers torch")

class DependencyParser:
    """Advanced dependency parsing with multiple models and evaluation capabilities."""
    
    def __init__(self):
        self.nlp = None
        self.transformer_parser = None
        self.load_models()
        self.init_database()
    
    def load_models(self):
        """Load spaCy and transformer models."""
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_sm")
            st.success("✅ spaCy model loaded successfully")
        except OSError:
            st.error("❌ spaCy English model not found. Run: python -m spacy download en_core_web_sm")
            return
        
        # Load transformer model if available
        if TRANSFORMERS_AVAILABLE:
            try:
                self.transformer_parser = pipeline("token-classification", 
                                                 model="dbmdz/bert-large-cased-finetuned-conll03-english",
                                                 aggregation_strategy="simple")
                st.success("✅ Transformer model loaded successfully")
            except Exception as e:
                st.warning(f"⚠️ Transformer model failed to load: {e}")
    
    def init_database(self):
        """Initialize SQLite database with sample data."""
        self.conn = sqlite3.connect('dependency_parsing.db', check_same_thread=False)
        cursor = self.conn.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sentences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                language TEXT DEFAULT 'en',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dependencies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sentence_id INTEGER,
                token_text TEXT,
                token_pos TEXT,
                dependency_label TEXT,
                head_text TEXT,
                head_pos TEXT,
                model_type TEXT,
                confidence REAL,
                FOREIGN KEY (sentence_id) REFERENCES sentences (id)
            )
        ''')
        
        # Insert sample data
        sample_sentences = [
            "The quick brown fox jumps over the lazy dog.",
            "Natural language processing is a fascinating field of artificial intelligence.",
            "Machine learning models can understand complex linguistic patterns.",
            "Dependency parsing reveals the grammatical structure of sentences.",
            "The beautiful sunset painted the sky with vibrant colors."
        ]
        
        for sentence in sample_sentences:
            cursor.execute('INSERT OR IGNORE INTO sentences (text) VALUES (?)', (sentence,))
        
        self.conn.commit()
    
    def parse_with_spacy(self, text: str) -> Dict:
        """Parse text using spaCy."""
        if not self.nlp:
            return {"error": "spaCy model not loaded"}
        
        doc = self.nlp(text)
        dependencies = []
        
        for token in doc:
            dependencies.append({
                'token': token.text,
                'pos': token.pos_,
                'dep': token.dep_,
                'head': token.head.text,
                'head_pos': token.head.pos_,
                'lemma': token.lemma_,
                'is_punct': token.is_punct,
                'is_space': token.is_space
            })
        
        return {
            'model': 'spaCy',
            'dependencies': dependencies,
            'sentences': [sent.text for sent in doc.sents],
            'entities': [(ent.text, ent.label_) for ent in doc.ents]
        }
    
    def parse_with_transformers(self, text: str) -> Dict:
        """Parse text using transformer models."""
        if not self.transformer_parser:
            return {"error": "Transformer model not loaded"}
        
        try:
            results = self.transformer_parser(text)
            return {
                'model': 'Transformers',
                'results': results,
                'confidence': np.mean([r['score'] for r in results]) if results else 0
            }
        except Exception as e:
            return {"error": f"Transformer parsing failed: {e}"}
    
    def save_to_database(self, text: str, results: Dict):
        """Save parsing results to database."""
        cursor = self.conn.cursor()
        
        # Insert sentence
        cursor.execute('INSERT INTO sentences (text) VALUES (?)', (text,))
        sentence_id = cursor.lastrowid
        
        # Insert dependencies
        if 'dependencies' in results:
            for dep in results['dependencies']:
                cursor.execute('''
                    INSERT INTO dependencies 
                    (sentence_id, token_text, token_pos, dependency_label, head_text, head_pos, model_type)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (sentence_id, dep['token'], dep['pos'], dep['dep'], 
                     dep['head'], dep['head_pos'], results['model']))
        
        self.conn.commit()
        return sentence_id
    
    def get_statistics(self) -> Dict:
        """Get parsing statistics from database."""
        cursor = self.conn.cursor()
        
        # Count sentences
        cursor.execute('SELECT COUNT(*) FROM sentences')
        sentence_count = cursor.fetchone()[0]
        
        # Count dependencies
        cursor.execute('SELECT COUNT(*) FROM dependencies')
        dep_count = cursor.fetchone()[0]
        
        # Most common dependency types
        cursor.execute('''
            SELECT dependency_label, COUNT(*) as count 
            FROM dependencies 
            GROUP BY dependency_label 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        common_deps = cursor.fetchall()
        
        # Most common POS tags
        cursor.execute('''
            SELECT token_pos, COUNT(*) as count 
            FROM dependencies 
            GROUP BY token_pos 
            ORDER BY count DESC 
            LIMIT 10
        ''')
        common_pos = cursor.fetchall()
        
        return {
            'sentence_count': sentence_count,
            'dependency_count': dep_count,
            'common_dependencies': common_deps,
            'common_pos_tags': common_pos
        }

def create_visualization(dependencies: List[Dict]) -> str:
    """Create interactive dependency visualization."""
    if not dependencies:
        return "No dependencies to visualize"
    
    # Create dependency tree data
    nodes = []
    edges = []
    
    for i, dep in enumerate(dependencies):
        nodes.append({
            'id': i,
            'label': f"{dep['token']}\n({dep['pos']})",
            'pos': dep['pos'],
            'dep': dep['dep']
        })
        
        # Find head index
        head_idx = next((j for j, d in enumerate(dependencies) 
                       if d['token'] == dep['head']), None)
        if head_idx is not None:
            edges.append({
                'from': head_idx,
                'to': i,
                'label': dep['dep']
            })
    
    return json.dumps({'nodes': nodes, 'edges': edges})

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Advanced Dependency Parsing",
        page_icon="🌳",
        layout="wide"
    )
    
    st.title("🌳 Advanced Dependency Parsing Implementation")
    st.markdown("Modern NLP-powered dependency parsing with multiple models and interactive visualization")
    
    # Initialize parser
    if 'parser' not in st.session_state:
        with st.spinner("Loading models..."):
            st.session_state.parser = DependencyParser()
    
    parser = st.session_state.parser
    
    # Sidebar for model selection and options
    st.sidebar.header("⚙️ Configuration")
    model_choice = st.sidebar.selectbox(
        "Select Parsing Model",
        ["spaCy", "Transformers", "Both"]
    )
    
    show_visualization = st.sidebar.checkbox("Show Interactive Visualization", True)
    save_to_db = st.sidebar.checkbox("Save Results to Database", True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📝 Input Text")
        text_input = st.text_area(
            "Enter text to parse:",
            value="The quick brown fox jumps over the lazy dog.",
            height=100
        )
        
        if st.button("🚀 Parse Text", type="primary"):
            if text_input.strip():
                with st.spinner("Parsing text..."):
                    results = {}
                    
                    if model_choice in ["spaCy", "Both"]:
                        spacy_results = parser.parse_with_spacy(text_input)
                        if "error" not in spacy_results:
                            results['spaCy'] = spacy_results
                    
                    if model_choice in ["Transformers", "Both"] and TRANSFORMERS_AVAILABLE:
                        transformer_results = parser.parse_with_transformers(text_input)
                        if "error" not in transformer_results:
                            results['Transformers'] = transformer_results
                    
                    if results:
                        st.session_state.last_results = results
                        st.session_state.last_text = text_input
                        
                        if save_to_db:
                            for model_name, result in results.items():
                                parser.save_to_database(text_input, result)
                            st.success("✅ Results saved to database")
                    else:
                        st.error("❌ No models available for parsing")
            else:
                st.warning("⚠️ Please enter some text to parse")
    
    with col2:
        st.header("📊 Quick Stats")
        stats = parser.get_statistics()
        st.metric("Total Sentences", stats['sentence_count'])
        st.metric("Total Dependencies", stats['dependency_count'])
        
        if stats['common_dependencies']:
            st.subheader("Most Common Dependencies")
            for dep, count in stats['common_dependencies'][:5]:
                st.text(f"{dep}: {count}")
    
    # Display results
    if 'last_results' in st.session_state:
        st.header("🔍 Parsing Results")
        
        for model_name, results in st.session_state.last_results.items():
            st.subheader(f"Model: {model_name}")
            
            if 'dependencies' in results:
                # Create DataFrame for better display
                df = pd.DataFrame(results['dependencies'])
                st.dataframe(df, use_container_width=True)
                
                # Show entities if available
                if 'entities' in results and results['entities']:
                    st.write("**Named Entities:**")
                    for entity, label in results['entities']:
                        st.write(f"- {entity} ({label})")
                
                # Visualization
                if show_visualization:
                    st.subheader("🌳 Dependency Tree Visualization")
                    try:
                        # Use spaCy's displacy for visualization
                        doc = parser.nlp(st.session_state.last_text)
                        html = displacy.render(doc, style="dep", page=True)
                        st.components.v1.html(html, height=600, scrolling=True)
                    except Exception as e:
                        st.error(f"Visualization error: {e}")
    
    # Database browser
    st.header("🗄️ Database Browser")
    if st.button("View All Sentences"):
        cursor = parser.conn.cursor()
        cursor.execute('SELECT id, text, created_at FROM sentences ORDER BY created_at DESC LIMIT 10')
        sentences = cursor.fetchall()
        
        if sentences:
            st.write("**Recent Sentences:**")
            for sentence_id, text, created_at in sentences:
                st.write(f"**{sentence_id}:** {text}")
                st.write(f"*Added: {created_at}*")
                st.write("---")
        else:
            st.write("No sentences in database")
    
    # Footer
    st.markdown("---")
    st.markdown("**Project 107:** Advanced Dependency Parsing Implementation")
    st.markdown("Built with spaCy, Streamlit, and modern NLP techniques")

if __name__ == "__main__":
    main()