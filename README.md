# MegaRAG Reproduction

> **A Python reproduction of the ACL 2026 paper**
>
> **MegaRAG: Multimodal Knowledge Graph-Based Retrieval-Augmented Generation**

This repository reproduces the core architecture of **MegaRAG**, a Multimodal Knowledge Graph-based Retrieval-Augmented Generation (RAG) framework. The implementation constructs a multimodal knowledge graph from PDF documents and performs graph-based retrieval to support question answering using locally deployed Qwen models.

Repository:
https://github.com/Ariful2607/ExtMEGA-RAG

---

# Table of Contents

- Overview
- Features
- Project Structure
- System Requirements
- Installation
- Model Preparation
- Configuration
- Pipeline
- Usage
  - Build Knowledge Graph
  - Run Inference
  - Evaluate
- Output Files
- Reproducing the Results
- Limitations
- Future Improvements
- References

---

# Overview

Traditional Retrieval-Augmented Generation (RAG) retrieves relevant text chunks before generating answers. MegaRAG extends this paradigm by constructing a **Multimodal Knowledge Graph (MMKG)** from documents, allowing retrieval over graph entities and relations rather than plain text.

This reproduction implements the complete end-to-end pipeline:

- PDF Parsing
- Entity Extraction
- Relation Extraction
- Knowledge Graph Construction
- Graph Retrieval
- Neighbor Expansion
- Context Construction
- LLM-based Answer Generation

The implementation uses **local models**, enabling offline inference without relying on proprietary APIs.

---

# Features

Implemented modules include:

- PDF Parser
- Page Chunking
- Multimodal Entity Extraction
- Relation Extraction
- Knowledge Graph Builder
- Duplicate Entity Merging
- Cross-page Entity Linking
- Embedding Generation
- Graph Retriever
- Neighbor Expansion
- Context Builder
- Qwen-based Generator
- Evaluation Script

---

# Project Structure

```text
MMKG-RAG/

├── configs/
│   └── config.yaml
│
├── parser/
├── extraction/
├── graph/
├── models/
├── pipeline/
├── prompts/
├── preprocessing/
├── utils/
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
├── requirements.txt
└── README.md
```

---

# System Requirements

Recommended hardware:

| Component | Recommendation |
|------------|---------------|
| Python | 3.11+ |
| GPU | NVIDIA RTX GPU |
| VRAM | 24 GB or higher |
| CUDA | 12.8+ |

Tested on:

- NVIDIA RTX 5090
- CUDA 13.1
- Windows 11

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/Ariful2607/ExtMEGA-RAG.git

cd ExtMEGA-RAG
```

---

## 2. Create Python Environment

Using Conda:

```bash
conda create -n mmkg-rag python=3.11

conda activate mmkg-rag
```

---

## 3. Upgrade pip

```bash
python -m pip install --upgrade pip
```

---

## 4. Install PyTorch

Install the PyTorch version compatible with your CUDA version.

Example (CUDA 12.8):

```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

For other CUDA versions:

https://pytorch.org/get-started/locally/

---

## 5. Install Project Dependencies

```bash
pip install -r requirements.txt
```

The main dependencies include:

- accelerate
- transformers
- sentence-transformers
- PyMuPDF
- faiss-cpu
- networkx
- timm
- Pillow
- opencv-python
- pandas
- scikit-learn
- scipy
- omegaconf
- tqdm

---

# Model Preparation

This project uses locally deployed Hugging Face models.

Required models:

| Component | Model |
|------------|-----------------------------|
| Vision-Language Model | Qwen2.5-VL |
| Text Generation Model | Qwen2.5 |
| Embedding Model | BAAI/bge-large-en-v1.5 |

Download the required models and update their locations in the configuration file.

---

# Configuration

Edit

```text
configs/config.yaml
```

Example:

```yaml
models:

  qwen_vl:
    model_path: models/Qwen2.5-VL

  llm:
    model_path: models/Qwen2.5

embedding:

  model_name: BAAI/bge-large-en-v1.5

retrieval:

  top_k: 5
  hops: 1

graph:

  cross_page_similarity: 0.90
```

---

# Pipeline

```text
PDF
 │
 ▼
Parser
 │
 ▼
Chunk
 │
 ▼
Entity Extraction
 │
 ▼
Relation Extraction
 │
 ▼
Knowledge Graph
 │
 ▼
Duplicate Merge
 │
 ▼
Embedding Generation
 │
 ▼
Cross-page Linking
 │
 ▼
Retriever
 │
 ▼
Neighbor Expansion
 │
 ▼
Context Builder
 │
 ▼
Generator
 │
 ▼
Answer
```

---

# Usage

## Step 1 — Build the Knowledge Graph

Run:

```bash
python -m scripts.build_graph
```

Expected output:

```text
Building Knowledge Graph...

Duplicate Merge...

Embedding Generation...

Cross-page Linking...

Final Graph

Entities : XX

Relations: XX
```

The generated graph will be saved as:

```text
graph/megarag_graph.pkl
```

---

## Step 2 — Run Inference

Run:

```bash
python -m scripts.inference
```

Example:

```text
Question:

What is MegaRAG?

Generated Answer:

MegaRAG is a multimodal graph-based Retrieval-Augmented Generation framework...
```

---

## Step 3 — Evaluate

Run:

```bash
python -m scripts.evaluate
```

Evaluation questions are stored in:

```text
evaluation/questions.json
```

Generated results:

```text
evaluation/results.json
```

Example summary:

```text
Average F1 Score: 0.81
```

---

# Output Files

Knowledge Graph

```text
graph/

    megarag_graph.pkl
```

Evaluation

```text
evaluation/

    questions.json

    results.json
```

---

# Reproducing the Results

To reproduce the implementation:

1. Install the required environment.
2. Download the required Hugging Face models.
3. Configure `configs/config.yaml`.
4. Build the knowledge graph:

```bash
python -m scripts.build_graph
```

5. Run inference:

```bash
python -m scripts.inference
```

6. Run evaluation:

```bash
python -m scripts.evaluate
```

---

# Limitations

This implementation focuses on reproducing the overall MegaRAG architecture.

Current limitations include:

- Evaluation is performed on a small-scale dataset.
- Entity canonicalization can be further improved.
- Retrieval quality depends on entity extraction quality.
- Benchmark datasets from the original paper are not included.

---

# Future Improvements

Potential future work includes:

- Support for larger document collections.
- Improved entity canonicalization.
- More sophisticated graph retrieval strategies.
- Evaluation using the original MegaRAG benchmark datasets.
- Integration with additional multimodal foundation models.

---

# References

MegaRAG:

**MegaRAG: Multimodal Knowledge Graph-Based Retrieval-Augmented Generation**

ACL 2026.