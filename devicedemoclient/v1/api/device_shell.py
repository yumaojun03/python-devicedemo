# Copyright 2015 NEC Corporation.  All rights reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from devicedemoclient.common import cliutils as utils
from devicedemoclient.common import utils as device_utils
from devicedemoclient import exceptions
from devicedemoclient.i18n import _
from uuid import uuid4
import logging



LOG = logging.getLogger(__name__)


def _show_cluster(device):
    # del cluster._info['links']
    utils.print_dict(device._info)


@utils.arg('--limit',
           metavar='<limit>',
           type=int,
           help='Maximum number of devices to return.')
@utils.arg('--sort-key',
           metavar='<sort-key>',
           help='Column to sort results by.')
@utils.arg('--sort-dir',
           metavar='<sort-dir>',
           choices=['desc', 'asc'],
           help='Direction to sort. "asc" or "desc".')
@utils.arg('--fields',
           default=None,
           metavar='<fields>',
           help=_('Comma-separated list of fields to display. '
                  'Available fields: uuid, name, baymodel_id, stack_id, '
                  'status, master_count, node_count, links, '
                  'device_create_timeout'
                  )
           )
def do_device_list(cs, args):
    """Print a list of available devices."""
    devices = cs.device.list(limit=args.limit, sort_key=args.sort_key, sort_dir=args.sort_dir)
    columns = ['uuid', 'name', 'type', 'vendor', 'version']
    columns += utils._get_list_table_columns_and_formatters(args.fields, devices, exclude_fields=(c.lower() for c in columns))[0]
    LOG.debug(devices)
    LOG.debug(columns)
    utils.print_list(devices, columns,
                     {'versions': device_utils.print_list_field('versions')},
                     sortby_index=None)


@utils.arg('name',
           metavar='<name>',
           help='Name of the device to create.')
@utils.arg('--type',
           metavar='<type>',
           help='The device type.')
@utils.arg('--vendor',
           metavar='<vendor>',
           help='The device vendor.')
@utils.arg('--version',
           metavar='<version>',
           help='The device version.')
@utils.arg('--timeout',
           metavar='<timeout>',
           type=int,
           default=60,
           help='The timeout for device creation in minutes. The default '
                'is 60 minutes.')
def do_device_create(cs, args):
    """Create a device."""
    opts = {}
    opts['uuid'] = str(uuid4())
    opts['name'] = args.name
    opts['type'] = args.type
    opts['vendor'] = args.vendor
    opts['version'] = args.version
    # opts['create_timeout'] = args.timeout
    try:
        ret = cs.device.create(**opts)
        error, data = ret['error'], ret['data']
        if error is not None:
            raise exceptions.ClientException(error)
        LOG.debug("return device: %s" % ret)
        print("Create device <%s> successful." % opts['uuid'])
    except Exception as e:
        print("Create for device %s failed: %s" %
              (opts['name'], e))


@utils.arg('uuid',
           metavar='<uuid>',
           nargs='+',
           help='ID or name of the (device)s to delete.')
def do_device_delete(cs, args):
    """Delete specified device."""
    for id in args.uuid:
        try:
            cs.device.delete(id=id)
            print("Request to delete device %s successful." % id)
        except Exception as e:
            print("Delete for cluster %(cluster)s failed: %(e)s" %
                  {'cluster': id, 'e': e})


@utils.arg('device_uuid',
           metavar='<device_uuid>',
           help='The uuid of the device to show.')
def do_device_show(cs, args):
    """Show details about the given device."""
    device = cs.device.get(args.device_uuid)
    LOG.debug("device data: %s" % device)
    _show_cluster(device)


@utils.arg('cluster', metavar='<cluster>', help="UUID or name of cluster")
@utils.arg(
    'op',
    metavar='<op>',
    choices=['add', 'replace', 'remove'],
    help="Operations: 'add', 'replace' or 'remove'")
@utils.arg(
    'attributes',
    metavar='<path=value>',
    nargs='+',
    action='append',
    default=[],
    help="Attributes to add/replace or remove "
         "(only PATH is necessary on remove)")
def do_device_update(cs, args):
    """Update information about the given device."""
    patch = device_utils.args_array_to_patch(args.op, args.attributes[0])
    cluster = cs.clusters.update(args.cluster, patch)
    if args.magnum_api_version and args.magnum_api_version == '1.1':
        _show_cluster(cluster)
    else:
        print("Request to update cluster %s has been accepted." % args.cluster)
