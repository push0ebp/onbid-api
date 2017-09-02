# onbid-api
python onbid api wrapper


### Start 
```python
API_KEY = 'a8ksKPoc~~~'
onbid = Onbid(API_KEY)
```

### Get Data
(more services will be updated soon)
return `result['response']['body']`

* service : onbid service ex) thing, 
* operation :  service operations, ex) list, detail
* ctgr_hirk_ids : category ids, tuple(normal, mid) ex) car category ids (12000,12100)
* page_no : page number
* num_rows : row count per pages
* params : extra parameters with dict
* header : if you have response header of xml data, set this to True
```python
onbid.get_data('thing', 'list', (12000, 12100), 1, 1)
```

### Get Item Detail
* cltr_no : CLTR_NO
* pbct_no : PBCT_NO
* page_no : page number
* num_rows : row count per pages
```python
details = onbid.get_item_detail(item['CLTR_NO'], item['PBCT_NO'])
details = details['items']['item'][0]
```

### Get Item List
* ctgr_hirk_ids : category ids, tuple(normal, mid) ex) car category ids (12000,12100)
* page_no : page number
* num_rows : row count per pages
* all : get all items, warning) processing may be long..
* new : onbid new object. this use `getNewObject` operation
```python
items = onbid.get_items((12000,121000), all=True) 
print(items['totalCount'])
for item in items['items']['item']:
	print(item) 
```
