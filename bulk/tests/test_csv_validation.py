from django.core.files.uploadedfile import SimpleUploadedFile
from bulk.utils import validate_and_parse_csv
import pytest

def make_csv(content: str):
    return SimpleUploadedFile(
        "test.csv",
        content.encode("utf-8"),
        content_type="text/csv"
    )


def test_valid_csv():
    csv = make_csv(
        "name,address,phone\n"
        "Lion City,BLR 560011,9876543210\n"
    )

    rows = validate_and_parse_csv(csv)
    assert len(rows)==1
    assert rows[0]["name"]=="Lion City"


def test_missing_required_column():
    csv = make_csv("name,phone\nTest,123\n")
    with pytest.raises(ValueError):
        validate_and_parse_csv(csv)


def test_exceeds_max_rows():
    content = "name,address\n" + "\n".join(
        [f"H{i},Addr{i}" for i in range(25)]
    )
    csv = make_csv(content)
    with pytest.raises(ValueError):
        validate_and_parse_csv(csv)