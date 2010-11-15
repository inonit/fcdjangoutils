# Note, this library is free software
# Copyright 2010 FreeCode AS
# Licensed under the MIT license

from django import template
from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.utils import simplejson
import django.db.models.base

register = template.Library()

def nth_filter(value, param):
    try:
        if param not in value:
            return None
        return value[param]
    except:
        return getattr(value, param)

def eachnth_filter(value, param):
    return [nth_filter(part, param) for part in value]

def sum_filter(value):
    return reduce(lambda a,b: a+b, value)

def separateminus_filter(value1, value2):
    if not value1 and not value2:
        return "0"
    res = ''
    if value1:
        res += "%s" % (value1,)
    if value2:
        res += "-%s" % (value2,)
    return res

def aadd_filter(value1, value2):
    return value1 + value2

def jsonify_filter(object):
    def jsonify_models(obj):
        if isinstance(obj, django.db.models.base.Model):
            return simplejson.loads(serialize('json', [obj]))[0]
        elif isinstance(obj, QuerySet):
            return simplejson.loads(serialize('json', obj))
        else:
            return obj
    return simplejson.dumps(object, default=jsonify_models)

register.filter('jsonify', jsonify_filter)
register.filter('nth', nth_filter)
register.filter('eachnth', eachnth_filter)
register.filter('sum', sum_filter)
register.filter('separateminus', separateminus_filter)
register.filter('aadd', aadd_filter)
