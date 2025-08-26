#!/usr/bin/env python3
"""Validate _data/store-data.csv structure.
Rules:
- Exactly 4 columns per non-empty, non-comment line.
- Header must match expected columns.
- Warn if duplicate (comandos, grupo) pair.
- Fail on unescaped double quotes inside fields.
Exit codes:
 0 success, 1 errors found.
"""
from __future__ import annotations
import csv, sys, pathlib, re

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = REPO_ROOT / '_data' / 'store-data.csv'
EXPECTED_HEADER = ['comandos','descricao','categoria','grupo']

errors: list[str] = []
warnings: list[str] = []

def main():
    if not CSV_PATH.exists():
        errors.append(f'Missing file: {CSV_PATH}')
        return finish()

    raw = CSV_PATH.read_text(encoding='utf-8').splitlines()
    if not raw:
        errors.append('CSV is empty')
        return finish()

    # Quick sanity: header must be first line exactly
    header_line = raw[0].strip('\ufeff')  # remove BOM if any
    if header_line.replace(' ', '') != ','.join(EXPECTED_HEADER):
        errors.append(f'Header mismatch. Got: {header_line!r} Expected: {",".join(EXPECTED_HEADER)!r}')
        return finish()

    seen = set()
    reader = csv.reader(raw)
    for idx, row in enumerate(reader):
        line_no = idx + 1
        if idx == 0:
            continue
        if not row or all(not c.strip() for c in row):
            errors.append(f'Line {line_no}: blank/empty line not allowed')
            continue
        # Accept separator/comment lines starting with '#'
        first = row[0].strip()
        if first.startswith('#'):
            continue
        if len(row) != 4:
            errors.append(f'Line {line_no}: expected 4 columns, got {len(row)} -> {row}')
            continue
        comandos, descricao, categoria, grupo = row
        # Basic quote check: unbalanced double quotes within field (very naive)
        for field in row:
            if field.count('"') == 1:
                errors.append(f'Line {line_no}: unbalanced double quote in field {field!r}')
        key = (comandos.strip(), grupo.strip())
        if key in seen:
            warnings.append(f'Line {line_no}: duplicate command+group {key}')
        else:
            seen.add(key)
        # Simple category normalization suggestion
        if categoria and categoria != categoria.upper() and ' ' in categoria:
            warnings.append(f'Line {line_no}: category not normalized (consider title case or uppercase): {categoria!r}')

    finish()

def finish():
    if warnings:
        print('WARNINGS:')
        for w in warnings:
            print('  -', w)
    if errors:
        print('ERRORS:')
        for e in errors:
            print('  -', e)
        sys.exit(1)
    print('CSV validation passed with', len(warnings), 'warnings.')

if __name__ == '__main__':
    main()
