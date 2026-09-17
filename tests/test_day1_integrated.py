import unittest

from device_test_guard.models import DeviceTestRecord
from device_test_guard.service import analyse_batch
from device_test_guard.validation import validate_record


def record(
    device_id: str,
    temperature_c: float = 25.0,
    test_results: dict[str, bool] | None = None,
) -> DeviceTestRecord:
    return DeviceTestRecord(
        device_id,
        temperature_c,
        1.0,
        {"logic": True} if test_results is None else test_results,
    )


class Day1IntegratedTests(unittest.TestCase):
    def test_temperature_just_outside_range_is_rejected(self):
        for temperature_c in (9.99, 85.01):
            with self.subTest(temperature_c=temperature_c):
                self.assertIn(
                    "temperature is outside the training range",
                    validate_record(record("DAY1-TEMP", temperature_c=temperature_c)),
                )

    def test_blank_device_identifier_is_rejected(self):
        self.assertIn(
            "device_id is required",
            validate_record(record("   ")),
        )

    def test_empty_test_results_are_rejected(self):
        self.assertIn(
            "at least one test result is required",
            validate_record(record("DAY1-EMPTY", test_results={})),
        )

    def test_empty_batch_summary_is_zero_and_held(self):
        summary = analyse_batch("DAY1-EMPTY-BATCH", [])
        self.assertEqual(summary.record_count, 0)
        self.assertEqual(summary.yield_percent, 0.0)
        self.assertEqual(summary.disposition, "HOLD")


if __name__ == "__main__":
    unittest.main()
