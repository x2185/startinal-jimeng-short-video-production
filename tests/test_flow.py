from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ai_video_factory.db import connect
from ai_video_factory.ingest import ingest_folder
from ai_video_factory.memory import add_memory, retrieve


class FactoryFlowTests(unittest.TestCase):
    def test_ingest_deduplicates_and_retrieves_approved_product_memory(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source" / "real-footage" / "unboxing"
            source.mkdir(parents=True)
            (source / "clip.mp4").write_bytes(b"same media")
            (source / "copy.mp4").write_bytes(b"same media")
            connection = connect(root / "factory.db")
            result = ingest_folder(connection, "toy-001", root / "source")
            self.assertEqual({"indexed": 1, "duplicates": 1, "ignored": 0}, result)
            add_memory(
                connection,
                "toy-001",
                "performance_rule",
                "Show the completed build in the first two seconds.",
                "August TikTok retention export, 12 creatives",
                "approved",
            )
            add_memory(
                connection,
                "toy-001",
                "performance_rule",
                "Unverified idea",
                "No data",
                "candidate",
            )
            memories = retrieve(connection, "toy-001", "completed build retention")
            self.assertEqual(1, len(memories))
            self.assertIn("completed build", memories[0]["content"])
            connection.close()


if __name__ == "__main__":
    unittest.main()
