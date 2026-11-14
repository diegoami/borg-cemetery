"""Project item descriptions and spell availability from recorded observations."""
import gzip
import json

from run_batch import write_json
from human_readable import spells


def lines(path):
    if not path.exists():
        return
    opener = gzip.open if path.suffix == '.gz' else open
    with opener(path, 'rt') as stream:
        for number, line in enumerate(stream, 1):
            try:
                yield number, json.loads(line)
            except ValueError:
                continue


def observations(raw):
    path = raw / 'observations.jsonl'
    if not path.exists():
        path = raw / 'observations.jsonl.gz'
    if path.exists():
        for number, row in lines(path):
            if not isinstance(row.get('turn'), int):
                continue
            def item(value):
                return {key: value[key] for key in ('desc', 'number', 'aware', 'fully_known') if key in value}
            yield dict(turn=row['turn'], source=path.name, line=number,
                       pack=[item(i) for i in row.get('inventory', [])],
                       equipment=[dict(slot=s.get('slot_type'), item=item(s['item']) if s.get('item') else None)
                                  for s in row.get('equipment', [])],
                       quiver=[item(i) for i in row.get('quiver', [])],
                       spells=row.get('spells', []))
        return
    inventory, spells = None, None
    for number, row in lines(raw / 'frames.jsonl'):
        if row.get('inventory') is not None:
            inventory = row['inventory']
        if row.get('spells') is not None:
            spells = row['spells']
        if inventory is not None:
            yield dict(turn=row['turn'], source='frames.jsonl', line=number,
                       pack=inventory.get('pack', []), equipment=inventory.get('equipment', []),
                       quiver=inventory.get('quiver', []), spells=spells)


def description(item):
    if item.get('item') is not None:
        item = item['item']
    text = item.get('desc', item.get('description', '(empty slot)'))
    return f"{item['number']} × {text}" if 'number' in item else text


def extract_inventory(raw, dest, start, end):
    selected, before, previous, last = [], None, None, None
    for row in observations(raw):
        if row['turn'] > end:
            break
        last = row
        if row['turn'] <= start:
            before = row
            continue
        if not selected and before:
            selected.append(before)
            previous = {k: before[k] for k in ('pack', 'equipment', 'quiver', 'spells')}
        signature = {k: row[k] for k in ('pack', 'equipment', 'quiver', 'spells')}
        if signature != previous:
            selected.append(row)
            previous = signature
    if not selected and before:
        selected = [before]
    if last and (not selected or last['line'] != selected[-1]['line']):
        selected.append(last)
    result = dict(schema='borg-cemetery/episode-inventory@1', status='available' if selected else 'not_recorded',
                  scope='Last observed inventory at/before start, then observed changes. Descriptions follow player knowledge.',
                  start_turn=start, end_turn=end, snapshots=selected,
                  terminal_inventory='last available observation; not asserted to be post-death')
    write_json(dest / 'inventory.json', result)
    render_inventory(result, dest / 'inventory.md')
    return result


def render_inventory(result, path):
    selected = result.get('snapshots', [])
    text = ['# Inventory, equipment and spells', '', result['scope'], '',
            'The final entry is the last observed inventory, not an invented post-death snapshot. '
            'Only learned spells are listed; casting also requires enough mana, the book and a legal target.', '']
    if not selected:
        text += ['Inventory was not recorded by this build/run.', '']
    for row in selected:
        text += [f"## Turn {row['turn']} (recorded observation {row['line']})", '']
        for key in ('pack', 'equipment', 'quiver'):
            text += [key.capitalize() + ':', '']
            present = [item for item in row[key] if item.get('item', True) is not None]
            text += ['- ' + description(item) for item in present] or ['- (none)']
            text += ['']
        text += ['Learned spells:', '', *spells(row['spells']), '']
    path.write_text('\n'.join(text))
