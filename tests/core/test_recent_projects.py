from __future__ import annotations

import json
from pathlib import Path

import pytest

from gpd.core.constants import HOME_DATA_DIR_NAME
from gpd.core.recent_projects import (
    RecentProjectsError,
    list_recent_projects,
    load_recent_projects_index,
    recent_projects_index_path,
    recent_projects_root,
    record_recent_project,
)


class TestRecentProjectsRootResolution:
    def test_prefers_explicit_data_dir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        explicit = tmp_path / "explicit-data"
        monkeypatch.setenv("GPD_DATA_DIR", str(tmp_path / "ignored"))
        monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")

        assert recent_projects_root(explicit) == explicit / "recent-projects"

    def test_uses_data_dir_env(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        data_dir = tmp_path / "data"
        monkeypatch.setenv("GPD_DATA_DIR", str(data_dir))
        monkeypatch.setattr(Path, "home", lambda: tmp_path / "home")

        assert recent_projects_root() == data_dir / "recent-projects"

    def test_defaults_to_home_gpd_dir(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        fake_home = tmp_path / "home"
        fake_home.mkdir()
        monkeypatch.delenv("GPD_DATA_DIR", raising=False)
        monkeypatch.setattr(Path, "home", lambda: fake_home)

        assert recent_projects_root() == fake_home / HOME_DATA_DIR_NAME / "recent-projects"


class TestRecentProjectsIndexPersistence:
    def test_save_and_load_round_trip(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GPD_DATA_DIR", raising=False)
        store_root = tmp_path / "cache"
        project_root = tmp_path / "project"
        project_root.mkdir()

        updated = record_recent_project(
            project_root,
            session_data={
                "last_date": "2026-03-26T12:00:00+00:00",
                "stopped_at": "Phase 03 Plan 2",
                "resume_file": "GPD/phases/03/.continue-here.md",
                "hostname": "builder-01",
                "platform": "Linux 6.1 x86_64",
            },
            store_root=store_root,
        )

        index_path = recent_projects_index_path(store_root)
        stored = json.loads(index_path.read_text(encoding="utf-8"))
        loaded = load_recent_projects_index(store_root)

        assert updated.project_root == project_root.resolve(strict=False).as_posix()
        assert stored["rows"][0]["stopped_at"] == "Phase 03 Plan 2"
        assert loaded.rows[0].resume_file == "GPD/phases/03/.continue-here.md"
        assert loaded.rows[0].last_session_at == "2026-03-26T12:00:00+00:00"

    def test_load_rejects_malformed_index(self, tmp_path: Path) -> None:
        store_root = tmp_path / "cache"
        index_path = recent_projects_index_path(store_root)
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text("{ not-json", encoding="utf-8")

        with pytest.raises(RecentProjectsError, match="Malformed"):
            load_recent_projects_index(store_root)

    def test_save_then_reload_retains_single_project_row(self, tmp_path: Path) -> None:
        store_root = tmp_path / "cache"
        project_root = tmp_path / "project"
        project_root.mkdir()

        record_recent_project(
            project_root,
            session_data={"last_date": "2026-03-26T12:00:00+00:00", "stopped_at": "Phase 1"},
            store_root=store_root,
        )
        record_recent_project(
            project_root,
            session_data={
                "last_date": "2026-03-26T13:00:00+00:00",
                "stopped_at": "Phase 2",
                "resume_file": "—",
            },
            store_root=store_root,
        )

        loaded = load_recent_projects_index(store_root)

        assert len(loaded.rows) == 1
        assert loaded.rows[0].stopped_at == "Phase 2"
        assert loaded.rows[0].resume_file is None

    def test_record_preserves_existing_optional_fields_when_not_repeated(
        self, tmp_path: Path
    ) -> None:
        store_root = tmp_path / "cache"
        project_root = tmp_path / "project"
        project_root.mkdir()

        record_recent_project(
            project_root,
            session_data={
                "last_date": "2026-03-26T12:00:00+00:00",
                "stopped_at": "Phase 1",
                "resume_file": "resume.md",
                "hostname": "builder-01",
                "platform": "Linux 6.1 x86_64",
            },
            store_root=store_root,
        )
        record_recent_project(
            project_root,
            session_data={"last_date": "2026-03-26T13:00:00+00:00", "stopped_at": "Phase 2"},
            store_root=store_root,
        )

        loaded = load_recent_projects_index(store_root)

        assert len(loaded.rows) == 1
        assert loaded.rows[0].stopped_at == "Phase 2"
        assert loaded.rows[0].resume_file == "resume.md"
        assert loaded.rows[0].hostname == "builder-01"
        assert loaded.rows[0].platform == "Linux 6.1 x86_64"


class TestRecentProjectsListing:
    def test_list_sorts_newest_first_and_preserves_missing_projects(self, tmp_path: Path) -> None:
        store_root = tmp_path / "cache"
        older = tmp_path / "older-project"
        newer = tmp_path / "newer-project"
        older.mkdir()
        newer.mkdir()

        record_recent_project(
            older,
            session_data={"last_date": "2026-03-26T10:00:00+00:00", "stopped_at": "Phase 1"},
            store_root=store_root,
        )
        record_recent_project(
            newer,
            session_data={"last_date": "2026-03-26T12:00:00+00:00", "stopped_at": "Phase 2"},
            store_root=store_root,
        )

        older.rmdir()

        rows = list_recent_projects(store_root)

        assert [row.project_root for row in rows] == [
            newer.resolve(strict=False).as_posix(),
            older.resolve(strict=False).as_posix(),
        ]
        assert rows[0].available is True
        assert rows[0].resumable is False
        assert rows[1].available is False
        assert rows[1].availability_reason == "project root missing"

    def test_list_marks_resumable_rows_when_resume_file_exists(self, tmp_path: Path) -> None:
        store_root = tmp_path / "cache"
        project_root = tmp_path / "project"
        project_root.mkdir()
        resume_file = project_root / "GPD" / "phases" / "03" / ".continue-here.md"
        resume_file.parent.mkdir(parents=True, exist_ok=True)
        resume_file.write_text("resume\n", encoding="utf-8")

        record_recent_project(
            project_root,
            session_data={
                "last_date": "2026-03-26T12:00:00+00:00",
                "stopped_at": "Phase 3",
                "resume_file": "GPD/phases/03/.continue-here.md",
            },
            store_root=store_root,
        )

        rows = list_recent_projects(store_root)

        assert len(rows) == 1
        assert rows[0].available is True
        assert rows[0].resume_file_available is True
        assert rows[0].resumable is True

    def test_list_keeps_missing_handoff_rows_but_marks_them_non_resumable(self, tmp_path: Path) -> None:
        store_root = tmp_path / "cache"
        project_root = tmp_path / "project"
        project_root.mkdir()

        record_recent_project(
            project_root,
            session_data={
                "last_date": "2026-03-26T12:00:00+00:00",
                "stopped_at": "Phase 3",
                "resume_file": "GPD/phases/03/.continue-here.md",
            },
            store_root=store_root,
        )

        rows = list_recent_projects(store_root)

        assert len(rows) == 1
        assert rows[0].available is True
        assert rows[0].resume_file == "GPD/phases/03/.continue-here.md"
        assert rows[0].resume_file_available is False
        assert rows[0].resume_file_reason == "resume file missing"
        assert rows[0].resumable is False
