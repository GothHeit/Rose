import unittest

from state import SharedState
from threads.utilities.skin_name_resolver import SkinNameResolver


class CustomModFallbackTests(unittest.TestCase):
    """A selected custom mod names its own target skin when no skin was hovered"""

    @staticmethod
    def _resolve(champion_id=429, **state_values):
        state = SharedState()
        state.locked_champ_id = champion_id
        for key, value in state_values.items():
            setattr(state, key, value)
        return SkinNameResolver(state).resolve_injection_name()

    def test_uses_the_mod_target_when_nothing_was_hovered(self):
        mod = {'skin_id': 429000, 'champion_id': 429}
        self.assertEqual(self._resolve(selected_custom_mod=mod), 'skin_429000')

    def test_hovered_skin_still_wins(self):
        mod = {'skin_id': 429000, 'champion_id': 429}
        name = self._resolve(selected_custom_mod=mod, last_hovered_skin_id=429001)
        self.assertEqual(name, 'skin_429001')

    def test_ignores_a_mod_from_another_champion(self):
        mod = {'skin_id': 103000, 'champion_id': 103}
        self.assertIsNone(self._resolve(selected_custom_mod=mod))

    def test_no_mod_and_no_hovered_skin_resolves_nothing(self):
        self.assertIsNone(self._resolve())


if __name__ == '__main__':
    unittest.main()
