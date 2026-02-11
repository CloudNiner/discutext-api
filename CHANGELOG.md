# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.1.0] - 2026-02-10

### Added

- Add Dockerfile
- Add CHANGELOG.md 🔥

## Changed

- Python 3.12 -> Python 3.14
- mypy -> basedpyright
- isort,black,flake8 -> ruff

## Fixed

- Significantly decreased API response times by slimming zip package enough to remove `slim_handler: true` by removing dev dependencies before upload

## [1.0.0] - 2025-01-25

### Changed

- Pydantic 1 -> Pydantic 2
- Python 3.9 -> Python 3.12
- Switch to `uv`
