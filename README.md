# AI Investment Research Platform

## Overview

This project is an AI-powered investment research assistant designed to help users perform advanced financial analysis, retrieve relevant market data, and generate actionable investment insights. The system leverages state-of-the-art language models, retrieval-augmented generation (RAG), and custom tool integrations to answer complex investment queries, suggest next research steps, and validate user input for relevance to investment research.

The platform features:
- **Natural language query validation** to ensure user questions are investment-related.
- **Retrieval-augmented generation (RAG)** using a FAISS vector database and HuggingFace embeddings for context-aware responses.
- **Multi-agent workflow** for validation, information retrieval, analysis, and next-step suggestions.
- **Integration with advanced LLMs** (Anthropic Claude, OpenAI, HuggingFace) for high-quality, context-rich answers.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/heraldpark15/Investment-Research-AI.git
cd Investment-Research-AI
```

### 2. Set Up Python Environment

It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

Make sure you have the following in your `requirements.txt` (or install manually if not):
- `langchain`
- `langchain-community`
- `langchain-openai`
- `langchain-anthropic`
- `langchain-huggingface`
- `faiss-cpu`
- `python-dotenv`
- `openai`
- `anthropic`
- `transformers`
- `torch`

### 4. Set Up Environment Variables

Create a `.env` file in the project root with your API keys:

OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

### 5. Prepare the RAG Database

Ensure you have a FAISS index and embedding database at the path specified in your code (e.g., `RAG/rag_database`). You may need to build this index using your own data and the appropriate embedding model.

---

## Made With

- **Python 3.11+**
- **LangChain**: Orchestrates LLMs, tools, and workflows.
- **FAISS**: Fast vector similarity search for retrieval-augmented generation.
- **HuggingFace Transformers**: For generating embeddings (`all-MiniLM-L6-v2`).
- **OpenAI & Anthropic APIs**: For advanced language model capabilities.
- **Django**
- **React**
- **JavaScript**
- **Chakra UI**

---

## Usage

1. **Start the Backend**
   - Run your backend server (e.g., Django or Flask) as per your project setup.

2. **Start the Frontend**
   - If you have a React frontend, navigate to the frontend directory and run:
     ```bash
     npm install
     npm start
     ```
   - The frontend will be available at `http://localhost:3000`.

3. **Interact with the Assistant**
   - Enter investment research queries in natural language.
   - The assistant will validate, retrieve, analyze, and suggest next steps for your research.


---

## License

MIT License

---

## Acknowledgements

- [LangChain](https://github.com/langchain-ai/langchain)
- [FAISS](https://github.com/facebookresearch/faiss)
- [HuggingFace](https://huggingface.co/)
- [Anthropic](https://www.anthropic.com/)
- [OpenAI](https://openai.com/)

---

*For questions or contributions, please open an issue or pull request on GitHub!*
