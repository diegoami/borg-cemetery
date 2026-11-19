"""Named-parameter receipts, including borg-reborn-rs #520 class values."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from scenario_config import parameter_effective, settings

ROWS = {r['name']: r for r in [
    dict(name='attack_preference_melee_permille', value=1000, origin='default',
         class_values={'warrior': dict(value=1800, origin='borg.txt'),
                       'paladin': dict(value=1700, origin='environment')}),
    dict(name='town_heal_reserve_hp_percent', value=30, origin='borg.txt'),
    dict(name='danger_scale', value=120, origin='borg.txt'),
]}


class ParameterReceiptTest(unittest.TestCase):
    def test_common_parameter(self):
        self.assertTrue(parameter_effective('borg_param_danger_scale', 120, ROWS))
        self.assertFalse(parameter_effective('borg_param_danger_scale', 121, ROWS))
        self.assertFalse(parameter_effective('borg_param_unknown', 1, ROWS))

    def test_legacy_attack_preference_alias_is_a_class_value(self):
        self.assertTrue(parameter_effective('borg_param_attack_preference_warrior_melee_permille', 1800, ROWS))
        self.assertFalse(parameter_effective('borg_param_attack_preference_warrior_melee_permille', 1000, ROWS))
        self.assertFalse(parameter_effective('borg_param_attack_preference_mage_melee_permille', 1800, ROWS))
        # Set, but not from borg.txt.
        self.assertFalse(parameter_effective('borg_param_attack_preference_paladin_melee_permille', 1700, ROWS))

    def test_at_class_form(self):
        self.assertTrue(parameter_effective('borg_param_attack_preference_melee_permille@warrior', 1800, ROWS))
        self.assertFalse(parameter_effective('borg_param_attack_preference_melee_permille@mage', 1800, ROWS))
        self.assertFalse(parameter_effective('borg_param_attack_preference_melee_permille@wizard', 1800, ROWS))

    def test_suffix_alias_at_sentinel_sets_nothing(self):
        self.assertTrue(parameter_effective('borg_param_town_heal_reserve_hp_percent_mage', -1, ROWS))
        self.assertFalse(parameter_effective('borg_param_town_heal_reserve_hp_percent_mage', 40, ROWS))

    def test_settings_reads_at_class_lines(self):
        parsed = settings('borg_param_attack_preference_melee_permille@warrior = 1800\n')
        self.assertEqual(parsed, {'borg_param_attack_preference_melee_permille@warrior': 1800})


if __name__ == '__main__':
    unittest.main()
