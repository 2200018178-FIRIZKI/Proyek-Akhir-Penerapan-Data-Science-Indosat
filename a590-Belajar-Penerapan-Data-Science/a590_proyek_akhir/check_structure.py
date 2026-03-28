#!/usr/bin/env python3
import json

with open('notebook.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print('📋 CURRENT NOTEBOOK STRUCTURE:')
print('=' * 70)
count = 1
for i, cell in enumerate(nb['cells']):
    if cell['cell_type'] == 'markdown':
        content = ''.join(cell.get('source', []))
        if content.strip().startswith('#'):
            heading = content.split('\n')[0].strip()
            print(f'{count}. Cell {i+1}: {heading}')
            count += 1
    elif cell['cell_type'] == 'code':
        lines = len(cell.get('source', []))
        print(f'   ↳ Code Cell {i+1}: {lines} lines')

print("\n" + "=" * 70)
print(f"Total cells: {len(nb['cells'])}")
