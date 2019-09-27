# coding: utf-8
from collections import namedtuple

from ability import Ability, Target
from building import Category
from common import Status, IncomeUp

Info = namedtuple('Info', ('name', 'ability'))


infos = [
    Info('一带一路建设', Ability(Target.All, (None, None, None, 0.75, 1.0))),
    Info('自由贸易区建设', Ability(Target.Business, (None, None, 1.5, 2.25, None))),
    Info('区域协调发展', Ability(Target.House, (None, None, 1.5, None, None))),

    Info('全面深化改革', Ability(Target.All, (0.2, None, None, None, None))),
    Info('全面依法治国', Ability(Target.All, (0.2, None, None, None, None),
                           Status.OnlineOnly)),
    Info('科教兴国', Ability(Target.All, (0.2, None, None, None, None),
                         Status.OfflineOnly)),
    Info('创新驱动', Ability(Target.Industry, (0.6, None, None, None, None))),
]

infos = {info.name: info for info in infos}


class Policy(object):
    def __init__(self, name, level):
        self.info = infos[name]
        self.level = level

    def trigger(self, building, online):
        for value in self.info.ability.trigger(building, online):
            yield IncomeUp(self.info.name, value[self.level - 1])


class Light(object):
    def __init__(self, value):
        self.value = value

    def trigger(self, building, online):
        yield IncomeUp('家国之光', self.value)


class PolicySet(object):
    def __init__(self, *policies):
        self.policies = policies

    def trigger(self, building, online):
        for policy in self.policies:
            for value in policy.trigger(building, online):
                yield value
