# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from distutils.version import StrictVersion
import django

__version__ = '1.1.3'


def django_gte_17():
    return StrictVersion(django.get_version()) >= StrictVersion('1.7')


def django_allows_app_config():
    return django_gte_17()


if django_allows_app_config():
    default_app_config = 'validate_on_save.apps.ValidateOnSaveConfig'


def validate_models_on_save(app_name):
    """
    Make all models in app_name be validated during their save() method
    (surprisingly, this does not happen by default, apparently for backwards
    compatibility reasons:
    http://stackoverflow.com/questions/4441539/why-doesnt-djangos-model-save-call-full-clean).
    """

    if django_gte_17():
        _validate_models_on_save_post_17(app_name)
    else:
        _validate_models_on_save_pre_17(app_name)


def _validate_models_on_save_post_17(app_name):
    from django.apps import apps
    app_config = apps.get_app_config(app_name)
    for model in app_config.get_models():
        validate_model_on_save(model)


def _validate_models_on_save_pre_17(app_name):
    """
    On Django < 1.7 we don't want all the apps to be loaded when the method is
    being called for a specific app. It causes circular dependencies when apps
    are trying to load stuff themselves through the template app loaders.

    This is evident when running South management commands. For some reason they
    load the template loaders which import all the apps which could import
    something like haystack which imports all the indexes which could be part of
    the models class of an app which uses validate on save in the models which
    will load all the apps in order to get the models which loads debug toolbar
    which calls a reverse on a url which loads all the context which may load
    the template loaders again in the case of djangocms causing a circular
    dependency.
    """
    from django.db.models.loading import load_app, cache, get_models, get_app

    load_app(app_name)
    loaded_models = cache.app_models[app_name]
    for (key, model) in loaded_models.items():
        validate_model_on_save(model)


def validate_model_on_save(model):
    """
    Make a model be validated during its save() method.

    model: a model class.
    """
    django.db.models.signals.pre_save.connect(_validate, sender=model)


def _validate(sender, signal, instance, raw, using, **kwargs):
    if not raw:
        instance.full_clean()
