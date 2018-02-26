#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `sing` package."""
import multiprocessing

from sing import single


def test_this_process():
    """ Do some assumption in the current process """
    assert single()


def test_multiple_times():
    single()  # does it exists? however create a lock

    second_check = single()  # here we are sure that the lock is hold
    assert second_check is False


def test_all_valid_from_this_process():
    assert single(allow_all_from_this_process=True) is True
    assert single(allow_all_from_this_process=True) is True


def test_flavors():
    assert single(flavor='first') is True
    assert single(flavor='second') is True

    assert single(flavor='first') is False
    assert single(flavor='second') is False


class TestMultiProcess(object):

    def test_different_processes(self):
        def check_im_the_one():
            separate_proc_result = single(flavor='process', ensure_process_running=True)
            q.put(separate_proc_result)

        q = multiprocessing.Queue()
        p = multiprocessing.Process(target=check_im_the_one)
        p.start()
        result = q.get()
        p.terminate()
        assert result is True
