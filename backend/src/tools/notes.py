from pathlib import Path
import os
from typing import Any

from langchain.tools import tool


def _get_vault_root() -> Path:
    """Resolve Obsidian vault root from env or by walking up to `.obsidian`."""
    env_path = os.getenv("OBSIDIAN_VAULT_PATH")
    if env_path:
        path = Path(env_path).expanduser().resolve()
        if not path.exists() or not path.is_dir():
            raise ValueError(
                "Configured OBSIDIAN_VAULT_PATH does not exist or is not a directory."
            )
        return path

    current = Path(__file__).resolve()
    for parent in [current, *current.parents]:
        if parent.name == ".obsidian":
            return parent.parent

    raise ValueError(
        "Could not determine vault root. Set OBSIDIAN_VAULT_PATH in environment."
    )


def _normalize_note_path(note_path: str, vault_root: Path) -> Path:
    """Create an absolute markdown path under the vault and block path traversal."""
    cleaned = note_path.strip().replace("\\", "/")
    if not cleaned:
        raise ValueError("note_path cannot be empty")

    if not cleaned.endswith(".md"):
        cleaned = f"{cleaned}.md"

    candidate = (vault_root / cleaned).resolve()
    if candidate != vault_root and vault_root not in candidate.parents:
        raise ValueError("note_path must stay within the Obsidian vault")

    return candidate


@tool
def add_note(note_path: str, content: str) -> dict[str, Any]:
    """Create or overwrite a markdown note in the Obsidian vault."""
    vault_root = _get_vault_root()
    target = _normalize_note_path(note_path=note_path, vault_root=vault_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "action": "add_note",
        "path": str(target.relative_to(vault_root)).replace("\\", "/"),
    }


@tool
def get_notes() -> dict[str, Any]:
    """Return all markdown notes in the Obsidian vault with their contents."""
    vault_root = _get_vault_root()
    notes: list[dict[str, str]] = []

    for file_path in sorted(vault_root.rglob("*.md")):
        if any(
            part.startswith(".") for part in file_path.relative_to(vault_root).parts
        ):
            # Skip hidden folders/files, including `.obsidian` internals.
            continue

        notes.append(
            {
                "path": str(file_path.relative_to(vault_root)).replace("\\", "/"),
                "content": file_path.read_text(encoding="utf-8", errors="ignore"),
            }
        )

    return {
        "success": True,
        "action": "get_notes",
        "count": len(notes),
        "notes": notes,
    }


@tool
def delete_note(note_path: str) -> dict[str, Any]:
    """Delete a markdown note from the Obsidian vault."""
    vault_root = _get_vault_root()
    target = _normalize_note_path(note_path=note_path, vault_root=vault_root)

    if not target.exists() or not target.is_file():
        return {
            "success": False,
            "action": "delete_note",
            "path": str(target.relative_to(vault_root)).replace("\\", "/"),
            "message": "Note not found",
        }

    target.unlink()
    return {
        "success": True,
        "action": "delete_note",
        "path": str(target.relative_to(vault_root)).replace("\\", "/"),
    }
