import requests
import time
from config import *
import random
import matplotlib.pyplot as plt
import matplotlib
import warnings


class ResponseTest:

    def out_order(self):
        url = "http://192.168.111.107:9994/wms/order/outOrder/pageInfo"
        data = {"createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None,
                "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库订单查询接口": response_time}

    def create_order(self):
        data = {
            "adminAreaCode": "广东省;汕尾市;城区",
            "arrivalStationArea": "安宁市",
            "arrivalStationCity": "昆明市",
            "arrivalStationContactName": "江西百洋",
            "arrivalStationContactTel": "18525647850",
            "arrivalStationProvince": "云南省",
            "businessDepartment": "销售支持部",
            "businessManager": "wwx",
            "businessType": 0,
            "buyerMsg": "销售支持部",
            "carrierCode": "CY012",
            "companyCode": "50",
            "confirmTime": 1666540800000,
            "contactAddr": "广东省汕尾市城区",
            "contactName": "王玮霞",
            "contactTel": "17856546504",
            "creator": "王玮霞",
            "customerCode": "C00077666",
            "customerType": "CUSTOMER",
            "departmentCode": "N0028",
            "discountPrice": 22480000,
            "dtList": [
                {
                    "amount": 175000000,
                    "assignedLot": "2402071",
                    "discountAmount": 175000000,
                    "invalidDate": "2026-04",
                    "limitValid": 0,
                    "mainUnit": "盒",
                    "outOrderQty": 180,
                    "productDate": "2023-05",
                    "rowNo": 1,
                    "skuCode": "M00005662",
                    "stockStatus": "HG"
                }
            ],
            "erpCreateTime": 1666601238000,
            "erpUpdateTime": 1666601261000,
            "extendOne": "xiaowang",
            "extendSix": "云南省昆明市安宁市八街街道八街村",
            "invoiceTitle": "1",
            "invoiceType": "INVOICE",
            "invoiceUrl": "https://img2.baidu.com/it/u=3734104099,2265105642&fm=253&fmt=auto&app=138&f=JPEG?w=708&h=500",
            "isPrintInvoice": 1,
            "isPrintUpstreamInvoice": 1,
            "isPrintUpstreamOrder": 1,
            "orderPrice": 27200000000,
            "orderPrintType": 1,
            "orderStatus": 1,
            "origNo": f"FHTZ-24090400000-{random.randint(1000, 9999)}",
            "origSys": "CQ_ERP",
            "origType": "WHL",
            "ownerCode": "QDBYYYGF",
            "payType": "转账",
            "pickUpType": "0",
            "planShipDate": 1718955010000,
            "productFormType": "YP",
            "saleDepartmentCode": "",
            "saleOfficeCode": "",
            "saleZoneCode": "",
            "sellerRemark": "健康连锁部",
            "updater": "王玮霞",
            "upstreamInvoiceUrl": "http://bswms-uat-01.baheal.com:9332/file/20230509/DRUG_REPORT//5eb5a9bb-669e-40d5-ab00-43765aa6bf0b.jpg",
            "warehouseCode": "50001"
        }
        url = "http://192.168.111.107:9994/oms/api/erp/apiOutOrder/addOrUpdateOutOrder"
        headers = get_token()
        res = requests.post(url=url, json=data, headers=headers)
        if res.json()['msg'] == "成功":
            write_yaml(base_path("data.yaml"), moudle_name="order_data", key="order_no", value=data['origNo'])
            return data['origNo']
        else:
            return {"ERROR": "创建出库单失败"}

    def get_so_list(self):
        url = "http://192.168.111.107:9994/wms/ob/so/pageInfo"
        data = {"createTimeBegin": f"{select_time()['three_months_ago']}",
                "createTimeEnd": f"{select_time()['current_time']}",
                "updateTimeBegin": None, "updateTimeEnd": None, "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"so列表查询接口": response_time}

    def get_so_fp(self):
        url = "http://192.168.111.107:9994/wms/ob/soAssignment/pageInfo"
        data = {"productFormType": None, "wmsBusinessType": None, "soNo": None, "cusOrderNo": None, "waveOrderNo": None,
                "shopOrderNo": None, "soType": None, "soStatus": None, "ownerId": None, "customerId": None,
                "partnerStoreId": None, "skuIdArray": None, "notContainSkuCode": None, "createTimeBegin": None,
                "createTimeEnd": None, "page": 1, "limit": 50, "orderByColumnList": None}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"so分配列表查询接口": response_time}

    def get_wave_list(self):
        url = "http://192.168.111.107:9994/wms/ob/waveIssued/pageWaveArrangement"
        data = {"orderByColumnList": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"波次预排列表接口": response_time}

    def get_wave_count(self):
        url = "http://192.168.111.107:9994/wms/ob/waveIssued/countSoDeliveryMethod"
        data = {"orderByColumnList": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"波次预排数量统计接口": response_time}

    def so_fp(self):
        select_url = "http://192.168.111.107:9994/wms/ob/so/pageInfo"
        data = {"createTimeBegin": f"{time_slp()['start']}", "createTimeEnd": f"{time_slp()['end']}",
                "cusOrderNo": f"{self.create_order()}", "orderByColumnList": [], "page": 1, "limit": 50}
        time.sleep(20)
        headers = get_token()
        res = requests.post(url=select_url, json=data, headers=headers).json()
        for i in res['obj']:
            if i['soStatusName'] == "新创建":
                so_fp_url = "http://192.168.111.107:9994/wms/ob/soAssignment/doAssign"
                so_data = [f"{i['key']}"]
                headers = get_token()
                start_time = time.time()
                res = requests.post(url=so_fp_url, json=so_data, headers=headers)
                end_time = time.time()
                response_time = end_time - start_time
                write_yaml(file_path=base_path("data.yaml"), moudle_name="order_data", key="order_id", value=i['key'])
                return {"so手动分配接口": response_time}
            else:
                return {"ERROR": "so单状态非已创建"}

    def wave_creat(self):
        url = "http://192.168.111.107:9994/wms/ob/waveIssued/manualCreateWaveOrder"
        data = {"soIdList": [read_yaml(base_path("data.yaml"), "order_data", "order_id")], "pickOrderLevel": 1,
                "zjPickMode": "XJHB", "lhPickMode": "XJHB", "isUrgent": False}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        wave_id_url = "http://192.168.111.107:9994/wms/ob/waveOrder/pageInfo"
        wave_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "productFormType": None,
                        "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [],
                        "page": 1, "limit": 50}
        result = requests.post(url=wave_id_url, json=wave_id_data, headers=headers).json()
        for i in result['obj']:
            write_yaml(base_path("data.yaml"), "order_data", "wave_id", i['key'])
        return {"波次安排接口": response_time}

    def wave_release(self):
        headers = get_token()
        select_wave_id_url = f"http://192.168.111.107:9994/wms/ob/waveIssued/selectWaveOrderDt/{read_yaml(base_path('data.yaml'), 'order_data', 'wave_id')}"
        select_wave_id_data = {}
        select_wave_id_result = requests.post(url=select_wave_id_url, headers=headers, json=select_wave_id_data).json()
        for i in select_wave_id_result['obj']:
            xn_url = "http://192.168.111.107:9994/wms/ob/waveIssued/batchMarkFictitiousStagingArea"
            xn_data = [i['key']]
            xn_res = requests.post(url=xn_url, json=xn_data, headers=headers)
            url = "http://192.168.111.107:9994/wms/ob/waveIssued/waveOrderRelease"
            data = {"idList": [read_yaml(base_path("data.yaml"), 'order_data', "wave_id")], "isEmptyStagingArea": False}
            start_time = time.time()
            res = requests.post(url=url, json=data, headers=headers)
            end_time = time.time()
            response_time = end_time - start_time
            return {"波次下发接口": response_time}

    def wave_task_list(self):
        url = "http://192.168.111.107:9994/wms/ob/waveOrder/pageInfo"
        data = {"createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "productFormType": None,
                "wmsBusinessType": None, "waveOrderNo": None, "pickOrderNo": None, "waveOrderType": None,
                "waveOrderStatus": None, "soNo": None, "erpOrderNo": None, "waveRuleName": None, "releaseTimeFm": None,
                "releaseTimeTo": None, "creatorName": None, "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"波次列表接口": response_time}

    def pick_task_list(self):
        url = "http://192.168.111.107:9994/wms/ob/pickOrder/pageInfo"
        data = {"createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": [],
                "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货单列表接口": response_time}

    def pick_task_mission_list(self):
        url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        data = {"createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": [],
                "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货任务列表接口": response_time}

    def pick_all_task(self):
        url = "http://192.168.111.107:9994/wms/ob/pcPick/queryTree/ALL"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货任务汇总接口": response_time}

    def get_pick_task(self):
        url = "http://192.168.111.107:9994/wms/ob/pcPick/receivePickTask"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货任务索取接口": response_time}

    def pick_task_assignment(self):
        pick_id_url = "http://192.168.111.107:9994/wms/ob/pickOrder/pageInfo"
        pick_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "cusOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        pick_id_res = requests.post(url=pick_id_url, json=pick_id_data, headers=headers).json()
        for i in pick_id_res['obj']:
            pick_task_url = "http://192.168.111.107:9994/wms/ob/pickOrder/pickAssignment"
            data = {"userId": "1899299914387968", "pickOrderId": f"{i['key']}", "pickWay": "ZJ", "workMode": "RG"}
            start_time = time.time()
            res = requests.post(url=pick_task_url, json=data, headers=headers)
            end_time = time.time()
            response_time = end_time - start_time
            return {"拣货任务指派": response_time}

    def pick_task(self):
        pick_id_url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        pick_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [], "page": 1, "limit": 50}
        pick_id_result = requests.post(url=pick_id_url, json=pick_id_data, headers=get_token()).json()
        for i in pick_id_result['obj']:
            pick_url = "http://192.168.111.107:9994/wms/ob/pcPick/onekeyPick"
            pick_data = [f"{i['key']}"]
            start_time = time.time()
            res = requests.post(url=pick_url, json=pick_data, headers=get_token())
            end_time = time.time()
            response_time = end_time - start_time
            return {"一键拣货接口": response_time}

    def select_zj_bz_list(self):
        url = "http://192.168.111.107:9994/wms/ob/sowInfoTob/selectPickTaskData"
        data = {"pickTaskNo": None, "pickOrderNo": None, "waveOrderNo": None, "orderByColumnList": [], "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"整件播种列表查询接口": response_time}

    def one_pick_bz(self):
        get_bz_url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}", "orderByColumnList": [],
                "page": 1, "limit": 50}
        get_bz_res = requests.post(url=get_bz_url, json=data, headers=get_token()).json()
        for i in get_bz_res['obj']:
            one_pick_url = f"http://192.168.111.107:9994/wms/ob/sowInfoTob/pcForceSow/{i['key']}"
            one_pick_data = {}
            start_time = time.time()
            res = requests.post(url=one_pick_url, json=one_pick_data, headers=get_token())
            end_time = time.time()
            response_time = end_time - start_time
            return {"整件播种一键分拣接口": response_time}

    def out_order_take(self):
        url = "http://192.168.111.107:9994/wms/ob/outReview/queryOutReviewByTaken"
        data = {"orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核已索取列表查询接口": response_time}

    def out_order_wait_take(self):
        url = "http://192.168.111.107:9994/wms/ob/outReview/queryOutReviewByWaitTake"
        data = {"orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核未索取列表查询接口": response_time}

    def make_out_task(self):
        order_id = "http://192.168.111.107:9994/wms/ob/outReview/queryOutReviewByWaitTake"
        order_data = {"cusOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                      "orderByColumnList": [], "page": 1, "limit": 50}
        order_res = requests.post(url=order_id, json=order_data, headers=get_token()).json()
        for i in order_res['obj']:
            url = "http://192.168.111.107:9994/wms/ob/outReview/confirmGoods"
            data = [f"{i['key']}"]
            start_time = time.time()
            res = requests.post(url=url, json=data, headers=get_token())
            end_time = time.time()
            response_time = end_time - start_time
            return {"集货复核手工集货接口": response_time}

    def one_task_out(self):
        order_id = "http://192.168.111.107:9994/wms/ob/outReview/queryOutReviewByWaitTake"
        order_data = {"cusOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                      "orderByColumnList": [], "page": 1, "limit": 50}
        order_res = requests.post(url=order_id, json=order_data, headers=get_token()).json()
        for i in order_res['obj']:
            url = "http://192.168.111.107:9994/wms/ob/outReview/oneKeyReviewDoneForPC"
            data = [f"{i['key']}"]
            start_time = time.time()
            res = requests.post(url=url, json=data, headers=get_token())
            end_time = time.time()
            response_time = end_time - start_time
            return {"集货复核一件复核接口": response_time}

    def so_detail(self):
        url = f"http://192.168.111.107:9994/wms/ob/so/initUpdate/{read_yaml(base_path('data.yaml'), 'order_data', 'order_id')}"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"so查看接口": response_time}

    def wave_detail(self):
        url = f"http://192.168.111.107:9994/wms/ob/waveOrder/initUpdate/{read_yaml(base_path('data.yaml'), 'order_data', 'wave_id')}"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"波次查看接口": response_time}

    def pick_detail(self):
        url = "http://192.168.111.107:9994/wms/ob/pickOrder/initUpdate/1900709434167808"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货单查看接口": response_time}

    def pick_task_detail(self):
        url = "http://192.168.111.107:9994/wms/ob/pickTask/initUpdate/1900709535912448"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货任务查看接口": response_time}

    def print_so(self):
        url = "http://192.168.111.107:9994/wms/ob/so/printNew"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": ["1900709169353216"]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"so打印接口": response_time}

    def print_cold_so(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/printColdLinkNew"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": ["1900709169353216"]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"冷链交接单打印接口": response_time}

    def reprint_so(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/reprintDeliveryNoteNew"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": ["1900709169353216"]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库单补打接口": response_time}

    def print_pick(self):
        url = "http://192.168.111.107:9994/wms/ob/pickOrder/print"
        data = {"mac": "B0-7B-25-29-F7-04", "pickOrderIdList": ["1900709434167808"]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货单打印接口": response_time}

    def print_pick_detail(self):
        url = "http://192.168.111.107:9994/wms/ob/sowInfoTob/printFjdNew"
        data = {"mac": "B0-7B-25-29-F7-04", "idList": [1900709535912448]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货单分拣明细打印接口": response_time}

    def print_pick_paper(self):
        url = "http://192.168.111.107:9994/wms/ob/pcPick/rePrintPickLabel"
        data = {"mac": "B0-7B-25-29-F7-04", "pickTaskId": "1900709535912448"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货单纸质打印接口": response_time}

    def change_price_order(self):
        url = "http://192.168.111.107:9994/wms/ob/specialOutOrder/pageInfo"
        data = {"orderByColumnList": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"调价订单列表查询接口": response_time}

    def get_self_order(self):
        url = "http://192.168.111.107:9994/wms/ob/selfPickupVerification/pageInfo"
        data = {"orderByColumnList": None, "cusOrderNo": None, "customerId": None, "ownerId": None,
                "saleDepartmentOrgIdList": None, "saleZoneOrgIdList": None, "saleOfficeOrgIdList": None, "soNo": None,
                "soStatus": None, "createTimeBegin": None, "createTimeEnd": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"自提校验单列表查询接口": response_time}

    def get_Temporary(self):
        url = "http://192.168.111.107:9994/wms//ob/stagingAreaClearUp/pageInfo"
        data = {"orderByColumnList": None, "whStagingAreaNo": None, "whStagingAreaType": None, "wmsBusinessType": None,
                "soNo": None, "cusOrderNo": None, "ownerId": None, "customerId": None, "partnerId": None,
                "deliveryMethod": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"暂存区整理列表查询接口": response_time}

    def print_out_order(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/pageInfo"
        data = {"orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库单l列表查询接口": response_time}

    def prin_sale_order(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/printSoCompanionNew"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": [1900709169353216]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"销售单打印接口": response_time}

    def print_with_out(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/printCompanionCover"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": [1900709169353216]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"随货同行单打印接口": response_time}

    def print_drug(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderDrugReport/pageInfo"
        data = {"orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"药检报告列表打印接口": response_time}

    def reprint_drug(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/printDrugReport"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": [1900552194183680]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"药检报告补打接口": response_time}

    def reprint_with_order(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/printSoUpstreamCompanion"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": [1900552194183680]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"随货同行单补打接口": response_time}

    def reprint_invoice(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderPrint/printUpstreamInvoice"
        data = {"mac": "B0-7B-25-29-F7-04", "soIdList": [1900552194183680]}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"发票打印接口": response_time}

    def out_order_fp_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderAssignDtRpt/pageInfo"
        data = {"createTimeFrom": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库订单分配明细表查询接口": response_time}

    def out_order_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderDtRpt/pageInfo"
        data = {"createTimeFrom": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库订单明细表查询接口": response_time}

    def out_order_cancel_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/outCancelOrderRpt/pageInfo"
        data = {"createTimeFrom": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"取消订单明细表查询接口": response_time}

    def pickl_details_form(self):
        url = "http://192.168.111.107:9994/wms/report/ob/pickRecordRpt/pageInfo"
        data = {"waveReleaseTimeFm": f"{select_time()['three_months_ago']}",
                "waveReleaseTimeTo": f"{select_time()['current_time']}", "orderByColumnList": [],
                "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货明细表查询接口": response_time}

    def heavy_details_form(self):
        url = "http://192.168.111.107:9994/wms/report/ob/pickRecordRpt/pageInfo"
        data = {"createTimeFrom": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"称重明细报表查询接口": response_time}

    def pick_leavel_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/pickProgress/pageInfo"
        data = {"pickOrderCreateTimeFrom": f"{select_time()['three_months_ago']}",
                "pickOrderCreateTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货进度明细表查询接口": response_time}

    def fh_leavel_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/sowReviewProgressRpt/pageInfo"
        data = {"soCreateTimeForm": f"{select_time()['three_months_ago']}",
                "soCreateTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"分拣复核进度表查询接口": response_time}

    def out_command_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/outCommandRpt/pageInfo"
        data = {"orderByColumnList": None, "operationTimeFm": f"{select_time()['three_months_ago']}",
                "operationTimeTo": f"{select_time()['current_time']}", "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库指令表查询接口": response_time}

    def out_work_details_form(self):
        url = "http://192.168.111.107:9994/wms/ob/outOrderWorkRecordRpt/pageInfo"
        data = {"createTimeFrom": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库作业记录表查询接口": response_time}

    def temgoray_details_form(self):
        url = "http://192.168.111.107:9994/wms//report/ob/stagingAreaRecord/pageInfo"
        data = {"createTimeFrom": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"暂存去移位表查询接口": response_time}

    def out_times_details_form(self):
        url = "http://192.168.111.107:9994/wms/report/ob/skuOutFrequency/pageInfo"
        data = {"orderByColumnList": None, "createTimeBegin": f"{select_time()['three_months_ago']}",
                "createTimeEnd": f"{select_time()['current_time']}", "page": 1, "limit": 50, "zsFlat": "ZJ"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"出库频次表查询接口": response_time}

    def out_watch_form(self):
        url = "http://192.168.111.107:9994/wms/report/ob/deliveryMonitoringRpt/pageInfo"
        data = {"soCreateTimeBegin": f"{select_time()['three_months_ago']}",
                "soCreateTimeEnd": f"{select_time()['current_time']}", "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"发货监控报表查询接口": response_time}


# # 执行所有函数
# print(ResponseTest().out_order())
# print(ResponseTest().get_so_list())
# print(ResponseTest().get_so_fp())
# print(ResponseTest().get_wave_list())
# print(ResponseTest().get_wave_count())
# print(ResponseTest().so_fp())
# print(ResponseTest().wave_creat())
# print(ResponseTest().wave_release())
# print(ResponseTest().wave_task_list())
# print(ResponseTest().pick_task_list())
# print(ResponseTest().pick_task_mission_list())
# print(ResponseTest().pick_all_task())
# print(ResponseTest().get_pick_task())
# print(ResponseTest().pick_task_assignment())
# print(ResponseTest().pick_task())
# print(ResponseTest().select_zj_bz_list())
# print(ResponseTest().one_pick_bz())
# print(ResponseTest().out_order_take())
# print(ResponseTest().out_order_wait_take())
# print(ResponseTest().make_out_task())
# print(ResponseTest().one_task_out())
# print(ResponseTest().so_detail())
# print(ResponseTest().wave_detail())
# print(ResponseTest().pick_detail())
# print(ResponseTest().pick_task_detail())
# print(ResponseTest().print_so())
# print(ResponseTest().print_cold_so())
# print(ResponseTest().reprint_so())
# print(ResponseTest().print_pick())
# print(ResponseTest().print_pick_detail())
# print(ResponseTest().print_pick_paper())
# print(ResponseTest().change_price_order())
# print(ResponseTest().get_self_order())
# print(ResponseTest().get_Temporary())
# print(ResponseTest().print_out_order())
# print(ResponseTest().prin_sale_order())
# print(ResponseTest().print_with_out())
# print(ResponseTest().print_drug())
# print(ResponseTest().reprint_drug())
# print(ResponseTest().reprint_with_order())
# print(ResponseTest().reprint_invoice())

# 禁用特定警告
warnings.filterwarnings("ignore", category=UserWarning, module='mpld3')

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 接口名称和响应时间
data = {
    '出库订单查询接口': ResponseTest().out_order()['出库订单查询接口'],
    'so列表查询接口': ResponseTest().get_so_list()['so列表查询接口'],
    'so分配列表查询接口': ResponseTest().get_so_fp()['so分配列表查询接口'],
    '波次预排列表接口': ResponseTest().get_wave_list()['波次预排列表接口'],
    '波次预排数量统计接口': ResponseTest().get_wave_count()['波次预排数量统计接口'],
    'so手动分配接口': ResponseTest().so_fp()['so手动分配接口'],
    '波次安排接口': ResponseTest().wave_creat()['波次安排接口'],
    '波次下发接口': ResponseTest().wave_release()['波次下发接口'],
    '波次列表接口': ResponseTest().wave_task_list()['波次列表接口'],
    '拣货单列表接口': ResponseTest().pick_task_list()['拣货单列表接口'],
    '拣货任务汇总接口': ResponseTest().pick_all_task()['拣货任务汇总接口'],
    '拣货任务索取接口': ResponseTest().get_pick_task()['拣货任务索取接口'],
    '拣货任务指派': ResponseTest().pick_task_assignment()['拣货任务指派'],
    '一键拣货接口': ResponseTest().pick_task()['一键拣货接口'],
    '整件播种列表查询接口': ResponseTest().select_zj_bz_list()['整件播种列表查询接口'],
    '整件播种一键分拣接口': ResponseTest().one_pick_bz()['整件播种一键分拣接口'],
    '集货复核已索取列表查询接口': ResponseTest().out_order_take()['集货复核已索取列表查询接口'],
    '集货复核未索取列表查询接口': ResponseTest().out_order_wait_take()['集货复核未索取列表查询接口'],
    '集货复核手工集货接口': ResponseTest().make_out_task()['集货复核手工集货接口'],
    '集货复核一件复核接口': ResponseTest().one_task_out()['集货复核一件复核接口'],
    'so查看接口': ResponseTest().so_detail()['so查看接口'],
    '波次查看接口': ResponseTest().wave_detail()['波次查看接口'],
    '拣货单查看接口': ResponseTest().pick_detail()['拣货单查看接口'],
    '拣货任务查看接口': ResponseTest().pick_task_detail()['拣货任务查看接口'],
    'so打印接口': ResponseTest().print_so()['so打印接口'],
    '冷链交接单打印接口': ResponseTest().print_cold_so()['冷链交接单打印接口'],
    '出库单补打接口': ResponseTest().reprint_so()['出库单补打接口'],
    '拣货单打印接口': ResponseTest().print_pick()['拣货单打印接口'],
    '拣货单分拣明细打印接口': ResponseTest().print_pick_detail()['拣货单分拣明细打印接口'],
    '拣货单纸质打印接口': ResponseTest().print_pick_paper()['拣货单纸质打印接口'],
    '调价订单列表查询接口': ResponseTest().change_price_order()['调价订单列表查询接口'],
    '自提校验单列表查询接口': ResponseTest().get_self_order()['自提校验单列表查询接口'],
    '暂存区整理列表查询接口': ResponseTest().get_Temporary()['暂存区整理列表查询接口'],
    '出库单l列表查询接口': ResponseTest().print_out_order()['出库单l列表查询接口'],
    '销售单打印接口': ResponseTest().prin_sale_order()['销售单打印接口'],
    '随货同行单打印接口': ResponseTest().print_with_out()['随货同行单打印接口'],
    '药检报告列表打印接口': ResponseTest().print_drug()['药检报告列表打印接口'],
    '药检报告补打接口': ResponseTest().reprint_drug()['药检报告补打接口'],
    '随货同行单补打接口': ResponseTest().reprint_with_order()['随货同行单补打接口'],
    '发票打印接口': ResponseTest().reprint_invoice()['发票打印接口'],
    '出库订单分配明细表查询接口':ResponseTest().out_order_fp_details_form()['出库订单分配明细表查询接口'],
    '出库订单明细表查询接口':ResponseTest().out_order_details_form()['出库订单明细表查询接口'],
    '取消订单明细表查询接口': ResponseTest().out_order_cancel_details_form()['取消订单明细表查询接口'],
    '拣货明细表查询接口': ResponseTest().pickl_details_form()['拣货明细表查询接口'],
    '称重明细报表查询接口': ResponseTest().heavy_details_form()['称重明细报表查询接口'],
    '拣货进度明细表查询接口': ResponseTest().pick_leavel_details_form()['拣货进度明细表查询接口'],
    '分拣复核进度表查询接口': ResponseTest().fh_leavel_details_form()['分拣复核进度表查询接口'],
    '出库指令表查询接口': ResponseTest().out_command_details_form()['出库指令表查询接口'],
    '出库作业记录表查询接口': ResponseTest().out_work_details_form()['出库作业记录表查询接口'],
    '暂存去移位表查询接口': ResponseTest().temgoray_details_form()['暂存去移位表查询接口'],
    '出库频次表查询接口': ResponseTest().out_times_details_form()['出库频次表查询接口'],
    '发货监控报表查询接口': ResponseTest().out_watch_form()['发货监控报表查询接口']
}

# 分离接口名称和响应时间
names = list(data.keys())
times = list(data.values())

# 设置颜色
colors = ['green' if time < 1 else
          'yellow' if time < 5 else
          'orange' if time < 10 else
          'red' for time in times]

# 创建柱状图
plt.figure(figsize=(16, 10),dpi=200)
bars = plt.barh(names, times, color=colors, edgecolor='black', linewidth=1.2)

# 在每个柱子上方添加标签
for bar in bars:
    plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
             f'{bar.get_width():.2f}s', va='center', ha='left', fontsize=10, color='black')

# 添加网格线
plt.grid(axis='x', linestyle='--', alpha=0.7)

# 设置坐标轴标签和标题
plt.xlabel('响应时间 (秒)', fontsize=12)
plt.title('接口响应时间统计', fontsize=14, fontweight='bold')

# 添加阈值线
plt.axvline(x=1, color='green', linestyle='--', label='1秒阈值')
plt.axvline(x=5, color='yellow', linestyle='--', label='5秒阈值')
plt.axvline(x=10, color='orange', linestyle='--', label='10秒阈值')

# 添加图例
plt.legend(fontsize=10)
plt.tight_layout()

# 显示图形
plt.show()
