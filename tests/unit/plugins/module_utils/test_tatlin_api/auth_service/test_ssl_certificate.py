# -*- coding: utf-8 -*-

# YADRO Tatlin Ansible Collection
# Version 1.0.0
# Copyright (c) 2022 YADRO (KNS Group LLC)

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible_collections.yadro.tatlin.plugins.module_utils.tatlin_api.endpoints import CERTIFICATE_ENDPOINT
from ansible_collections.yadro.tatlin.tests.unit.plugins.module_utils.test_tatlin_api.constants import OPEN_URL_FUNC


class TestSslCertificate:

    def test_upload_ssl_certificate(
        self, tatlin, make_mock, open_url_kwargs,
    ):
        # Mock open_url method
        open_url_mock = make_mock(target=OPEN_URL_FUNC)

        tatlin.upload_ssl_certificate(
            crt='crt_content', key='key_content'
        )

        # Get request's content type
        call_args, call_kwargs = open_url_mock.call_args
        content_type = call_kwargs['headers'].get('Content-Type')

        # Check that header is correct
        assert content_type is not None, \
            'Not found Content-Type in request headers'
        assert 'boundary="' in content_type, \
            'Not found boundary in Content-Type'

        # Get boundary
        boundary = content_type.split('boundary="')[1][:-1]

        # Define expected data
        data = \
            '--{boundary}\r\n' \
            'Content-Type: application/octet-stream\r\n' \
            'Content-Disposition: form-data; ' \
            'name="crt"; filename="crt"\r\n\r\ncrt_content\r\n' \
            '--{boundary}' \
            '\r\nContent-Type: application/octet-stream\r\n' \
            'Content-Disposition: form-data; ' \
            'name="key"; filename="key"\r\n\r\nkey_content\r\n' \
            '--{boundary}--\r\n'.format(boundary=boundary).encode()

        # Defining expected call parameters
        open_url_kwargs.update(
            method='PUT',
            url='https://localhost/{0}'.format(
                CERTIFICATE_ENDPOINT),
            data=data,
            headers={'Content-Type': 'multipart/form-data; boundary="{boundary}"'.format(boundary=boundary)},
        )

        # Result: Request with expected parameters was sent to tatlin
        open_url_mock.assert_called_with(**open_url_kwargs)
