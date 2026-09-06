# ResearchVault — Project Spec

> Save this as the project spec. When you get lost, come back to it and ask:
> **what is the next smallest thing needed to make this system work?**

## The idea

ResearchVault is a personal document knowledge system.

A user creates a workspace around a topic, uploads multiple documents, and
can then search and ask questions across their own material.

Example workspace: **Operating Systems**

Contains:
- `os-textbook.pdf`
- `lecture-notes.pdf`
- `assignment.pdf`
- `deadlocks-notes.txt`

User asks:

> "Why can starvation happen with priority scheduling?"

ResearchVault finds the relevant information from the uploaded documents and
answers using those sources, with citations showing where the information
came from.

The important distinction is:

> This is not "upload PDF → send entire PDF to an LLM."

You're building a real retrieval pipeline.

---

## Core system

Conceptually:

```
Documents → extraction → chunking → embeddings → retrieval → LLM → cited answer
```

### Document ingestion

Users should be able to create a workspace and upload documents into it.

Initially, support PDF only. TXT/Markdown/etc. can come later.

When a PDF arrives, the backend should validate it and extract its text.

You should retain metadata such as:

- document name, page number, workspace, chunk identifier

because you'll eventually need that information for citations.

### Chunking

You cannot assume the entire document fits into an LLM request.

Split extracted content into smaller chunks.

But don't blindly pick some number because a tutorial used it.

Experiment later with things like:

- chunk size, overlap, page boundaries, paragraph boundaries.

You should eventually understand why your chunking strategy works.

### Embeddings + storage

Each chunk gets converted into an embedding.

Store:

- chunk text + embedding + metadata

in your retrieval system/vector store.

Separately, use PostgreSQL for normal application data such as
users/workspaces/documents/conversations/messages.

You get to decide the exact architecture.

### Retrieval

User asks:

> "What are the four conditions necessary for deadlock?"

Convert the question into an embedding and retrieve the most semantically
relevant chunks from that workspace.

Those chunks become evidence for the answer.

Eventually, experiment with:

- semantic retrieval, keyword retrieval, and perhaps hybrid retrieval.

But semantic retrieval alone is enough for V1.

### Generation

Give the LLM:

- user's question + retrieved chunks + source metadata

and have it generate an answer grounded in those sources.

When the documents don't contain enough information, the system should be
willing to say so rather than fabricate an answer.

### Citations

This is a core feature, not optional polish.

An answer might look like:

> Deadlock requires four conditions to hold simultaneously...
>
> Sources:
> - os-textbook.pdf — page 214
> - lecture-notes.pdf — page 37

The LLM shouldn't magically guess these sources. Your retrieval pipeline
already knows the metadata associated with each retrieved chunk.

---

## What counts as V1

Don't accidentally build Notion + ChatGPT + Google Drive + Perplexity by
yourself.

V1 is done when someone can:

> Create workspace → upload PDFs → process them → ask question → retrieve
> relevant chunks → receive grounded answer → see source citations.

That's it.

A hideous frontend is completely acceptable.

You do not need teams, sharing, payments, Google Drive integration, agents,
beautiful dashboards, mobile support, OAuth, twenty document formats, etc.

---

## The engineering side

This project exists partly to force you through the things the assessment
exposed.

The likely ecosystem is:

- Python + FastAPI for backend/AI logic.
- PostgreSQL for relational application data.
- A vector retrieval solution that you'll choose after understanding what
  you need.
- An LLM API for generation.
- Eventually a simple React/Next.js frontend.
- Git from commit #1.
- Docker once you actually have services worth containerizing.
- Then deploy the finished system.

But none of those choices are sacred. You're the engineer. Research
alternatives and make decisions.

---

## The part that makes it portfolio-worthy

Once the basic system works, don't immediately add 30 features.

**Evaluate the AI system.**

Create a small evaluation dataset yourself:

> Question / Expected source/document / Relevant passage/page

Maybe 20–30 questions across your test documents.

Then experiment.

- Does retrieving 3 chunks work better than 10?
- Does overlap help?
- Does a 300-token chunk outperform a 1,000-token chunk?
- Does keyword search catch things semantic search misses?
- Does reranking improve retrieval?

You don't need to implement every possible technique. The important thing is
learning to measure instead of guessing.

Then your résumé project stops being:

> Built a RAG chatbot using FastAPI and vector DB.

There are ten billion of those.

It becomes something closer to:

> Built and deployed a multi-document RAG system with source-grounded
> responses; designed and evaluated retrieval strategies across a custom
> benchmark and improved retrieval quality through chunking/retrieval
> experiments.

And because you built it yourself, an interviewer can ask:

> "Why did you choose that chunk size?"

and instead of:

> "Claude chose it."

you can actually explain the experiment that led you there.

---

## Your rule during the project

Documentation, Google, Stack Overflow, tutorials, papers, GitHub examples:
allowed.

Looking up syntax: allowed.

Learning unfamiliar concepts: obviously allowed.

Using an AI to understand what embeddings are or why your architecture might
have a problem: fine.

But:

> "Here's my requirement, write the FastAPI endpoint."

Nope.

And when something breaks, spend time investigating it yourself before
bringing it to an AI.

The finished application is useful.

But the real product of ResearchVault is supposed to be **you becoming
capable of building ResearchVault**.
