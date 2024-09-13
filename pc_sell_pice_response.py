import requests
import time
from config import *
import random
import matplotlib.pyplot as plt
import matplotlib
import warnings


class ResponseSellTest:

    @staticmethod
    def create_order():
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
                    "outOrderQty": 10,
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
        print(res.json())
        if res.json()['msg'] == "成功":
            write_yaml(base_path("data.yaml"), moudle_name="order_data", key="order_no", value=data['origNo'])
            return data['origNo']
        else:
            return {"ERROR": "创建出库单失败"}

    @staticmethod
    def so_fp():
        select_url = "http://192.168.111.107:9994/wms/ob/so/pageInfo"
        data = {"createTimeBegin": f"{time_slp()['start']}", "createTimeEnd": f"{time_slp()['end']}",
                "cusOrderNo": f"{ResponseSellTest.create_order()}", "orderByColumnList": [], "page": 1, "limit": 50}
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
                write_yaml(file_path=base_path("data.yaml"), moudle_name="order_data", key="sow_group",
                           value=i['sowGroup'])
                return {"so手动分配接口": response_time}
            else:
                return {"ERROR": "so单状态非已创建"}

    @staticmethod
    def wave_creat():
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

    @staticmethod
    def wave_release():
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

    @staticmethod
    def pick_task_assignment():
        pick_id_url = "http://192.168.111.107:9994/wms/ob/pickOrder/pageInfo"
        pick_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "cusOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        pick_id_res = requests.post(url=pick_id_url, json=pick_id_data, headers=headers).json()
        for i in pick_id_res['obj']:
            pick_task_url = "http://192.168.111.107:9994/wms/ob/pickOrder/pickAssignment"
            data = {"userId": "1899299914387968", "pickOrderId": f"{i['key']}", "pickWay": "LH", "workMode": "RG"}
            start_time = time.time()
            res = requests.post(url=pick_task_url, json=data, headers=headers)
            end_time = time.time()
            response_time = end_time - start_time
            return {"拣货任务指派": response_time}

    @staticmethod
    def pick_task():
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

    @staticmethod
    def get_lh_bz_data():
        pick_id_url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        pick_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [], "page": 1, "limit": 50}
        pick_task_mission_no = requests.post(url=pick_id_url, json=pick_id_data, headers=get_token()).json()
        for i in pick_task_mission_no['obj']:
            pick_tak_no = i['pickTaskNo']
            url = f"http://192.168.111.108:9994/wms/ob/sowInfoTob/pcLhScanPickTaskNo/{pick_tak_no}"
            data = {}
            headers = get_token()
            start_time = time.time()
            res = requests.post(url=url, json=data, headers=headers)
            end_time = time.time()
            response_time = end_time - start_time
            write_yaml(base_path("data.yaml"), "order_data", "sell_price_id", res.json()['obj']['pickTaskId'])
            return {"索取零货播种任务接口": response_time}

    @staticmethod
    def pick_container_details():
        url = f"http://192.168.111.108:9994/wms/ob/sowInfoTob/getLhPickTaskInfo/{read_yaml(base_path('data.yaml'), 'order_data', 'sell_price_id')}"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拣货容器查看接口": response_time}

    @staticmethod
    def split_pick_details():
        url = f"http://192.168.111.108:9994/wms/ob/sowInfoTob/getLhSowScanRecord/{read_yaml(base_path('data.yaml'), 'order_data', 'sell_price_id')}"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"分拣信息查看接口": response_time}

    @staticmethod
    def sell_bz_details():
        url = f"http://192.168.111.108:9994/wms/ob/sowInfoTob/pcLhScanSkuCode/{read_yaml(base_path('data.yaml'), 'order_data', 'sell_price_id')}/M00005662"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        write_yaml(base_path("data.yaml"), "order_data", "sow_id_lh_fh", res.json()['obj']['sowInfoTobId'])
        return {"零货播种商品明细接口": response_time}

    @staticmethod
    def sell_bz():
        headers = get_token()
        pick_id_url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        pick_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [], "page": 1, "limit": 50}
        pick_task_mission_no = requests.post(url=pick_id_url, json=pick_id_data, headers=get_token()).json()
        for i in pick_task_mission_no['obj']:
            pick_tak_no = i['pickTaskNo']
            url = "http://192.168.111.108:9994/wms/ob/sowInfoTob/pcSaveSowInfoTobScanRecord"
            data = {"pickTaskNo": f"{pick_tak_no}", "sowCode": "1", "skuCode": "M00005662",
                    "productionBatch": "2402071",
                    "sowInfoTobId": read_yaml(base_path('data.yaml'), 'order_data', 'sow_id_lh_fh'), "scanSowQty": 10}
            start_time = time.time()
            res = requests.post(url=url, json=data, headers=headers)
            end_time = time.time()
            response_time = end_time - start_time
            return {"零货播种接口": response_time}

    @staticmethod
    def get_sell_fh_data():
        headers = get_token()
        pick_id_url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        pick_id_data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                        "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                        "orderByColumnList": [], "page": 1, "limit": 50}
        pick_task_mission_no = requests.post(url=pick_id_url, json=pick_id_data, headers=get_token()).json()
        for i in pick_task_mission_no['obj']:
            box_url = f"http://192.168.111.108:9994/wms/ob/pickTask/initUpdate/{i['key']}"
            box_data = {}
            box_res = requests.post(url=box_url, json=box_data, headers=headers).json()
            for box_no_data in box_res['obj']['sowDtList']:
                box_no = box_no_data['boxNo']
                write_yaml(base_path("data.yaml"), "order_data", "box_no", box_no)
                url = "http://192.168.111.108:9994/wms/ob/review/b2b/initReviewData"
                data = {"checkPlatformId": 1092414772990464, "platform": "PC", "boxNo": f"{box_no}"}
                start_time = time.time()
                res = requests.post(url=url, json=data, headers=headers)
                end_time = time.time()
                response_time = end_time - start_time
                for a in res.json()['obj']['dtList']:
                    write_yaml(base_path("data.yaml"), "order_data", "lh_review_id", a['reviewId'])
                return {"拆零复核索取接口": response_time}

    @staticmethod
    def get_fh_commodity_details():
        url = "http://192.168.111.108:9994/wms/ob/review/b2b/queryRecommendConsumable/1238587950765056"
        data = {}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拆零复核商品明细接口": response_time}

    @staticmethod
    def sell_fh():
        url = "http://192.168.111.108:9994/wms/ob/review/b2b/saveReviewData"
        data = {"id": f"{read_yaml(base_path('data.yaml'), 'order_data', 'lh_review_id')}", "barcode": "M00005662",
                "batchNo": "2402071", "reviewQty": 10}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"拆零复核接口": response_time}

    @staticmethod
    def sell_fh_take_drug():
        url = "http://192.168.111.108:9994/wms/drug/drugElectrSuperviseCodeCollection/saveDrugSupervisionCode"
        data = {"orderNo": f"[{read_yaml(base_path('data.yaml'), 'order_data', 'box_no_lh')}]", "ownerId": 103,
                "ownerName": None, "originId": read_yaml(base_path('data.yaml'), 'order_data', 'order_id'),
                "originNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}", "orderType": "PFXSD",
                "cooperativePartnerCode": "C00077666",
                "cooperativePartnerName": "新疆一心康达医药有限公司", "originType": "OUT", "dtList": [
                {"skuFlagSystemName": None, "isContainSerialNo": None,
                 "commonSku": {"skuId": 1238587950765056, "skuCode": "M00005662", "barcode": "6923878310726",
                               "skuName": "沙格列汀片", "skuCategoryId": None, "skuCategoryName": None,
                               "skuCategoryCode": None, "skuBigCategoryCode": None, "skuBigCategoryName": None,
                               "spec": "5mg*7片/盒", "mainUnit": "盒", "perQty": None, "originCountry": "美国",
                               "drugForm": "片剂", "tradeName": "安立泽", "approvalNumber": "国药准字HJ20160089",
                               "brandName": "安立泽08030", "mfgName": "AstraZeneca Pharmaceuticals LP", "mfg": None,
                               "permitHolder": "AstraZeneca AB", "tempControl": "CW", "validityDay": None,
                               "tempControlName": "常温", "tempMax": None, "tempMin": None, "mnemonicCode": None,
                               "instrumentModel": None}, "msg": None, "rowNum": None, "shouldGatherQty": 10,
                 "shouldGatherWholePieceQty": None, "shouldGatherScatteredQty": None, "alreadyGatherQty": 0,
                 "waitGatherQty": None, "skuId": 1238587950765056, "skuCode": "M00005662", "batchNo": "P24052400159",
                 "productionBatch": "2402071", "productionDate": "2023-05", "invalidDate": "2026-04", "perQty": None,
                 "isFinish": None, "isPass": 0, "isPassName": "否", "shouldGatherBoxQty": None,
                 "alreadyGatherBoxQty": None, "waitGatherBoxQty": None, "outBoxId": None,
                 "drugElectrSuperviseCodeList": None}], "orderTypeName": "批发销售单", "shouldTaskCount": 1,
                "alreadyTaskCount": 0, "isFinish": None, "outBoxId": None, "whetherList": None,
                "skuFlagSystemNameList": None, "skuId": 1238587950765056, "skuCode": "M00005662",
                "scannSkuCode": "M00005662", "productionBatch": "2402071", "shouldGatherQty": 10,
                "batchNo": "P24052400159",
                "reviewId": f"{read_yaml(base_path('data.yaml'), 'order_data', 'lh_review_id')}", "reviewType": "INNER",
                "electrSuperviseCode": None,
                "electrSuperviseCodeList": ["81111111118111111111", "81111111118111111112", "81111111118111111113",
                                            "81111111118111111114", "81111111118111111115", "81111111118111111116",
                                            "81111111118111111117", "81111111118111111118", "81111111118111111119",
                                            "81111111118111111110"]}

        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        print(res.json())
        response_time = end_time - start_time
        return {"拆零复核采集追溯码": response_time}

    @staticmethod
    def save_sell_fh():
        url = "http://192.168.111.108:9994/wms/ob/review/b2b/reviewDone"
        data = {"id": f"{read_yaml(base_path('data.yaml'), 'order_data', 'lh_review_id')}"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        print(res.json())
        return {"拆零复核完成接口": response_time}


print(ResponseSellTest.so_fp())
print(ResponseSellTest.wave_creat())
print(ResponseSellTest.wave_release())
print(ResponseSellTest.pick_task_assignment())
print(ResponseSellTest.pick_task())
print(ResponseSellTest.get_lh_bz_data())
print(ResponseSellTest.pick_container_details())
print(ResponseSellTest.split_pick_details())
print(ResponseSellTest.sell_bz_details())
print(ResponseSellTest.sell_bz())
print(ResponseSellTest.get_sell_fh_data())
print(ResponseSellTest.get_fh_commodity_details())
print(ResponseSellTest.sell_fh())
print(ResponseSellTest.sell_fh_take_drug())
print(ResponseSellTest.save_sell_fh())

# 禁用特定警告
warnings.filterwarnings("ignore", category=UserWarning, module='mpld3')

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 接口名称和响应时间
data = {
    "so手动分配接口": ResponseSellTest.so_fp()['so手动分配接口'],
    "波次安排接口": ResponseSellTest.wave_creat()['波次安排接口'],
    "波次下发接口": ResponseSellTest.wave_release()['波次下发接口'],
    "拣货任务指派": ResponseSellTest.pick_task_assignment()['拣货任务指派'],
    "一键拣货接口": ResponseSellTest.pick_task()['一键拣货接口'],
    "索取零货播种任务接口": ResponseSellTest.get_lh_bz_data()['索取零货播种任务接口'],
    "拣货容器查看接口": ResponseSellTest.pick_container_details()['拣货容器查看接口'],
    "分拣信息查看接口": ResponseSellTest.split_pick_details()['分拣信息查看接口'],
    "零货播种商品明细接口": ResponseSellTest.sell_bz_details()['零货播种商品明细接口'],
    "零货播种接口": ResponseSellTest.sell_bz()['零货播种接口'],
    "拆零复核索取接口": ResponseSellTest.get_sell_fh_data()['拆零复核索取接口'],
    "拆零复核商品明细接口": ResponseSellTest.get_fh_commodity_details()['拆零复核商品明细接口'],
    "拆零复核接口": ResponseSellTest.sell_fh()['拆零复核接口'],
    "拆零复核采集追溯码": ResponseSellTest.sell_fh_take_drug()['拆零复核采集追溯码'],
    "拆零复核完成接口": ResponseSellTest.save_sell_fh()['拆零复核完成接口'],
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
plt.figure(figsize=(12, 8))
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
