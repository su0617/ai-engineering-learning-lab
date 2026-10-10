"""基于 FAISS + Ollama 的单机知识库检索。

这条路径只用于学习和快速验证。正式项目的生产向量库仍然保留在
`app/core/milvus.py` 和 `app/core/vector_store.py` 中。
"""

from __future__ import annotations

import os
import re
from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CORPUS_ROOT = PROJECT_ROOT / "data" / "kb_corpus"


def _query_tokens(query: str) -> list[str]:
    """提取用于本地预筛选的中英文关键词。"""

    tokens = re.findall(r"[a-zA-Z0-9_]+|[\u4e00-\u9fff]{2,}", (query or "").lower())
    stopwords = {"the", "and", "for", "with", "how", "what", "诊断", "排查", "问题"}
    return [token for token in tokens if len(token) > 1 and token not in stopwords]


def _rank_files(files: list[Path], query: str) -> list[Path]:
    """在调用 Embedding 前做小成本候选筛选。

    目的不是替代向量检索，而是避免轻量模式只索引少量文件时被目录排序主导。
    正式模式仍可把 `max_docs` 设为 0，对全部语料做向量化。
    """

    tokens = _query_tokens(query)
    if not tokens:
        return files

    scored: list[tuple[int, Path]] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        source = str(path).lower()
        score = sum(text.count(token) + 3 * source.count(token) for token in tokens)
        scored.append((score, path))
    return [path for _score, path in sorted(scored, key=lambda item: (-item[0], str(item[1])))]


def load_corpus(max_docs: int = 80, *, query: str = "") -> list[Document]:
    """读取少量相关 Markdown 文档，避免第一次验证耗时过长。"""

    files = sorted(CORPUS_ROOT.rglob("*.md"))
    files = _rank_files(files, query)
    if max_docs > 0:
        files = files[:max_docs]
    documents: list[Document] = []
    for path in files:
        text = path.read_text(encoding="utf-8", errors="ignore").strip()
        if text:
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": str(path.relative_to(PROJECT_ROOT))},
                )
            )
    return documents


def build_local_store(max_docs: int = 80, *, query: str = "") -> FAISS:
    """构建一次性本地 FAISS 索引。"""

    documents = load_corpus(max_docs=max_docs, query=query)
    if not documents:
        raise RuntimeError(f"知识库为空: {CORPUS_ROOT}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embeddings = OllamaEmbeddings(
        model=os.getenv("OLLAMA_EMBEDDING_MODEL", "bge-m3"),
        base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
    )
    return FAISS.from_documents(chunks, embeddings)


def retrieve_local(
    query: str,
    *,
    max_docs: int = 80,
    top_k: int = 4,
) -> list[dict[str, str | float]]:
    """检索知识库并返回带来源的证据。"""

    store = build_local_store(max_docs=max_docs, query=query)
    results = store.similarity_search_with_score(query, k=max(1, top_k))
    return [
        {
            "source": str(doc.metadata.get("source", "unknown")),
            "content": doc.page_content[:2400],
            "score": float(score),
        }
        for doc, score in results
    ]
