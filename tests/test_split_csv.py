from os.path import join

from csv_diff import compare, load_csv
from csv_splitter import split_csv

from .settings import DATA_PATH


def test_split_csv(tmpdir):
    source = join(DATA_PATH, "source_01.csv")
    dest_path = tmpdir.mkdir("dest")
    destinations = (
        dest_path.join("actual_x_01.csv"),
        dest_path.join("actual_y_01.csv"),
    )
    split_csv(
        source,
        var_name="language_code",
        separator="::",
        destinations=destinations,
    )
    diff = compare(
        load_csv(open(join(DATA_PATH, "expected_x_01.csv")), key="id"),
        load_csv(open(destinations[0]), key="id"),
    )
    assert not any(list(diff.values()))
    diff = compare(
        load_csv(open(join(DATA_PATH, "expected_y_01.csv")), key="id"),
        load_csv(open(destinations[1]), key="id"),
    )
    assert not any(list(diff.values()))
