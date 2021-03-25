#!/usr/bin/env python3

# Copyright 2015-2016 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import os
import subprocess
import sys

from ros_buildfarm.workspace import clean_workspace
from ros_buildfarm.workspace import ensure_workspace_exists


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description="Invoke 'rosdoc2' on each package of a workspace")
    parser.add_argument(
        '--workspace-root',
        required=True,
        help='The root path of the workspace to document')
    parser.add_argument(
        '--rosdoc2-dir',
        required=True,
        help='The root path of the rosdoc2 repository')
    args = parser.parse_args(argv)

    ensure_workspace_exists(args.workspace_root)
    clean_workspace(args.workspace_root)

    print('Installing rosdoc2')
    pip_rc = subprocess.call(['python3', '-m', 'pip', 'install', '--no-warn-script-location', '.'], cwd=args.rosdoc2_dir)
    if pip_rc:
        return pip_rc

    print('Invoking rosdoc2')
    env = {
        **os.environ,
    }
    if 'PATH' not in env:
        env['PATH'] = ''
    else:
        env['PATH'] += ':'
    env['PATH'] += '/home/buildfarm/.local/bin'

    rosdoc2_rc = subprocess.call(['rosdoc2', 'build', '--package-path', '/tmp/ws/src/rcutils'], cwd=args.workspace_root, env=env)
    if rosdoc2_rc:
        return rosdoc2_rc

    return 0


if __name__ == '__main__':
    sys.exit(main())
