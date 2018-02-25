# -*- coding: utf-8 -*-
import logging
import os
import re
import sys
import atexit
import tempfile

import psutil

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

_created_pids = set()


class ProcessRunningException(Exception):
    pass


def get_exec_file_path():
    try:
        exec_file_path = os.path.abspath(sys.modules['__main__'].__file__)
    except:
        exec_file_path = sys.executable
    return exec_file_path


def get_valid_filename(s):
    s = str(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '-', s)


def create_pid(pid, pid_path):
    with open(pid_path, 'w') as f:
        f.write(str(pid))
    _created_pids.add(pid_path)


def delete_pids():
    logger.debug("Removing %d created pid files" % len(_created_pids))
    for pid_path in _created_pids:
        os.remove(pid_path)


def get_pid_path(flavor=""):
    process_path = get_exec_file_path()
    logger.debug("Ensuring {process_name} is run once".format(
        process_name=process_path)
    )
    process_name, ext = os.path.splitext(process_path)
    if flavor:
        process_name += "-%s" % flavor
    # get a single filename out of the process complete path
    pid_filename = get_valid_filename(process_name)
    temp_folder = tempfile.gettempdir()
    return os.path.join(temp_folder, pid_filename + '.pid')


def get_pid(pid_path):
    if os.path.isfile(pid_path):
        with open(pid_path) as f:
            content = f.read()
            pid = int(content.strip())
    else:
        raise IOError("PID file not found %s" % pid_path)
    return pid


def single(flavor="",
           allow_all_from_this_process=False,
           ensure_process_running=False,
           as_exception=False):
    pid_path = get_pid_path(flavor=flavor)
    current_pid = os.getpid()
    if os.path.isfile(pid_path):
        # the PID exists
        pid = None  # our pid
        if allow_all_from_this_process:
            pid = pid or get_pid(pid_path)
            if pid == current_pid:
                logger.debug("A lock is hold, but from this process")
                return True

        if ensure_process_running:
            pid = pid or get_pid(pid_path)
            if not psutil.pid_exists(pid):
                logger.warning(
                    "The process {pid} in {pidpath} is not running."
                )
                os.remove(pid_path)

        if as_exception:
            raise ProcessRunningException(
                "There's a PID file in %s" % pid_path
            )
        return False

    create_pid(current_pid, pid_path)
    return True


atexit.register(delete_pids)
