# Security

Brevo Helper is an unofficial community plugin. Do not use public issues, pull requests, screenshots, or chat transcripts to share Brevo credentials, contact exports, customer data, or private campaign content.

## Supported Scope

The public/default plugin is designed for read-oriented setup, campaign planning, QA, and backend integration work. It intentionally avoids default send, schedule, launch, activation, and enrollment capabilities.

## Reporting A Vulnerability

If you find a vulnerability:

1. Do not include secrets or customer data in the report.
2. Open a GitHub security advisory for this repository if available.
3. If a private advisory is not available, open a minimal GitHub issue describing the affected area without exploitable credentials or private account data.

## If A Secret Was Exposed

Rotate the exposed Brevo key or token immediately in Brevo, remove it from local environment files or logs, and verify the repository history before publishing any additional release.

The validation script checks for obvious Brevo token patterns, but it is not a substitute for manual review.

