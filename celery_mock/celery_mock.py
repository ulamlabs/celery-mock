# -*- coding: utf-8 -*-
from unittest import mock
from celery import Task, states
from celery.result import EagerResult
from celery.utils import uuid


class ALL(object):
    pass


class AlreadyMockedError(Exception):
    pass


class NotStartedError(Exception):
    pass


_super_apply_async = Task.apply_async
_mocked_tasks = dict()


class CeleryTaskMock(object):
    """
    Mocks celery task so that it won't get run until `runtasks` method call.

    >>> cmock = task_mock('myapp.tasks.dummy_task')
    >>> cmock.start()
    >>> mydummyfunction()  # triggers dummy_task
    >>> cmock.stop()  # runs dummy_task

    or

    >>> with task_mock('myapp.tasks.dummy_task'):
    >>>     mydummyfunction()  # triggers  dummy_task
    >>> # check_activation_status was automatically called
    """

    def __init__(self, taskname=ALL):
        self.taskname = taskname
        self.calls = []

    def start(self):
        try:
            _mocked_apply_async = _mocked_fn.start()
            _mocked_apply_async.side_effect = _apply_async
        except TypeError:
            pass
        already_mocked = (
            ALL in _mocked_tasks or
            self.taskname in _mocked_tasks or
            (self.taskname == ALL and _mocked_tasks)
        )
        if already_mocked:
            raise AlreadyMockedError()
        _mocked_tasks[self.taskname] = self
        return self

    def stop(self, run_tasks=True):
        if _mocked_tasks.get(self.taskname) != self:
            raise NotStartedError()

        if run_tasks:
            self.runtasks()
        del _mocked_tasks[self.taskname]

    def runtasks(self):
        while self.calls:
            task, args, kwargs = self.calls.pop(0)
            _super_apply_async(task, args=args, kwargs=kwargs)

    def __enter__(self):
        return self.start()

    def __exit__(self, *exc_info):
        self.stop()
        _mocked_fn.stop()


def _apply_async(selftask, a, kw=None, *args, **kwargs):
    tmock = _mocked_tasks.get(ALL) or _mocked_tasks.get(selftask.name)
    if tmock:
        tmock.calls.append((selftask, a, kw))
        return EagerResult(uuid(), None, states.PENDING)

    return _super_apply_async(selftask, *args, **kwargs)


_mocked_fn = mock.patch.object(
    Task, 'apply_async', autospec=True,
)
task_mock = CeleryTaskMock
del CeleryTaskMock
