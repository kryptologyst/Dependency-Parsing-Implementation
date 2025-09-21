import pytest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from 0107 import DependencyParser

class TestDependencyParser:
    """Test cases for DependencyParser class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.parser = DependencyParser()
        self.test_text = "The quick brown fox jumps over the lazy dog."
    
    def test_spacy_model_loading(self):
        """Test that spaCy model loads correctly."""
        assert self.parser.nlp is not None
    
    def test_spacy_parsing(self):
        """Test spaCy dependency parsing."""
        results = self.parser.parse_with_spacy(self.test_text)
        
        assert "error" not in results
        assert "dependencies" in results
        assert "model" in results
        assert results["model"] == "spaCy"
        
        # Check that we have dependencies
        assert len(results["dependencies"]) > 0
        
        # Check structure of first dependency
        first_dep = results["dependencies"][0]
        required_keys = ["token", "pos", "dep", "head", "head_pos", "lemma"]
        for key in required_keys:
            assert key in first_dep
    
    def test_database_initialization(self):
        """Test database initialization."""
        assert self.parser.conn is not None
        
        # Check that tables exist
        cursor = self.parser.conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        assert "sentences" in tables
        assert "dependencies" in tables
    
    def test_save_to_database(self):
        """Test saving parsing results to database."""
        results = self.parser.parse_with_spacy(self.test_text)
        sentence_id = self.parser.save_to_database(self.test_text, results)
        
        assert sentence_id is not None
        
        # Verify data was saved
        cursor = self.parser.conn.cursor()
        cursor.execute("SELECT text FROM sentences WHERE id = ?", (sentence_id,))
        saved_text = cursor.fetchone()[0]
        assert saved_text == self.test_text
    
    def test_get_statistics(self):
        """Test statistics retrieval."""
        stats = self.parser.get_statistics()
        
        assert "sentence_count" in stats
        assert "dependency_count" in stats
        assert "common_dependencies" in stats
        assert "common_pos_tags" in stats
        
        # All counts should be non-negative
        assert stats["sentence_count"] >= 0
        assert stats["dependency_count"] >= 0
    
    def test_empty_text_handling(self):
        """Test handling of empty text."""
        results = self.parser.parse_with_spacy("")
        
        # Should handle empty text gracefully
        assert "dependencies" in results
        assert len(results["dependencies"]) == 0
    
    def test_punctuation_handling(self):
        """Test handling of punctuation."""
        text_with_punct = "Hello, world! How are you?"
        results = self.parser.parse_with_spacy(text_with_punct)
        
        assert "error" not in results
        assert len(results["dependencies"]) > 0
        
        # Check that punctuation tokens are marked
        punct_tokens = [dep for dep in results["dependencies"] if dep["is_punct"]]
        assert len(punct_tokens) > 0

def test_create_visualization():
    """Test visualization creation."""
    from 0107 import create_visualization
    
    # Test with empty dependencies
    result = create_visualization([])
    assert result == "No dependencies to visualize"
    
    # Test with sample dependencies
    sample_deps = [
        {"token": "The", "pos": "DET", "dep": "det", "head": "fox"},
        {"token": "fox", "pos": "NOUN", "dep": "nsubj", "head": "jumps"}
    ]
    
    result = create_visualization(sample_deps)
    assert isinstance(result, str)
    
    # Should be valid JSON
    import json
    parsed = json.loads(result)
    assert "nodes" in parsed
    assert "edges" in parsed

if __name__ == "__main__":
    pytest.main([__file__])
