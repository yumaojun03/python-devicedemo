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
import logging


LOG = logging.getLogger(__name__)


def _show_cluster(cluster):
    del cluster._info['links']
    utils.print_dict(cluster._info)


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


@utils.arg('--uuid',
           metavar='<name>',
           help='Name of the cluster to create.')
@utils.arg('--cluster-template',
           required=True,
           metavar='<cluster_template>',
           help='ID or name of the cluster template.')
@utils.arg('--node-count',
           metavar='<node-count>',
           type=int,
           default=1,
           help='The cluster node count.')
@utils.arg('--master-count',
           metavar='<master-count>',
           type=int,
           default=1,
           help='The number of master nodes for the cluster.')
@utils.arg('--discovery-url',
           metavar='<discovery-url>',
           help='Specifies custom discovery url for node discovery.')
@utils.arg('--timeout',
           metavar='<timeout>',
           type=int,
           default=60,
           help='The timeout for cluster creation in minutes. The default '
                'is 60 minutes.')
def do_device_create(cs, args):
    """Create a device."""
    cluster_template = cs.cluster_templates.get(args.cluster_template)

    opts = {}
    opts['name'] = args.name
    opts['cluster_template_id'] = cluster_template.uuid
    opts['node_count'] = args.node_count
    opts['master_count'] = args.master_count
    opts['discovery_url'] = args.discovery_url
    opts['create_timeout'] = args.timeout
    try:
        cluster = cs.clusters.create(**opts)
        # support for non-async in 1.1
        if args.magnum_api_version and args.magnum_api_version == '1.1':
            _show_cluster(cluster)
        else:
            fields = str(cluster).split("u'")
            uuid = fields[2]
            print("Request to create cluster %s has been accepted." % uuid[:3])
    except Exception as e:
        print("Create for cluster %s failed: %s" %
              (opts['name'], e))


@utils.arg('cluster',
           metavar='<cluster>',
           nargs='+',
           help='ID or name of the (cluster)s to delete.')
def do_device_delete(cs, args):
    """Delete specified device."""
    for id in args.cluster:
        try:
            cs.clusters.delete(id)
            print("Request to delete cluster %s has been accepted." %
                  id)
        except Exception as e:
            print("Delete for cluster %(cluster)s failed: %(e)s" %
                  {'cluster': id, 'e': e})


@utils.arg('device_uuid',
           metavar='<device_uuid>',
           help='The uuid of the device to show.')
def do_device_show(cs, args):
    """Show details about the given device."""
    cluster = cs.clusters.get(args.cluster)
    if args.long:
        cluster_template = \
            cs.cluster_templates.get(cluster.cluster_template_id)
        del cluster_template._info['links'], cluster_template._info['uuid']

        for key in cluster_template._info:
            if 'clustertemplate_' + key not in cluster._info:
                cluster._info['clustertemplate_' + key] = \
                    cluster_template._info[key]
    _show_cluster(cluster)


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
