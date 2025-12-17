# 🔮 Sistema Oráculo - Guia Rápido

## ✅ Status Atual: SISTEMA TOTALMENTE FUNCIONAL

O Sistema Oráculo está **completo e operacional** com as seguintes funcionalidades:

### 🎯 Funcionalidades Principais

1. **✅ RAG Completo** - Retrieval Augmented Generation totalmente local
2. **✅ 7 Modelos LLM** - Gerenciamento integrado de modelos GPT4All
3. **✅ GPU Acelerada** - Suporte automático a NVIDIA CUDA
4. **✅ Interface Limpa** - Logs organizados, console profissional
5. **✅ Alta Precisão** - Temperature 0.2, prompt otimizado
6. **✅ Logs Detalhados** - Pasta logs/ com arquivos diários

## 🚀 Início Rápido

### 1. Instalação Automática (Windows)

```cmd
execute.bat
# Escolha: 1 - Instalar dependências
```

### 2. Executar o Sistema

```cmd
python index.py
# ou
execute.bat → 2 - Executar Sistema
```

### 3. Menu Principal

**📚 DOCUMENTOS:**
- 1️⃣ Indexar documentos
- 2️⃣ Fazer pergunta
- 3️⃣ Modo interativo
- 4️⃣ Ver estatísticas
- 5️⃣ Reindexar

**🤖 MODELOS LLM:**
- 6️⃣ Listar modelos (7 disponíveis)
- 7️⃣ Ver detalhes de modelo
- 8️⃣ Selecionar modelo ativo

## 📋 Requisitos

### ✅ Compatibilidade Python

| Versão | Status | Notas |
|--------|--------|-------|
| 3.10.x | ✅ Excelente | Totalmente testado |
| 3.11.x | ✅ Excelente | Totalmente testado |
| 3.12.x | ✅ Excelente | Totalmente testado |
| 3.13.x | ✅ Ótimo | **Versão atual recomendada** |
| 3.14.x | ⚠️ Evitar | Bibliotecas sem suporte completo |

### 💻 Hardware Recomendado

**Mínimo:**
- CPU: Dual-core 2.0 GHz
- RAM: 8 GB
- Disco: 10 GB livres
- GPU: Nenhuma (funciona em CPU)

**Recomendado:**
- CPU: Quad-core 3.0 GHz+
- RAM: 16 GB
- Disco: 20 GB livres (para múltiplos modelos)
- GPU: NVIDIA RTX 2060+ (6GB VRAM)

## 🤖 Modelos LLM Disponíveis

O sistema usa **GPT4All** - 100% Python, sem compiladores!

# 3. Executar instalador
execute.bat

