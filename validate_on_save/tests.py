# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.core.exceptions import ValidationError
from django.test import TestCase
from validate_on_save.models import PickyModel


class ValidateOnSaveTests(TestCase):
    def test_full_clean_called(self):
        picky = PickyModel()
        with self.assertRaises(ValidationError):
            picky.save()
