# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.core.exceptions import ValidationError
from django.db import models
import validate_on_save


class PickyModel(models.Model):
    """
    A model that always raises a ValidationError in full_clean(). Just for
    use by validate_on_save's tests, to make sure that full_clean() is being
    called.
    """

    def full_clean(self, *args, **kwargs):
        super(PickyModel, self).full_clean(*args, **kwargs)
        raise ValidationError("This data isn't good enough!")


validate_on_save.validate_models_on_save('validate_on_save')
