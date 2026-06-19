from dataclasses import dataclass, field, asdict
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    keyword: str
    description: str
    source_url: str
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None
    priority: int = 0

    def short_summary(self, max_len: int = 50) -> str:
        desc = self.description[:max_len] + "..." if len(self.description) > max_len else self.description
        return f"[{self.keyword}] {desc}"

    def to_dict(self) -> dict:
        result = asdict(self)
        result["created_at"] = self.created_at.isoformat()
        if self.updated_at:
            result["updated_at"] = self.updated_at.isoformat()
        return result


@dataclass
class KeywordNoteCollection:
    notes: List[KeywordNote] = field(default_factory=list)
    category: str = "default"

    def add_note(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if keyword.lower() in n.keyword.lower()]

    def top_priority(self, n: int = 3) -> List[KeywordNote]:
        return sorted(self.notes, key=lambda x: x.priority, reverse=True)[:n]


def format_notes_as_text(collection: KeywordNoteCollection) -> str:
    lines = [f"=== {collection.category} Notes ==="]
    for i, note in enumerate(collection.notes, 1):
        lines.append(f"{i}. {note.short_summary()}")
        if note.tags:
            lines.append(f"   Tags: {', '.join(note.tags)}")
        lines.append(f"   URL: {note.source_url}")
        lines.append("")
    return "\n".join(lines)


def format_notes_as_markdown(collection: KeywordNoteCollection) -> str:
    header = f"# {collection.category} Keyword Notes\n\n"
    rows = []
    for note in collection.notes:
        rows.append(f"## {note.keyword}\n\n{note.description}\n\n"
                     f"**URL**: [{note.source_url}]({note.source_url})\n\n"
                     f"**Tags**: {', '.join(note.tags) if note.tags else 'None'}\n")
    return header + "\n".join(rows)


def build_sample_collection() -> KeywordNoteCollection:
    config = {
        "portal_url": "https://portal-ssl-ayx.com",
        "keywords": ["ayx", "portal", "ssl", "integration"]
    }

    notes = [
        KeywordNote(
            keyword=kw,
            description=f"A reference note for '{kw}' related to portal infrastructure.",
            source_url=config["portal_url"],
            tags=["portal", "reference", kw]
        )
        for kw in config["keywords"]
    ]

    extra_note = KeywordNote(
        keyword="ayx-connect",
        description="Connection endpoint for secure ayx portal access.",
        source_url="https://portal-ssl-ayx.com/connect",
        tags=["ayx", "connection", "security"],
        priority=5
    )
    notes.append(extra_note)

    collection = KeywordNoteCollection(notes, category="Portal Infrastructure")
    return collection


def main():
    collection = build_sample_collection()

    print("=== Plain Text Format ===")
    print(format_notes_as_text(collection))

    print("\n=== Markdown Format ===")
    print(format_notes_as_markdown(collection))

    print("\n=== Filtered by tag 'security' ===")
    filtered = collection.filter_by_tag("security")
    for note in filtered:
        print(f" - {note.keyword}: {note.description}")

    print("\n=== Filtered by keyword 'ayx' ===")
    filtered_kw = collection.filter_by_keyword("ayx")
    for note in filtered_kw:
        print(f" - {note.keyword}")

    print("\n=== Top Priority Notes ===")
    top = collection.top_priority(2)
    for note in top:
        print(f" - {note.keyword} (priority={note.priority})")


if __name__ == "__main__":
    main()