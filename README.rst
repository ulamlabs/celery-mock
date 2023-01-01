===============================
Celery Task Mocking
===============================


.. image:: https://img.shields.io/pypi/v/celery-mock.svg
        :target: https://pypi.python.org/pypi/celery-mock

.. image:: https://img.shields.io/travis/ulamlabs/celery-mock.svg
        :target: https://travis-ci.org/ulamlabs/celery-mock

.. image:: https://codecov.io/gh/ulamlabs/celery-mock/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/ulamlabs/celery-mock


celery-mock allows you to mock celery task and then run them when you want

Rationale
==========

Sometimes a celery task retries itself to wait for some event or model to change.
This is hard to test because celery tasks run (and retry) inline in tests.
Now you can choose when to run your tasks.

Supported versions
==================

- Python 3 support
- Celery 3.1.x and 4.0.x support 


How to install
================

    .. code-block:: bash
    
        pip install celery-mock


How to use
==========

    .. code-block:: python
    
        from celery_mock import task_mock
        from django.test import TestCase, Client
        
        from myapp import dummyview
        
        class UsersTestCase(TestCase):
         
            def test_create_user(self):
                client = Client()
                client.post('/api/users/', data={'username': 'konrad')  # runs tasks inline
                
                with task_mock():
                    client.post('/api/users/', data={'username': 'konrad')
                    # no tasks started yet
                # all tasks ran here
                
                with task_mock('myapp.post_user_create_task'):
                    client.post('/api/users/', data={'username': 'konrad')
                    # all tasks started execept myapp.post_user_create_task
                # myapp.post_user_create_task started here
                
                # you can use task_mock manually:
                
                tmock = task_mock().start()
                client.post('/api/users/', data={'username': 'konrad')
                # no tasks started yet
                tmock.stop()  # all tasks ran here
