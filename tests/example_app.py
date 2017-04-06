from celery import Celery


celery_app = Celery()
celery_app.conf.CELERY_ALWAYS_EAGER = True


class DB(dict):
    def __init__(self, *a, **kw):
        super(DB, self).__init__(*a, **kw)
        self.reset()

    def reset(self):
        self['rows'] = []


db = DB()


@celery_app.task()
def dummytask1(*args, **kwargs):
    db['rows'].append('1')


@celery_app.task
def dummytask2(*args, **kwargs):
    db['rows'].append('2')


@celery_app.task
def dummytask_args_kwargs(*args, **kwargs):
    db['rows'].append((args, kwargs))


def dummymethod1(*args, **kwargs):
    dummytask1.s(*args, **kwargs).delay()


def dummymethod2(*args, **kwargs):
    dummytask2.s(*args, **kwargs).delay()


def dummymethod_args_kwargs(*args, **kwargs):
    dummytask_args_kwargs.s(*args, **kwargs).delay()
