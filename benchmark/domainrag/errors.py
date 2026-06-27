from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str

    def format(self) -> str:
        return f"{self.path}: {self.message}"


class ValidationError(Exception):
    """Raised when DomainRAG dataset validation fails."""

    def __init__(self, issues: list[ValidationIssue] | str):
        if isinstance(issues, str):
            self.issues = [ValidationIssue(path="<unknown>", message=issues)]
        else:
            self.issues = issues
        super().__init__("\n".join(issue.format() for issue in self.issues))
