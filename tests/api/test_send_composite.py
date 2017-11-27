#-*- encoding:utf-8 -*-
import json
import unittest
import responses
try:
    from unittest import mock
except:
    import mock


from nta import (
    NaverTalkApi
)
from nta.models import(
    CompositeContent, Composite, ElementData, ElementList,
    ButtonText
)


class TestNaverTalkAPI(unittest.TestCase):
    def setUp(self):
        self.tested = NaverTalkApi('test_naver_talk_access_token')

    @responses.activate
    def test_send_composite(self):
        responses.add(
            responses.POST,
            NaverTalkApi.DEFAULT_API_ENDPOINT,
            json={
                "success": True,
                "resultCode": "00"
            },
            status=200
        )

        counter = mock.MagicMock()
        def test_callback(res, payload):
            self.assertEqual(res.result_code, "00")
            self.assertEqual(res.success, True)
            self.assertEqual(
                payload.as_json_dict(),
                {
                    'event': 'send',
                    'user': 'test_user_id',
                    'compositeContent': {
                        'compositeList': [
                            {
                                'title': 'test_title',
                                'description': 'test_descript',
                                'image': {
                                    'imageUrl': 'test_image'
                                },
                                'elementList':{
                                    'type': 'LIST',
                                    'data': [
                                        {
                                            'title': 'test_ed_title',
                                            'description': 'test_ed_descript',
                                            'subDescription': 'test_ed_subdescript',
                                            'image': {
                                                'imageUrl': 'test_ed_image'
                                            },
                                            'button':{
                                                'type': 'TEXT',
                                                'data': {
                                                    'title': 'test'
                                                }
                                            }
                                        }
                                    ]

                                },
                                'buttonList': None
                            }
                        ]
                    },
                    'options': {
                        'notification': False
                    }
                }
            )
            counter()


        self.tested.send(
            'test_user_id',
            message=CompositeContent(
                composite_list=[
                    Composite(
                        title='test_title',
                        description='test_descript',
                        image='test_image',
                        element_list=ElementList([
                            ElementData(
                                title='test_ed_title',
                                description='test_ed_descript',
                                sub_description='test_ed_subdescript',
                                image='test_ed_image',
                                button=ButtonText('test')
                            )
                        ])
                    )
                ]
            ),
            callback=test_callback
        )
        self.assertEqual(counter.call_count, 1)