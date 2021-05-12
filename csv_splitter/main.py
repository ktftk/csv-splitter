import csv
from os.path import splitext
from typing import Dict, List, Optional, Tuple

Records = List[Dict[str, str]]

Columns = List[str]


def split_csv(
    filepath: str,
    var_name: str,
    separator: str,
    primary_key: Optional[Columns] = None,
    suffixes: Tuple[str, str] = ("_x", "_y"),
) -> None:
    records = _read_csv(filepath)
    columns = list(records[0].keys())
    if not _check_splittable(columns, separator):
        return
    _split_primary(
        records,
        columns,
        separator,
        f"{splitext(filepath)[0]}{suffixes[0]}.csv",
    )
    _split_secondary(
        records,
        columns,
        var_name,
        separator,
        primary_key,
        f"{splitext(filepath)[0]}{suffixes[1]}.csv",
    )


def _read_csv(filepath: str) -> Records:
    with open(filepath) as f:
        reader = csv.DictReader(f)
        records = [record for record in reader]
    return records


def _write_csv(filepath: str, columns: Columns, records: Records) -> None:
    with open(filepath, "w") as f:
        writer = csv.DictWriter(f, columns, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)


def _check_splittable(columns: Columns, separator: str) -> bool:
    if len(list(filter(lambda x: separator in x, columns))) == 0:
        return False
    return True


def _split_primary(
    records: Records, columns: Columns, separator: str, filepath: str
) -> None:
    _write_csv(filepath, _get_primary_columns(columns, separator), records)


def _get_primary_columns(columns: Columns, separator: str) -> Columns:
    return list(filter(lambda x: separator not in x, columns))


def _split_secondary(
    records: Records,
    columns: Columns,
    var_name: str,
    separator: str,
    primary_key: Optional[Columns],
    filepath: str,
) -> None:
    attributes = _get_secondary_attributes(columns, separator)
    if primary_key is None:
        primary_key = [columns[0]]
    var_values = _get_var_values(columns, separator)
    new_records = []
    for record in records:
        for var_value in var_values:
            new_record = {}
            new_record.update(
                {column: record[column] for column in primary_key}
            )
            new_record[var_name] = var_value
            for attribute in attributes:
                new_record[attribute] = record.get(
                    f"{attribute}{separator}{var_value}", ""
                )
            new_records.append(new_record)
    new_columns = primary_key + [var_name] + attributes
    _write_csv(filepath, new_columns, new_records)


def _get_secondary_attributes(columns: Columns, separator: str) -> List[str]:
    result = []
    for column in columns:
        if separator in column:
            result.append(column.split(separator)[0])
    return list(dict.fromkeys(result))


def _get_var_values(columns: Columns, separator: str) -> List[str]:
    result = []
    for column in columns:
        if separator in column:
            result.append(column.split(separator)[1])
    return list(dict.fromkeys(result))
