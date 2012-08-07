# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.db import models
from django.db.models.loading import get_app, get_models


__version__ = '1.0.0'


def validate_models_on_save(app_name):
    """
    Make all models in app_name be validated during their save() method
    (surprisingly, this does not happen by default, apparently for backwards
    compatibility reasons:
    http://stackoverflow.com/questions/4441539/why-doesnt-djangos-model-save-call-full-clean).
    """
    app = get_app(app_name)
    for model in get_models(app):
        validate_model_on_save(model)


def validate_model_on_save(model):
    """
    Make a model be validated during its save() method.

    model: a model class.
    """
    models.signals.pre_save.connect(_validate, sender=model)


def _validate(sender, signal, instance, raw, using, **kwargs):
    if not raw:
        instance.full_clean()
