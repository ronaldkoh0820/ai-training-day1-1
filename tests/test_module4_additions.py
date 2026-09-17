import unittest

from device_test_guard.disposition import decide_disposition
from device_test_guard.models import DeviceTestRecord
from device_test_guard.validation import validate_record


def record(
    device_id: str,
    passed: bool = True,
    voltage: float = 1.0,
    retest_count: int = 0,
) -> DeviceTestRecord:
    return DeviceTestRecord(
        device_id,
        25.0,
        voltage,
        {"logic": passed},
        retest_count,
    )


class Module4AdditionalTests(unittest.TestCase):
    def test_voltage_boundaries_are_inclusive(self):
        self.assertEqual(validate_record(record("VOLTAGE_LOW", voltage=0.8)), ())
        self.assertEqual(validate_record(record("VOLTAGE_HIGH", voltage=1.2)), ())

    def test_exhausted_retest_is_held(self):
        batch = [record("PASS", passed=True), record("FAIL", passed=False, retest_count=1)]
        self.assertEqual(decide_disposition(batch, 90.0)[0], "HOLD")

    def test_invalid_record_is_held(self):
        self.assertEqual(decide_disposition([record("INVALID", voltage=1.5)], 90.0)[0], "HOLD")
