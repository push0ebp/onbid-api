import json
from urllib.parse import urlencode


import requests
import xmltodict

class Onbid():
    API_KEY = ''
    API_URL = 'http://openapi.onbid.co.kr/newopenapi/services'
    SERVICES = {'thing':'ThingInfoInquireSvc'}
    OPERATIONS = {'ThingInfoInquireSvc':{'list':'getObjPerUsage',
                                         'detail':'getObjPerUsageDetail',
                                         'new':'getNewObject'}}
    ITEM_DETAIL_URL = 'http://www.onbid.co.kr/op/cta/cltrdtl/collateralDetailMoveableAssetsDetail.do'
    
    def __init__(self, api_key):
        self.API_KEY = api_key

    def xmltodic(self, xml):
        return json.loads(json.dumps(xmltodict.parse(xml)))

    def get_data(self, service, operation, ctgr_hirk_ids=None, page_no=1, num_rows=1, params={}, header=False):
        params.update({'ServiceKey' : self.API_KEY,
                      'pageNo' : page_no,
                      'numOfRows' :num_rows})
        if ctgr_hirk_ids:
            params['CTGR_HIRK_ID'] = ctgr_hirk_ids[0]
            params['CTGR_HIRK_ID_MID'] = ctgr_hirk_ids[1]
        
        url = '{}/{}/{}'.format(self.API_URL, self.SERVICES[service], self.OPERATIONS[self.SERVICES['thing']][operation])
        res = requests.get(url, params=params)
        xml = res.content.decode('utf-8')
        result = self.xmltodic(xml) 
        
        try:
            if not result['response']['header']['resultMsg'] == 'OK':
                return False
        except KeyError:
            raise 'invalid response data'

        data = result['response']['body']
        try:
            if type(data['items']['item']) != list:
                data['items']['item'] = [data['items']['item']]
        except:
            pass

        if header:
            return result
        
        return data

    def make_item_detail_url(self, item):
        params = {'cltrNo' : item['CLTR_NO'],
                  'plnmNo' : item['PLNM_NO'],
                  'pbctNo' : item['PBCT_NO'],
                  'pbctCdtnNo' : item['PBCT_CDTN_NO']}
        query_string = urlencode(params)
        url = self.ITEM_DETAIL_URL + '?' + query_string
        return url

    def get_item_detail(self, cltr_no, pbct_no, page_no=1, num_rows=1):
        params = {'CLTR_NO':cltr_no,
                  'PBCT_NO':pbct_no }
        data = self.get_data('thing','detail', params=params, page_no=page_no, num_rows=num_rows)
        return data

    def get_items(self, ctgr_hirk_ids, page_no=1, num_rows=1, all=False, new=False):
        items = self.get_data('thing', ['list','new'][new==True], ctgr_hirk_ids, page_no, num_rows)
        

        for item in items['items']['item']:
            item['URL'] = self.make_item_detail_url(item)
        
        if all:
            items = self.get_items(ctgr_hirk_ids, 1, 1)
            if not items:
                return False

            items = self.get_items(ctgr_hirk_ids, 1, int(items['totalCount']))
            return items
        return items


