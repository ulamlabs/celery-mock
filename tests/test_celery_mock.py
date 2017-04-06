#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_celery_mock
----------------------------------

Tests for `celery_mock` module.
"""

import pytest

from celery_mock import task_mock
from celery_mock.celery_mock import AlreadyMockedError, NotStartedError
from .example_app import (
    db,
    dummymethod1,
    dummymethod2,
    dummymethod_args_kwargs,
)


@pytest.yield_fixture(autouse=True)
def reset_db():
    db.reset()
    yield


def test_context_manager():
    dummymethod1()

    assert db['rows'] == ['1']

    with task_mock():
        dummymethod1()
        dummymethod1()
        assert db['rows'] == ['1']

    assert db['rows'] == ['1', '1', '1']

    dummymethod1()

    assert db['rows'] == ['1', '1', '1', '1']


def test_start_stop():
    tmock = task_mock()

    dummymethod1()
    assert db['rows'] == ['1']

    tmock.start()
    dummymethod1()
    dummymethod1()
    assert db['rows'] == ['1']
    tmock.stop()
    assert db['rows'] == ['1', '1', '1']

    dummymethod1()

    assert db['rows'] == ['1', '1', '1', '1']


def test_mock_single_task():
    dummymethod1()
    dummymethod2()

    assert db['rows'] == ['1', '2']

    with task_mock('tests.example_app.dummytask1'):
        dummymethod1()
        dummymethod2()
        assert db['rows'] == ['1', '2', '2']

    assert db['rows'] == ['1', '2', '2', '1']

    dummymethod1()
    dummymethod2()

    assert db['rows'] == ['1', '2', '2', '1', '1', '2']


def test_mock_both_tasks():
    tmock1 = task_mock('tests.example_app.dummytask1').start()
    tmock2 = task_mock('tests.example_app.dummytask2').start()

    dummymethod1()
    dummymethod2()

    assert db['rows'] == []

    tmock2.stop()

    assert db['rows'] == ['2']

    tmock1.stop()

    assert db['rows'] == ['2', '1']


def test_call_arguments_assertion():
    with task_mock('tests.example_app.dummytask1') as tmock1:
        with task_mock('tests.example_app.dummytask2') as tmock2:
            dummymethod2('22', b='bb')
            assert len(tmock1.calls) == 0
            assert len(tmock2.calls) == 1
            task, args, kwargs = tmock2.calls[0]
            assert task.name == 'tests.example_app.dummytask2'
            assert args == ('22',)
            assert kwargs == {'b': 'bb'}
            dummymethod1('11', a='aa')
        assert db['rows'] == ['2']
        assert len(tmock1.calls) == 1
        assert len(tmock2.calls) == 0
        task, args, kwargs = tmock1.calls[0]
        assert task.name == 'tests.example_app.dummytask1'
        assert args == ('11',)
        assert kwargs == {'a': 'aa'}
    assert db['rows'] == ['2', '1']
    assert len(tmock1.calls) == 0
    assert len(tmock2.calls) == 0


def test_call_args():
    with task_mock('tests.example_app.dummytask_args_kwargs'):
        dummymethod_args_kwargs('a1', a='aa1')
        dummymethod_args_kwargs('a2', a='aa2')
        dummymethod_args_kwargs('a3', a='aa3')

    assert db['rows'] == [
        (('a1',), {'a': 'aa1'}),
        (('a2',), {'a': 'aa2'}),
        (('a3',), {'a': 'aa3'}),
    ]


def test_exceptions():
    tmock = task_mock().start()
    with pytest.raises(AlreadyMockedError):
        task_mock().start()

    with pytest.raises(NotStartedError):
        task_mock().stop()
    tmock.stop()
    task_mock().start()

    with pytest.raises(AlreadyMockedError):
        task_mock().start()

    with pytest.raises(AlreadyMockedError):
        task_mock('tests.example_app.dummytask_args_kwargs').start()
