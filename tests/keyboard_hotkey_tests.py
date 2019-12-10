# coding=utf-8
# pystray
# Copyright (C) 2015-2019 Moses Palmér
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import contextlib
import locale
import sys
import threading
import unittest

from pynput.keyboard import HotKey, Key as k, KeyCode as kc


class KeyboardHotKeyTest(unittest.TestCase):
    def test_parse_invalid(self):
        with self.assertRaises(ValueError) as e:
            HotKey.parse('invalid')
        self.assertEqual(e.exception.args, ('invalid',))

        with self.assertRaises(ValueError) as e:
            HotKey.parse('a+')
        self.assertEqual(e.exception.args, ('a+',))

        with self.assertRaises(ValueError) as e:
            HotKey.parse('<ctrl>+<halt>')
        self.assertEqual(e.exception.args, ('<halt>',))

        with self.assertRaises(ValueError) as e:
            HotKey.parse('<ctrl>+a+a')
        self.assertEqual(e.exception.args, ('<ctrl>+a+a',))

        with self.assertRaises(ValueError) as e:
            HotKey.parse('<ctrl>+a+A')
        self.assertEqual(e.exception.args, ('<ctrl>+a+A',))

    def test_parse_valid(self):
        self.assertSetEqual(
            HotKey.parse('a'),
            {
                kc.from_char('A')})
        self.assertSetEqual(
            HotKey.parse('<ctrl>+a'),
            {
                k.ctrl,
                kc.from_char('A')})
        self.assertSetEqual(
            HotKey.parse('<ctrl>+<alt>+a'),
            {
                k.ctrl,
                k.alt,
                kc.from_char('A')})

    def test_activate_single(self):
        activations = []
        def on_activate():
            activations.append(True)

        hk = HotKey({kc.from_char('a')}, on_activate)

        hk.press(kc.from_char('b'))
        self.assertEqual(0, len(activations))
        hk.release(kc.from_char('b'))
        self.assertEqual(0, len(activations))

        hk.press(kc.from_char('a'))
        self.assertEqual(1, len(activations))
        hk.release(kc.from_char('a'))
        self.assertEqual(1, len(activations))

        hk.press(kc.from_char('a'))
        self.assertEqual(2, len(activations))
        hk.press(kc.from_char('a'))
        self.assertEqual(2, len(activations))
        hk.release(kc.from_char('a'))
        self.assertEqual(2, len(activations))

        hk.press(kc.from_char('A'))
        self.assertEqual(3, len(activations))
        hk.release(kc.from_char('A'))
        self.assertEqual(3, len(activations))

    def test_activate_combo(self):
        activations = []
        def on_activate():
            activations.append(True)

        hk = HotKey({k.ctrl, kc.from_char('a')}, on_activate)

        hk.press(kc.from_char('b'))
        self.assertEqual(0, len(activations))
        hk.release(kc.from_char('b'))
        self.assertEqual(0, len(activations))

        hk.press(kc.from_char('a'))
        self.assertEqual(0, len(activations))
        hk.release(kc.from_char('a'))
        self.assertEqual(0, len(activations))

        hk.press(k.ctrl)
        self.assertEqual(0, len(activations))
        hk.release(k.ctrl)
        self.assertEqual(0, len(activations))

        hk.press(kc.from_char('a'))
        hk.press(k.ctrl)
        self.assertEqual(1, len(activations))
        hk.press(kc.from_char('a'))
        hk.press(k.ctrl)
        self.assertEqual(1, len(activations))
        hk.release(k.ctrl)
        hk.press(k.ctrl)
        self.assertEqual(2, len(activations))
        hk.release(kc.from_char('a'))
        hk.press(kc.from_char('a'))
        self.assertEqual(3, len(activations))