# 4. Escolher opção 1
```

## ⚡ Sistema Funcionará Sem LLM

**Importante**: Se `llama-cpp-python` falhar na instalação:
- ✅ O sistema AINDA funcionará
- ✅ Todos os documentos serão indexados
- ✅ Busca semântica funcionará perfeitamente
- ⚠️ Respostas serão limitadas (modo teste)

Para respostas completas, você pode:
1. Instalar Python 3.12 (recomendado)
2. Ou baixar modelos LLM via API (Ollama, LM Studio)

## 📞 Perguntas Frequentes

**P: Preciso desinstalar Python 3.14?**
R: Não necessariamente. Você pode ter múltiplas versões. Use `py -3.12` ou `python3.12`.


| Modelo | Tamanho | Qualidade | Ideal Para |
|--------|---------|-----------|------------|
| **Mistral 7B OpenOrca** | 3.8 GB | ⭐⭐⭐⭐⭐ | Uso geral (Padrão) |
| **Mistral 7B Instruct** | 3.8 GB | ⭐⭐⭐⭐⭐ | Precisão literal |
| **Orca 2 7B** | 3.8 GB | ⭐⭐⭐⭐ | Análise técnica |
| **Nous Hermes 13B** | 7.3 GB | ⭐⭐⭐⭐⭐ | Máxima qualidade |
| **GPT4All Falcon** | 3.9 GB | ⭐⭐⭐⭐ | Versatilidade |
| **WizardLM 13B** | 7.3 GB | ⭐⭐⭐⭐⭐ | Raciocínio complexo |
| **Orca Mini 3B** | 1.8 GB | ⭐⭐⭐ | PCs fracos |

💡 **Download automático** na primeira execução!

## 🎨 Recursos Avançados

### 📊 Sistema de Logs

**Console:** Interface limpa, apenas o essencial
**Arquivos:** `logs/oraculo_YYYYMMDD.log` - Completo e detalhado

```
logs/
├── oraculo_20251217.log  ← Hoje
├── oraculo_20251216.log  ← Ontem
└── oraculo_20251215.log  ← Anteontem
```

### ⚙️ Configurações (config.json)

```json
{
  "selected_model": "mistral-7b-openorca.Q4_0.gguf",
  "temperature": 0.2,
  "max_tokens": 512
}
```

### 🎯 Precisão Otimizada

- **Temperature:** 0.2 (respostas determinísticas)
- **Chunks:** 5 documentos relevantes (antes: 3)
- **Contexto:** 2500 chars por chunk (antes: 1500)
- **Prompt:** Instruções rigorosas para evitar "alucinações"

### 🧪 Benchmark de Qualidade

Incluso: `BENCHMARK-PERGUNTAS.md`
- 25+ perguntas de teste
- 7 categorias (contradições, ambiguidades, etc)
- Sistema de pontuação

## 📚 Documentação Completa

```
docs/
├── README.md              # Visão geral
├── LEIA-ME-PRIMEIRO.md   # Este arquivo
├── INSTALLATION.md        # Instalação detalhada
├── ARCHITECTURE.md        # Arquitetura do sistema
└── GPT4ALL-IMPLEMENTADO.md # Detalhes do GPT4All
```

## 🐛 Solução de Problemas

### Erro: "Python not found"
```cmd
# Reinstale Python e marque "Add to PATH"
# Ou use: py -3.13 index.py
```

### Erro: "Failed to load DLL"
✅ **Normal!** São warnings do GPT4All tentando diferentes versões CUDA.
O sistema funciona perfeitamente, apenas ignore.

### Erro: "No module named X"
```cmd
pip install -r requirements.txt
```

### GPU não detectada
```cmd
# Verifique CUDA
nvidia-smi

# Instale PyTorch com CUDA (opcional)
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Respostas imprecisas
1. Use Menu → Opção 8 para trocar modelo
2. Teste Mistral 7B Instruct (mais preciso)
3. Use BENCHMARK-PERGUNTAS.md para testar

## ❓ FAQ

**P: Funciona totalmente offline?**
R: ✅ Sim! 100% local após baixar o modelo.

**P: Quanto tempo demora para baixar o modelo?**
R: ~10-20 minutos (3.8 GB), dependendo da conexão.

**P: Posso usar múltiplos modelos?**
R: ✅ Sim! Baixe vários e troque pelo menu (opção 8).

**P: GPU é obrigatória?**
R: ❌ Não! Funciona em CPU (mais lento, mas funciona).

**P: Quantos documentos posso indexar?**
R: Sem limite! Depende apenas do espaço em disco.

**P: Suporta português?**
R: ✅ Perfeitamente! Embeddings multilíngues + modelos em PT.

## 🎓 Próximos Passos

1. ✅ Execute `python index.py`
2. ✅ Opção 1 - Indexar documentos de teste
3. ✅ Opção 3 - Modo interativo
4. ✅ Teste com perguntas do BENCHMARK-PERGUNTAS.md
5. ✅ Opção 6 - Ver modelos disponíveis
6. ✅ Adicione seus documentos em `training/`

## 📞 Suporte

- **Logs:** Verifique `logs/oraculo_YYYYMMDD.log`
- **Documentação:** Consulte arquivos em `docs/`
- **Problemas:** Revise erros nos logs detalhados

---

**Sistema Oráculo v1.0.0**
Inteligência Artificial Local para Consulta de Documentos 🔮

**Última atualização:** 17/12/2025  
**Status:** ✅ Totalmente funcional  
**Recursos:** 7 modelos LLM, GPU acelerada, logs organizados, interface limpa
