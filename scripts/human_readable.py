"""Render recorded facts as prose and tables, never serialized data dumps."""
import re


DIRECTIONS = {1: 'southwest', 2: 'south', 3: 'southeast', 4: 'west',
              5: 'in place', 6: 'east', 7: 'northwest', 8: 'north', 9: 'northeast'}


def action(choice):
    value = str(choice or 'No choice recorded')
    move = re.fullmatch(r'(Walk|Melee|Run|Alter)\((\d)\)', value)
    if move:
        verb = {'Walk': 'Move', 'Melee': 'Attack', 'Run': 'Run', 'Alter': 'Interact'}[move[1]]
        return f'{verb} {DIRECTIONS.get(int(move[2]), "in an unspecified direction")}'
    rest = re.fullmatch(r'Rest\((\d+)\)', value)
    if rest:
        return f'Rest, requesting {rest[1]} player turns'
    cast = re.search(r'Cast.*book: (\d+).*letter: (?:Some\()?(\d+)', value)
    if cast:
        letter = chr(int(cast[2])) if 97 <= int(cast[2]) <= 122 else '?'
        return f'Cast spell {letter} from book {int(cast[1]) + 1}' + (' with an aimed target' if 'aim: true' in value else '')
    item = re.search(r'^(\w+)\s*\{.*item: (\d+)', value)
    if item:
        verbs = {'Read': 'Read a scroll', 'Quaff': 'Drink a potion', 'Eat': 'Eat',
                 'Wear': 'Equip an item', 'Wield': 'Wield an item', 'Use': 'Use an item'}
        return f'{verbs.get(item[1], item[1])} (carried item {int(item[2]) + 1})'
    # Unknown future variants remain reported, without Rust object syntax.
    return re.sub(r'\s+', ' ', value.replace('{', '(').replace('}', ')').replace('Some(', '(')).strip()


def threat(value):
    if not isinstance(value, dict) or not value:
        return 'Threat estimate not recorded'
    parts = []
    for key, label in (('expected', 'expected damage'), ('worst', 'worst estimated damage')):
        if isinstance(value.get(key), (int, float)):
            parts.append(f'{label} {value[key]:.1f} HP')
    if isinstance(value.get('p_death'), (int, float)):
        parts.append(f"estimated death chance {value['p_death']:.0%}")
    return '; '.join(parts) or 'No quantified threat estimate recorded'


def spells(rows):
    """The observation format supplies book/letter identities, not spell names."""
    if not isinstance(rows, list):
        return ['Spell availability was not retained in a supported readable form.']
    known, positions = [], {}
    for row in rows:
        book = row.get('book', 0)
        position = positions.get(book, 0)
        positions[book] = position + 1
        if not row.get('flags', 0) & 1:
            continue
        name = row.get('name') or f'Book {book + 1}, spell {chr(97 + position)}'
        state = 'Forgotten; cannot cast' if row.get('flags', 0) & 4 else 'Learned'
        known.append(f"| {name} | {row.get('mana', 'Unknown')} | {row.get('fail', 'Unknown')}% | {state} |")
    if not known:
        return ['No learned spells were recorded.']
    return ['| Learned spell | Mana cost | Failure chance | Knowledge |',
            '| --- | --- | --- | --- |', *known, '',
            'Casting still requires the book, enough mana and a legal target. '
            'Spell names were not captured when only a book and menu letter are shown.']


def clean_kind(value):
    return str(value).replace('& ', '').replace('~', '').strip()
