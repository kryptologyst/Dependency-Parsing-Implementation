# Advanced Dependency Parsing Implementation

A modern, comprehensive dependency parsing implementation featuring multiple NLP models, interactive visualization, and database integration.

## Features

- **Multiple Parsing Models**: spaCy and Transformer-based models
- **Interactive Web UI**: Built with Streamlit for easy interaction
- **Database Integration**: SQLite database for storing and analyzing results
- **Advanced Visualization**: Interactive dependency trees and statistics
- **Comprehensive Analysis**: POS tagging, named entity recognition, and dependency statistics
- **Modern NLP Stack**: Latest versions of spaCy, Transformers, and PyTorch

## Prerequisites

- Python 3.8 or higher
- pip package manager

## 🛠️ Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd dependency-parsing-implementation
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Download spaCy English model**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Usage

### Web Interface (Recommended)

Run the Streamlit web application:

```bash
streamlit run 0107.py
```

The application will open in your browser at `http://localhost:8501`

### Features Available:

- **Text Input**: Enter any sentence or paragraph for parsing
- **Model Selection**: Choose between spaCy, Transformers, or both models
- **Interactive Visualization**: View dependency trees with spaCy's displacy
- **Database Browser**: View previously parsed sentences
- **Statistics Dashboard**: See parsing statistics and common patterns

### Command Line Usage

You can also use the parser programmatically:

```python
from 0107 import DependencyParser

# Initialize parser
parser = DependencyParser()

# Parse text
text = "The quick brown fox jumps over the lazy dog."
results = parser.parse_with_spacy(text)

# View results
for dep in results['dependencies']:
    print(f"{dep['token']} -> {dep['head']} ({dep['dep']})")
```

## Database Schema

The application uses SQLite with two main tables:

### Sentences Table
- `id`: Primary key
- `text`: The input text
- `language`: Language code (default: 'en')
- `created_at`: Timestamp

### Dependencies Table
- `id`: Primary key
- `sentence_id`: Foreign key to sentences table
- `token_text`: The token text
- `token_pos`: Part-of-speech tag
- `dependency_label`: Dependency relation label
- `head_text`: Head token text
- `head_pos`: Head token POS tag
- `model_type`: Model used for parsing
- `confidence`: Parsing confidence score

## 🔧 Configuration

### Model Options

1. **spaCy**: Fast, accurate dependency parsing with linguistic features
2. **Transformers**: BERT-based models for advanced NLP tasks
3. **Both**: Compare results from multiple models

### Visualization Options

- Interactive dependency trees
- POS tag distribution charts
- Dependency frequency analysis
- Named entity highlighting

## Performance Metrics

The application tracks various metrics:

- Total sentences parsed
- Total dependencies extracted
- Most common dependency types
- Most common POS tags
- Model performance comparisons

## Testing

Run the test suite:

```bash
pytest tests/
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [spaCy](https://spacy.io/) for excellent NLP tools
- [Hugging Face Transformers](https://huggingface.co/transformers/) for state-of-the-art models
- [Streamlit](https://streamlit.io/) for the web interface
- [Plotly](https://plotly.com/) for interactive visualizations

## Additional Resources

- [spaCy Documentation](https://spacy.io/usage)
- [Universal Dependencies](https://universaldependencies.org/)
- [Transformers Documentation](https://huggingface.co/docs/transformers/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## Troubleshooting

### Common Issues

1. **spaCy model not found**:
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Transformers model loading fails**:
   - Check internet connection
   - Verify PyTorch installation
   - Try a different model

3. **Database errors**:
   - Ensure write permissions in the project directory
   - Check SQLite installation

### Getting Help

- Check the [Issues](https://github.com/kryptologyst/issues) page
- Create a new issue with detailed error information
- Include Python version, OS, and error traceback

## Version History

- **v1.0.0**: Initial release with basic spaCy parsing
- **v2.0.0**: Added Streamlit UI and database integration
- **v3.0.0**: Added Transformer models and advanced visualization
- **v3.1.0**: Enhanced statistics and performance metrics


# Dependency-Parsing-Implementation
