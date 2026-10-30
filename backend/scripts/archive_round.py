#!/usr/bin/env python3
"""Script to archive the current voting database and export a summary report."""
import argparse
import json
import os
import shutil
import sys
from datetime import datetime

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
BACKEND_DIR = os.path.join(REPO_ROOT, "backend")
sys.path.insert(0, BACKEND_DIR)

from sqlmodel import Session, select
from app.db import engine
from app.models.file import VoteFile
from app.models.vote import Vote
ARCHIVE_DIR = os.path.join(BACKEND_DIR, "archive")
LOCAL_DB_PATH = os.path.join(BACKEND_DIR, "voting.db")


def archive_current_round(round_num: int = 1):
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_db_name = f"voting_round_{round_num}_{timestamp_str}.db"
    archive_db_path = os.path.join(ARCHIVE_DIR, archive_db_name)

    print(f"Archiving round {round_num} data...")

    # 1. Snapshot database file if it exists
    if os.path.exists(LOCAL_DB_PATH):
        shutil.copy2(LOCAL_DB_PATH, archive_db_path)
        print(f"  ✓ Database snapshot saved to: {os.path.relpath(archive_db_path, REPO_ROOT)}")
    else:
        print(f"  Notice: No local db file at {LOCAL_DB_PATH}")

    # 2. Export summary report
    with Session(engine) as session:
        votes = session.exec(select(Vote)).all()
        files = session.exec(select(VoteFile)).all()

        by_figure: dict[str, int] = {}
        by_palette: dict[str, int] = {}
        by_position: dict[str, int] = {}
        recommendations_list: list[dict] = []

        file_map = {f.vote_id: f for f in files}

        for v in votes:
            by_figure[v.figure_id] = by_figure.get(v.figure_id, 0) + 1
            by_palette[v.palette_id] = by_palette.get(v.palette_id, 0) + 1
            by_position[v.position_id] = by_position.get(v.position_id, 0) + 1
            att = file_map.get(v.id) if v.id is not None else None

            if v.rationale or att:
                recommendations_list.append({
                    "student_id": v.student_id,
                    "figure_id": v.figure_id,
                    "rationale": v.rationale,
                    "has_attachment": att is not None,
                    "attachment_name": att.filename if att else None,
                    "attachment_size": att.file_size if att else None,
                })

        summary = {
            "round": round_num,
            "archived_at": datetime.now().isoformat(),
            "total_votes": len(votes),
            "total_attachments": len(files),
            "distribution": {
                "by_figure": by_figure,
                "by_palette": by_palette,
                "by_position": by_position,
            },
            "feedback_and_attachments": recommendations_list,
        }

        summary_name = f"summary_round_{round_num}_{timestamp_str}.json"
        summary_path = os.path.join(ARCHIVE_DIR, summary_name)
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"  ✓ Round summary report saved to: {os.path.relpath(summary_path, REPO_ROOT)}")


def main():
    parser = argparse.ArgumentParser(description="Archive voting round database and summaries.")
    parser.add_argument("--round", "-r", type=int, default=1, help="Round number to archive")
    args = parser.parse_args()
    archive_current_round(args.round)


if __name__ == "__main__":
    main()
