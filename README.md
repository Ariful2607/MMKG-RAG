# MegaRAG Reproduction

A Python reproduction of the ACL 2026 paper:

> **MegaRAG: Multimodal Knowledge Graph-Based Retrieval-Augmented Generation**

This project reproduces the end-to-end MegaRAG framework, including document parsing, multimodal entity extraction, relation extraction, knowledge graph construction, graph retrieval, neighborhood expansion, context building, and answer generation using local Qwen models.

https://github.com/Ariful2607/ExtMEGA-RAG

---

# Table of Contents

- Overview
- Features
- Project Structure
- Environment Requirements
- Installation
- Configuration
- Models
- Pipeline
- Build Knowledge Graph
- Run Inference
- Evaluate
- Expected Outputs
- Reproducing the Results
- Notes
- Limitations
- References

---

# Overview

MegaRAG enhances Retrieval-Augmented Generation (RAG) by constructing a Multimodal Knowledge Graph (MMKG) from PDF documents.

Instead of retrieving plain text chunks, MegaRAG retrieves graph entities and their neighboring evidence before generating responses.

This reproduction implements the complete pipeline locally using:

- Qwen2.5-VL
- Qwen2.5
- SentenceTransformer embeddings

---

# Features

Implemented components:

- PDF Parsing
- Page Chunking
- Multimodal Entity Extraction
- Relation Extraction
- Knowledge Graph Construction
- Duplicate Entity Merging
- Embedding Generation
- Cross-page Entity Linking
- Graph Retrieval
- Neighbor Expansion
- Context Builder
- LLM-based Answer Generation
- Evaluation Script

---

# Project Structure

```
MMKG-RAG/

│
├── configs/
│   └── config.yaml
│
├── parser/
│
├── extraction/
│
├── graph/
│
├── models/
│
├── pipeline/
│
├── prompts/
│
├── scripts/
│   ├── build_graph.py
│   ├── inference.py
│   └── evaluate.py
│
├── evaluation/
│   ├── questions.json
│   └── results.json
│
├── graph/
│   └── megarag_graph.pkl
│
└── README.md
```

---

# Environment Requirements

Recommended:

- Python 3.11+
- CUDA 12.4 or newer
- NVIDIA GPU (24GB+ VRAM recommended)

Tested on

- RTX 5090
- CUDA 13.1
- Windows 11

---

# Installation

Create a virtual environment

```bash
conda create -n mmkg-rag python=3.11

conda activate mmkg-rag
```

Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is unavailable:

```bash
pip install

torch
transformers
sentence-transformers
networkx
numpy
opencv-python
pdfplumber
Pillow
omegaconf
tqdm
```

---

# Configuration

Edit

```
configs/config.yaml
```

Example

```yaml
models:

  qwen_vl: path/to/Qwen2.5-VL

  llm: path/to/Qwen2.5

embedding:

  model: BAAI/bge-large-en-v1.5

retrieval:

  top_k: 5

  hops: 1

graph:

  cross_page_similarity: 0.90
```

---

# Models

The following local models are used.

| Component | Model |
|------------|------------------------------|
| Vision-Language | Qwen2.5-VL |
| Text Generation | Qwen2.5 |
| Embedding | BAAI/bge-large-en-v1.5 |

---

# Pipeline

```
PDF

↓

Parser

↓

Chunk

↓

Entity Extraction

↓

Relation Extraction

↓

Knowledge Graph

↓

Duplicate Merge

↓

Embedding Generation

↓

Cross-page Linking

↓

Retriever

↓

Neighbor Expansion

↓

Context Builder

↓

Generator
```

---

# Step 1: Build Knowledge Graph

Run

```bash
python -m scripts.build_graph
```

Expected output

```
Building Knowledge Graph...

Duplicate Merge...

Generating Embeddings...

Cross-page Linking...

Final Graph

Entities : XX

Relations : XX
```

Graph will be saved as

```
graph/megarag_graph.pkl
```

---

# Step 2: Run Inference

Run

```bash
python -m scripts.inference
```

Example

```
Question:

What is MegaRAG?

Generated Answer:

MegaRAG is a multimodal graph-based Retrieval-Augmented Generation framework...
```

---

# Step 3: Evaluate

Run

```bash
python -m scripts.evaluate
```

Evaluation uses

```
evaluation/questions.json
```

Example

```json
[
  {
    "question": "...",
    "ground_truth": "..."
  }
]
```

Results

```
evaluation/results.json
```

Average score example

```
Average F1 : 0.81
```

---

# Expected Outputs

Knowledge Graph

```
graph/

    megarag_graph.pkl
```

Evaluation

```
evaluation/

    questions.json

    results.json
```

---

# Reproducing the Results

1. Download the PDF document.

2. Configure model paths in

```
configs/config.yaml
```

3. Build the knowledge graph

```bash
python -m scripts.build_graph
```

4. Run inference

```bash
python -m scripts.inference
```

5. Evaluate

```bash
python -m scripts.evaluate
```

---

# Notes

This implementation is intended as a reproduction of the MegaRAG architecture.

Some implementation details differ from the original paper:

- Local Qwen models are used instead of proprietary APIs.
- The evaluation dataset may differ from the original benchmark.
- Entity extraction quality depends on the selected VLM.
- Results may vary depending on hardware and generation parameters.

---

# Limitations

Current limitations include:

- Small-scale graph construction during testing.
- Limited entity canonicalization.
- Simple evaluation protocol.
- No benchmark datasets from the original paper are included.

---

# References

MegaRAG:

MegaRAG: Multimodal Knowledge Graph-Based Retrieval-Augmented Generation.

ACL 2026.
