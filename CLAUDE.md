# Project purpose

This is a learning project. The user is building a RAG (Retrieval-Augmented
Generation) system by hand in order to learn real software/ML engineering
skills — not to end up with a working product built by someone else.

**Read `project_doc.md` in this repo root before doing anything else in a new
session.** It is the actual project spec (ResearchVault) — scope, V1
definition, architecture expectations, and the evaluation-driven mindset the
user is building toward. Everything below assumes you've read it.

# How to work in this repo

- **Do not build, implement, or architect this project for the user.** The
  user writes the code and makes the design decisions.
- **Default mode is teaching.** When the user asks a question — about a
  concept, a design tradeoff, why something behaves a certain way, or how to
  debug an error — explain it clearly, grounded in the actual code/files in
  this repo where relevant, rather than giving generic textbook answers.
- **Code is sometimes requested, but only to teach.** The user may ask for a
  snippet or example to illustrate a concept. Write it to explain, not to
  advance the project. Prefer small, isolated examples over patches to their
  actual files unless they explicitly ask you to write/edit their code.
- **If the user shares code and asks "is this right?"**, critique and explain
  — point out bugs, tradeoffs, what to look up — don't just rewrite it for
  them, unless they explicitly ask you to fix/write it.
- **Don't jump ahead.** No adding features, refactors, or scaffolding beyond
  what's been asked, even if it seems like the obvious next step. Specs are
  given incrementally by the user, not all upfront.
- If the user does explicitly ask you to write or edit their project code,
  that's fine — this restriction is about defaulting to teaching, not a hard
  ban on ever touching files.

# State check (for whichever Claude picks this up next)

This section exists so a new session can get oriented fast without re-reading
the whole conversation history. **Keep it current** — update it whenever
something meaningfully changes (a stage gets built, an architecture decision
gets made), not just at the end of a long session. Stale status here is worse
than no status.

## Done so far

- Ported the original single-file toy (`reference/llm_rag.py`) into a
  modular pipeline under `src/`: `ingestion/`, `chunking/`, `embedding/`,
  `retrieval/`, `generation/` (`reranking/` scaffolded, empty). Each stage is
  a plain function; `scripts/build_index.py` wires them together.
- Verified end-to-end manually: load one hardcoded PDF → chunk
  (`RecursiveCharacterTextSplitter`) → embed (`all-MiniLM-L6-v2` via
  `sentence-transformers`) → store in a local Chroma `PersistentClient`
  collection → embed the user's query → retrieve top-k chunks → generate a
  grounded answer via Ollama (`gemma2:2b`) → print it. It runs and produces
  a real answer.
- Several naming/scope bugs from the port got debugged and fixed by the user
  (param/body name mismatches, an undefined-variable bug in the prompt
  template, a stray absolute filesystem path for the Chroma db, an unused
  import). Not documented in code comments — see conversation history if the
  "why" behind a fix matters.
- **PostgreSQL is installed and running**, via `podman` (not a native dnf
  install), specifically to keep its data on the `/mnt/kingfed` partition
  instead of the small home partition. See "Environment / infra notes" below
  for the exact setup and gotchas. The database is up and empty — no schema,
  no tables yet.

## Not started yet (per `project_doc.md` scope)

- **Workspaces.** Currently everything is one hardcoded PDF path and one
  hardcoded Chroma collection name — no concept of a workspace at all yet.
- **Multi-document ingestion** within a workspace (`data/` currently holds
  one PDF; `loader.py` takes a single hardcoded path, not a directory).
- **Incremental/idempotent reindexing.** Every run of `build_index.py`
  reprocesses everything from scratch. Chunk ids (`chunk_0, chunk_1, ...`)
  restart at zero each run and are not scoped per source file, so multi-file
  or repeated-run indexing will collide/overwrite in Chroma as-is.
- **App data schema.** Postgres itself is running (see "Done so far"), but no
  tables exist yet — `users`/`workspaces`/`documents`/`conversations`/
  `messages` per the spec are all still just a plan.
- **Citations.** `PyPDFLoader` already captures page-number metadata per
  chunk, but it isn't threaded through retrieval into the generated answer
  yet.
- FastAPI backend, frontend, Docker, deployment — none started.
- Evaluation dataset + retrieval experiments (chunk size/overlap, top-k,
  keyword vs. semantic, reranking) — none started; this is the part of the
  spec that makes the project portfolio-worthy, don't skip it once V1 works.

## In progress / actively being discussed

- Designing a **content-hash-based** approach to tell new vs.
  already-indexed files apart, scoped per workspace, so reindexing doesn't
  redo embedding work on unchanged files. Open questions being worked
  through with the user: hash file bytes vs. extracted text; where the
  hash/indexed-state lives (Chroma metadata vs. a future Postgres
  `documents` table); how chunk ids need to change to be stable per
  file/workspace instead of restarting at 0 each run.

## Next smallest step

As of 2026-09-04: Postgres is up and empty. Next real step is designing and
creating the first tables (likely `workspaces` and `documents` first, since
the hash-based reindexing work depends on `documents` existing). This is a
schema-design decision for the user to make, not to hand them — walk through
it conceptually if asked, don't write the `CREATE TABLE` statements unless
explicitly asked to.

## Environment / infra notes

Postgres runs as a rootless **podman** container, not a native install.
Worth knowing if you're debugging anything DB-connectivity related:

- Container name: `researchvault-pg`, image `docker.io/library/postgres:16`,
  port `5432` mapped to host.
- Data directory: `/mnt/kingfed/pgdata/research_vault` (bind-mounted, `:Z`
  SELinux flag), deliberately outside the git repo — it's runtime state, not
  project code.
- Podman's own image/layer storage (`graphroot`) was relocated to
  `/mnt/kingfed/containers-storage` via `~/.config/containers/storage.conf`,
  again purely for disk space reasons (home partition is small).
- **The container requires `--security-opt label=disable` to start at all.**
  Without it, Postgres's `docker-entrypoint.sh` gets killed immediately by
  SELinux (`cannot apply additional memory protection after relocation` /
  AVC denials on `libc.so.6`) — a friction point specific to running
  rootless podman's overlay storage on this btrfs mount at
  `/mnt/kingfed/containers-storage`. **Any new container run against this
  same relocated storage will likely need the same flag.** Root cause was
  never fully diagnosed at the SELinux-policy level; this flag is the
  accepted pragmatic workaround for a personal dev box, not a real fix.
- To connect manually: `podman exec -it researchvault-pg psql -U
  researchvault -d researchvault`. No `psql` client is installed on the host
  itself — connecting through the container is the intended way.
- Connection string belongs in the (currently still needs to be filled in)
  `.env` at repo root, e.g. `DATABASE_URL=postgresql://researchvault:
  <password>@localhost:5432/researchvault` — not written yet as of
  2026-09-04.
- `--restart=unless-stopped` was set on the container, but **confirmed it
  does NOT survive a full reboot** — `podman-restart.service` is disabled
  and user linger is off (verified 2026-09-04). After any reboot, the
  container will be stopped, not gone. Recovery is just:
  ```
  podman ps -a
  podman start researchvault-pg
  ```
  (no need to re-run the full `podman run ...` command — the container
  still exists, it's just not started). Auto-start on boot is possible via
  `systemctl --user enable --now podman-restart.service` +
  `loginctl enable-linger satvik`, but that hasn't been set up — user chose
  not to yet.
- The user set a shell alias, `rvpsql`, for the connect command
  (`podman exec -it researchvault-pg psql -U researchvault -d researchvault`)
  in their `~/.bashrc`.
