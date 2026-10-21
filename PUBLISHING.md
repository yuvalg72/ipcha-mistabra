# Packaging and Publishing

This repository is designed as a **single ChatGPT Skill at the repository root**. `SKILL.md` is the execution contract and `README.md` is the human-facing landing page.

## Build the installable ZIP

From the repository root, with Python 3.10+:

```bash
python3 scripts/validate_skill.py
python3 -B -m unittest discover -s tests -v
python3 scripts/package.py
```

The packager creates `skill.zip` with exactly one top-level directory named `ipcha-mistabra`, including the source README, `SKILL.md`, `agents/`, `assets/`, `references/`, `scripts/`, tests, license, notices, and CI sources. Temporary files, caches, `.git`, local environments and the archive itself are excluded. ZIP metadata is fixed to support byte-for-byte repeatability when source files do not change. The package must be smaller than 25 MiB.

To write the package outside the repository:

```bash
python3 scripts/package.py --output ../skill.zip
```

Upload that archive to the ChatGPT Skills management interface. No API key or upload automation is required to build it.

## Initial GitHub publication to an empty repository

The initial target is `https://github.com/yuvalg72/ipcha-mistabra`. If the repository is still empty, a first commit to its default branch is necessary before normal PR-based development is possible. In a local copy of this **repository-ready source tree**:

```bash
git init -b main
git add .github .editorconfig .gitattributes .gitignore SKILL.md README.md LICENSE THIRD_PARTY_NOTICES.md SECURITY.md CONTRIBUTING.md PUBLISHING.md CHANGELOG.md agents assets examples references scripts tests
git commit -m "feat: initialize Ipcha Mistabra decision-review skill"
git remote add origin https://github.com/yuvalg72/ipcha-mistabra.git
git push -u origin main
```

The push requires the repository owner's GitHub authentication and intentionally does not include a token. If the remote has since been initialized, do not overwrite it: fetch and reconcile existing content or submit a PR from a new branch. After bootstrap, use dedicated branches and PRs for changes. Never force push to overcome a conflicting history.

## Post-publication checks

1. Refetch `main` and confirm `SKILL.md`, the README, icon, sources, CI and tests exist.
2. Confirm GitHub Actions actually ran and passed on the exact commit, not just that workflow YAML exists.
3. Inspect open PR discussions and reviews before merge; a missing automated review is not approval.
4. Add an accurate repository About description (suggested: `Evidence-first contrarian decision reviews, structured red-teaming and falsifiable verdicts for ChatGPT`) and topics such as `chatgpt-skill`, `devils-advocate`, `red-team`, `critical-thinking`, `decision-making`, `argumentation` when permissions permit.
5. Only create a version tag and GitHub Release when the source, tests, and governance gates are satisfied. Do not call the ZIP "released" merely because it exists locally.
