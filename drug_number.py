import requests
import time
from config import *
import random
import matplotlib.pyplot as plt
import matplotlib
import warnings


class DrugNumer:

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
                "cusOrderNo": f"{DrugNumer.create_order()}", "orderByColumnList": [], "page": 1, "limit": 50}
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
    def get_drug_list():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCode/pageInfo"
        data = {"orderByColumnList": None, "createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}",
                "ownerId": None, "cooperativePartnerName": None, "originNo": None, "originType": None,
                "uploadStatusList": [], "isCancel": None, "isSyncBms": None, "isUploadPlatform": None,
                "skuIdArray": None, "orderTypeList": [], "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码采集列表接口": response_time}

    @staticmethod
    def get_drug_in_order():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCodeInInfo/pageInfo"
        data = {"orderByColumnList": None, "createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}",
                "operateTimeTm": None, "operateTimeTo": None, "ownerId": None, "inOrder": None,
                "electrSuperviseCode": None, "parentCode": None, "productionBatch": None, "creatorName": None,
                "cooperativePartnerName": None, "uploadStatusList": [], "skuIdArray": None, "orderTypeList": [],
                "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码入库列表查询接口": response_time}

    @staticmethod
    def get_drug_out_order():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCodeInInfo/pageInfo"
        data = {"orderByColumnList": None, "createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}",
                "operateTimeTm": None, "operateTimeTo": None, "ownerId": None, "inOrder": None,
                "electrSuperviseCode": None, "parentCode": None, "productionBatch": None, "creatorName": None,
                "cooperativePartnerName": None, "uploadStatusList": [], "skuIdArray": None, "orderTypeList": [],
                "page": 1, "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码出库列表查询接口": response_time}

    @staticmethod
    def get_drug_commodity_order():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCodeProductBatch/pageInfo"
        data = {"createTimeFm": f"{select_time()['three_months_ago']}",
                "createTimeTo": f"{select_time()['current_time']}", "ownerId": None, "originNo": None,
                "productionBatch": None, "cooperativePartnerName": None, "originType": None, "uploadStatusList": [],
                "orderTypeList": [], "isCancel": None, "skuIdArray": None, "orderByColumnList": None, "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码品批列表查询接口": response_time}

    @staticmethod
    def get_drug_check_order():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCodeCheckRecord/pageInfo"
        data = {"updateTimeFm": None, "updateTimeTo": None, "ownerId": None, "skuCodes": None, "originOrderNo": None,
                "productionBatch": None, "cooperativePartner": None, "originType": None, "uploadStatus": None,
                "skuIdArray": None, "drugElectrSuperviseCodeCheckErrorTypeList": None,
                "drugCodeCreateTimeFm": f"{select_time()['three_months_ago']}",
                "drugCodeCreateTimeTo": f"{select_time()['current_time']}", "orderByColumnList": None, "page": 1,
                "limit": 50}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码校验记录列表查询接口": response_time}

    @staticmethod
    def take_drug_order():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCodeCollection/scanOrderNo"
        data = {"orderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_id')}"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, json=data, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码查询接口": response_time}

    @staticmethod
    def upload_drug_data():
        url = "http://192.168.111.107:9994/wms/drug/drugElectrSuperviseCodeCollection/upload"
        headers = {"Authorization": get_token()['Authorization']}
        files = {
            'uploadFile': (
                'drug.xlsx', open('drug.xlsx', 'rb'),
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        }
        data = {
            'uploadFileName': 'drug.xlsx',
            'templateName': 'drugElectrSuperviseCodeService',
            'params.orderNo': f'{read_yaml(base_path("data.yaml"), "order_data", "sow_group")}',
            'params.ownerId': '103',
            'params.ownerName': 'null',
            'params.originId': '1902186232336896',
            'params.originNo': f'{read_yaml(base_path("data.yaml"), "order_data", "order_id")}',
            'params.orderType': 'PFXSD',
            'params.cooperativePartnerCode': 'C00077666',
            'params.cooperativePartnerName': '新疆一心康达医药有限公司',
            'params.originType': 'OUT',
            'params.dtList': '[object Object]',
            'params.orderTypeName': '批发销售单',
            'params.shouldTaskCount': '1',
            'params.alreadyTaskCount': '0',
            'params.isFinish': 'null',
            'params.outBoxId': 'null',
            'params.whetherList': 'null',
            'params.skuFlagSystemNameList': 'null',
            'params.skuId': '1238587950765056',
            'params.skuCode': 'M00005662',
            'params.productionBatch': '2402071',
            'params.shouldGatherQty': '180',
            'params.batchNo': 'P24041800317',
        }
        start_time = time.time()
        res = requests.post(url=url, files=files, headers=headers, data=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"追溯码导入接口": response_time}


# 禁用特定警告
warnings.filterwarnings("ignore", category=UserWarning, module='mpld3')

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
# 接口名称和响应时间
data = {
    "so手动分配接口": DrugNumer.so_fp()['so手动分配接口'],
    "追溯码采集列表接口": DrugNumer.get_drug_list()['追溯码采集列表接口'],
    "追溯码入库列表查询接口": DrugNumer.get_drug_in_order()['追溯码入库列表查询接口'],
    "追溯码出库列表查询接口": DrugNumer.get_drug_out_order()['追溯码出库列表查询接口'],
    "追溯码品批列表查询接口": DrugNumer.get_drug_commodity_order()['追溯码品批列表查询接口'],
    "追溯码校验记录列表查询接口": DrugNumer.get_drug_check_order()['追溯码校验记录列表查询接口'],
    "追溯码查询接口": DrugNumer.take_drug_order()['追溯码查询接口'],
    "追溯码导入接口": DrugNumer.upload_drug_data()['追溯码导入接口']
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
