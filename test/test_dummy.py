"""LICENSE
Copyright 2017 Hermann Krumrey

This file is part of ci-scripts.

ci-scripts is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

ci-scripts is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with ci-scripts.  If not, see <http://www.gnu.org/licenses/>.
LICENSE"""


from unittest import TestCase


class DummyTests(TestCase):
    """
    A dummy test case
    """

    def test_dummy(self):
        """
        A dummy test method
        :return: None
        """
        self.assertEqual(True, True)
