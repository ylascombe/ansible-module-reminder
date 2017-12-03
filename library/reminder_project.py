#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: reminder
short_description: Handle communication with reminder-api.
description:
  - short_description: Handle communication with reminder-api.
options:
  addr:
    description: reminder api address
    required: true
  cmd:
    description:
      Operation to execute (CREATE, GET, LIST, DELETE)
    required: true
  name:
    description:
      name of the project targeted by the operation
    required: true
'''

EXAMPLES = '''
# Create a new project
reminder_project:
  addr: 127.0.0.1:8000
  cmd: CREATE
  project: "awesome"

# Get a project data
reminder_project:
  addr: 127.0.0.1:8000
  cmd: GET
  project: "awesome"
'''

import httplib
import os.path
import json
from pyreminder.base import ReminderManager


def main():

    argument_spec = dict(
        addr=dict(required=True, type='str'),
        cmd=dict(required=True, type='str',
                 choices=['LIST', 'GET', 'CREATE', 'UPDATE', 'DELETE']),
        name=dict(required=True, type='str'),
    )

    module = AnsibleModule(argument_spec=argument_spec)

    addr = module.params.get('addr')
    cmd = module.params.get('cmd')
    name = module.params.get('name')
    changed = False

    reminder = ReminderManager(addr)

    if cmd == 'CREATE':
        try:
            data = reminder.get_project(name)
            if not data:
                data = reminder.create_project(name)
                changed = True
        except Exception as err:
            module.fail_json(msg="Failed to create project %s" % err)

    if cmd == 'GET':
        try:
            data = reminder.get_project(name)
            if data is None:
                module.fail_json(msg="No project named '%s'" % name)
        except Exception as err:
            module.fail_json(msg="Failed to get project %s" % err)

    if cmd == 'LIST':
        status, data = reminder.list_projects()
        module.exit_json(changed=changed, projects=data)

    module.exit_json(changed=changed, project=data)

from ansible.module_utils.basic import *
from ansible.module_utils.urls import *

if __name__ == "__main__":
    main()
