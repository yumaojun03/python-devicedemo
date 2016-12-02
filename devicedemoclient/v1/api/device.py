# Copyright 2015 Rackspace, Inc.  All rights reserved.
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

from devicedemoclient.common import base
from devicedemoclient import exceptions
import logging


LOG = logging.getLogger(__name__)
CREATION_ATTRIBUTES = ['device_uuid', 'csr']


class Device(base.Resource):
    def __repr__(self):
        return "<Device %s>" % self._info


class DeviceManager(base.Manager):
    resource_class = Device

    @staticmethod
    def _path(id=None):
        return '/v1/devices/%s' % id if id else '/v1/devices'

    def get(self, device_uuid):
        try:
            return self._list(self._path(device_uuid))[0]
        except IndexError:
            return None

    def list(self, limit=None, sort_key=None, sort_dir=None, detail=False):
        """Retrieve a list of devices.

        :param limit: The maximum number of results to return per
                      request, if:

            1) limit > 0, the maximum number of bays to return.
            2) limit == 0, return the entire list of bays.
            3) limit param is NOT specified (None), the number of items
               returned respect the maximum imposed by the Magnum API
               (see Magnum's api.max_limit option).

        :param sort_key: Optional, field used for sorting.

        :param sort_dir: Optional, direction of sorting, either 'asc' (the
                         default) or 'desc'.

        :param detail: Optional, boolean whether to return detailed information
                       about devices.

        :returns: A list of device.

        """
        if limit is not None:
            limit = int(limit)

        # filters = utils.common_filters(marker, limit, sort_key, sort_dir)

        path = ''
        if detail:
            path += 'detail'
        # if filters:
        #     path += '?' + '&'.join(filters)

        if limit is None:
            return self._list(self._path(path))
        else:
            return self._list_pagination(self._path(path),
                                         self.__class__.template_name,
                                         limit=limit)

    def create(self, **kwargs):
        new = {}
        for (key, value) in kwargs.items():
            if key in CREATION_ATTRIBUTES:
                new[key] = value
            elif key == 'bay_uuid':
                new['cluster_uuid'] = value
            else:
                raise exceptions.InvalidAttribute(
                    "Key must be in %s" % ",".join(CREATION_ATTRIBUTES))
        return self._create(self._path(), new)

    def delete(self):
        pass

    def update(self):
        pass
