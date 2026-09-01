# Security Policy

## Scope

This repository documents shared local-AI architecture and integration patterns for the AMD Lemonade Developer Challenge. It contains **reference examples and documentation only** — not production deployments, credentials, or private data.

## What This Repository Must Never Contain

- `.env` files, passwords, tokens, API keys, or SSH keys
- Cookies, browser profiles, or session data
- Private documents, private RAG corpora, or user-generated content
- Model weights (GGUF, ONNX, safetensors, etc.)
- Unsanitized application or system logs
- Database files or backups containing personal data
- TLS private keys or certificate signing requests

## Reporting a Vulnerability

If you discover a security issue in materials published here, please report it privately to the repository maintainer. Do **not** open a public issue containing exploit details or sensitive data.

## Handling Credentials in Local Deployments

Applications that call Lemonade (e.g., Father Fox) read credentials from environment variables such as `LEMONADE_API_KEY`. These values belong in your local environment or secret store — never in this repository.

## Sanitized Evidence

Log excerpts under `evidence/sanitized-logs/` are deliberately redacted examples derived from known log message patterns in source code. They are not copies of raw system logs.

## Third-Party Services

This project is designed for **fully local** inference via AMD Lemonade. No cloud API keys or external inference endpoints are required for the documented architecture.
