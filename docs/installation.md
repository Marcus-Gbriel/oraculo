# Guia de Instalação - Sistema Oráculo

## 📋 Pré-requisitos

### Sistema Operacional
- Windows 10/11 (recomendado)
- Linux (Ubuntu 20.04+, Debian, etc)
- macOS 10.15+

### Software Necessário
- **Python 3.10-3.13** (⚠️ Não use 3.14, ainda não tem suporte)
- pip (gerenciador de pacotes Python)
- 8GB RAM mínimo (16GB recomendado para modelos 13B)
- 10GB espaço em disco (para modelos LLM)

### Opcional (Aceleração GPU)
- GPU NVIDIA com CUDA (RTX série 20XX+)
- CUDA Toolkit 11.8 ou superior
- 6GB+ VRAM recomendado

## 🔧 Instalação Passo a Passo

### Método 1: Instalação Automática (Windows - Recomendado)

```bash
# Execute o instalador automático
execute.bat

# Escolha: 1 - Instalar todas as dependências
```

O script irá:
✅ Criar ambiente virtual automaticamente
✅ Instalar dependências na ordem correta
✅ Validar instalação
✅ Exibir menu de opções

### Método 2: Instalação Manual

#### 1. Verificar Python

```bash
python --version
# Deve mostrar: Python 3.10.x, 3.11.x, 3.12.x ou 3.13.x
```

Se não tiver Python instalado:
- **Windows**: https://python.org/downloads (marque "Add to PATH")
- **Linux**: `sudo apt install python3.13 python3.13-venv python3-pip`
- **macOS**: `brew install python@3.13`

#### 2. Criar Ambiente Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3. Instalar Dependências Core

```bash
pip install --upgrade pip

# Dependências principais (ordem otimizada)
pip install numpy>=1.24.0
pip install PyPDF2>=3.0.0 python-docx>=1.0.0 openpyxl>=3.1.0
pip install sentence-transformers>=2.2.0
pip install chromadb>=0.5.0
pip install gpt4all>=2.0.0
```

#### 4. Modelos LLM (GPT4All)

**🎉 Boa notícia: O sistema usa GPT4All - sem complicações!**

✅ **Vantagens do GPT4All:**
- Download automático na primeira execução
- 100% Python (sem compiladores C++)
- 7 modelos disponíveis para escolha
- Suporte a GPU NVIDIA automático
- Gerenciamento integrado no menu

💾 **Modelos Disponíveis:**

| Modelo | Tamanho | Qualidade | Velocidade | Melhor Para |
|--------|---------|-----------|------------|-------------|
| Mistral 7B OpenOrca | 3.8 GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ | Uso geral (Padrão) |
| Mistral 7B Instruct | 3.8 GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡⚡ | Precisão literal |
| Orca 2 7B | 3.8 GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | Documentos técnicos |
| Nous Hermes 13B | 7.3 GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | Máxima precisão |
| GPT4All Falcon | 3.9 GB | ⭐⭐⭐⭐ | ⚡⚡⚡⚡ | Versatilidade |
| WizardLM 13B | 7.3 GB | ⭐⭐⭐⭐⭐ | ⚡⚡⚡ | Análise complexa |
| Orca Mini 3B | 1.8 GB | ⭐⭐⭐ | ⚡⚡⚡⚡⚡ | PCs fracos |

📝 **Como funciona:**
1. Na primeira execução, o modelo padrão será baixado
2. Use o Menu → Opção 6 para ver modelos disponíveis
3. Use o Menu → Opção 8 para trocar de modelo
4. Reinicie o sistema para aplicar

⚠️ **Espaço necessário:**
- Modelo 7B: ~4 GB
- Modelo 13B: ~8 GB
- Todos os modelos: ~30 GB

#### 5. Verificar Instalação

```bash
# Testar importações
python -c "import PyPDF2, docx, openpyxl, sentence_transformers, chromadb, gpt4all; print('✅ Todas as dependências OK!')"

# Verificar GPU (opcional)
python -c "import torch; print('✅ GPU disponível!' if torch.cuda.is_available() else 'ℹ️ GPU não detectada (usará CPU)')"
```

## 📦 Arquivo requirements.txt

O projeto já inclui `requirements.txt` otimizado:

```txt
numpy>=1.24.0
PyPDF2>=3.0.0
python-docx>=1.0.0
openpyxl>=3.1.0
sentence-transformers>=2.2.0
chromadb>=0.5.0
gpt4all>=2.0.0
torch>=2.0.0  # Opcional, para GPU
```

Instale tudo de uma vez:
```bash
pip install -r requirements.txt
```

⚠️ **Importante:**
- Use versões `>=` para compatibilidade futura
- Python 3.10-3.13 recomendado
- Evite Python 3.14 (muito novo)

## 🚀 Primeira Execução

### 1. Verificar Estrutura de Pastas

```bash
oraculo/
├── index.py
├── modules/
├── src/
│   ├── models/      # Coloque seu modelo .gguf aqui
│   └── vectorstore/ # Será criado automaticamente
├── training/        # Coloque seus documentos aqui
└── docs/
```

### 2. Adicionar Documentos

Coloque seus arquivos na pasta `training/`:
- PDFs: relatórios, manuais, etc
- DOCX: documentos Word
- XLSX/XLS: planilhas Excel

### 3. Executar pela Primeira Vez

```bash
python index.py
```

O sistema irá:
1. Verificar dependências
2. Alertar se falta o modelo LLM (pode continuar sem ele)
3. Mostrar o menu principal

### 4. Indexar Documentos

No menu, escolha opção **1** para indexar seus documentos.

Primeira vez demora mais (baixa modelo de embeddings ~200MB).

### 5. Fazer Primeira Pergunta

Escolha opção **2** e faça uma pergunta sobre seus documentos!

## ⚙️ Configurações Avançadas

### Ajustar Caminho do Modelo

Edite `index.py` linha ~87:

```python
MODEL_PATH = "src/models/seu-modelo.gguf"
```

### Trocar Modelo de Embeddings

Edite `modules/embedding_generator.py`:

```python
def __init__(self, model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
```

Alternativas:
- `distiluse-base-multilingual-cased-v2` (mais rápido)
- `paraphrase-multilingual-mpnet-base-v2` (melhor qualidade)

### Ajustar Uso de Memória

Para computadores com menos RAM, edite `modules/llm.py`:

```python
self.llm = Llama(
    model_path=self.model_path,
    n_ctx=1024,        # Reduzir de 2048
    n_threads=2,       # Reduzir de 4
    n_batch=128        # Adicionar para limitar batch
)
```

## 🐛 Problemas Comuns

### Erro: "No module named 'sentence_transformers'"

```bash
pip install sentence-transformers
```

### Erro: "Failed to build llama-cpp-python"

**Solução 1** (Windows): Instale Visual Studio Build Tools
- https://visualstudio.microsoft.com/visual-cpp-build-tools/

**Solução 2**: Use versão pré-compilada
```bash
pip install llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
```

### Erro: Memória Insuficiente

- Use modelo menor (Q4 ao invés de Q5/Q6)
- Reduza `n_ctx` no código
- Feche outros programas

### Modelo de Embeddings não Baixa

```bash
# Download manual
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')"
```

### ChromaDB - Erro SQLite

No Windows, pode precisar atualizar:
```bash
pip install pysqlite3-binary
```

## 🔄 Atualização

Para atualizar dependências:

```bash
pip install --upgrade PyPDF2 python-docx openpyxl sentence-transformers chromadb llama-cpp-python
```

## 🧪 Testar Componentes

### Teste 1: Carregar Documentos

```python
from modules.document_loader import DocumentLoader

loader = DocumentLoader("training")
docs = loader.load_all_documents()
print(f"✅ {len(docs)} documentos carregados")
```

### Teste 2: Embeddings

```python
from modules.embedding_generator import EmbeddingGenerator

gen = EmbeddingGenerator()
emb = gen.generate_embedding("teste")
print(f"✅ Embedding gerado: {emb.shape}")
```

### Teste 3: Vector Store

```python
from modules.vector_store import VectorStore

vs = VectorStore("src/vectorstore")
stats = vs.get_collection_stats()
print(f"✅ Vector Store: {stats}")
```

## 📚 Recursos Adicionais

- **Modelos LLM**: https://huggingface.co/TheBloke
- **sentence-transformers**: https://www.sbert.net/
- **ChromaDB Docs**: https://docs.trychroma.com/
- **llama.cpp**: https://github.com/ggerganov/llama.cpp

## 💡 Dicas

1. **Primeira execução**: Seja paciente, downloads iniciais podem demorar
2. **Sem modelo LLM**: Sistema funciona em modo teste
3. **Documentos grandes**: Indexação pode demorar alguns minutos
4. **Internet**: Necessária apenas para instalar pacotes e baixar modelos inicialmente

## ✅ Checklist Pós-Instalação

- [ ] Python 3.8+ instalado
- [ ] Todas as dependências instaladas
- [ ] Pasta `training/` com documentos
- [ ] Modelo LLM baixado (opcional)
- [ ] Primeira indexação completa
- [ ] Primeira pergunta testada

---

**Pronto!** Você está pronto para usar o Sistema Oráculo! 🔮

Se tiver problemas, consulte os logs em `oraculo.log` ou a documentação adicional em `docs/`.
