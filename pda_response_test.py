import requests
import time
from config import *
import random
from pc_response_test import *
import matplotlib.pyplot as plt
import matplotlib
import warnings


class PdaResponseTest:

    @staticmethod
    def lh_pick_list():
        url = "http://192.168.111.108:9994/wms/pda/ob/lhPick/queryPickTaskByUser"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"PDA零货拣货列表查询接口": response_time}

    @staticmethod
    def zj_pick_list():
        url = "http://192.168.111.108:9994/wms/pda/ob/zjPick/queryPickTaskByUser"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"PDA整件拣货列表查询接口": response_time}

    @staticmethod
    def zj_pick_detail():
        make_so = ResponseTest().create_order()
        make_so_fp = ResponseTest().so_fp()
        make_wave = ResponseTest().wave_creat()
        make_wave_release = ResponseTest().wave_release()
        make_pick_assign = ResponseTest().pick_task_assignment()
        get_task_mission_id_url = "http://192.168.111.107:9994/wms/ob/pickTask/pageInfo"
        data = {"createTimeFm": f"{time_slp()['start']}", "createTimeTo": f"{time_slp()['end']}",
                "erpOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}", "orderByColumnList": [],
                "page": 1, "limit": 50}
        get_task_mission_id = requests.post(url=get_task_mission_id_url, headers=get_token(), json=data).json()
        for i in get_task_mission_id['obj']:
            pick_url = f"http://192.168.111.108:9994/wms/pda/ob/zjPick/startPicking/{i['key']}"
            write_yaml(base_path('data.yaml'), 'order_data', 'pick_task_id', i['key'])
            start_time = time.time()
            res = requests.post(url=pick_url, headers=get_token())
            end_time = time.time()
            write_yaml(base_path('data.yaml'), 'order_data', 'pick_data', res.json()['obj']['pickTaskDtKey'])
            write_yaml(base_path('data.yaml'), 'order_data', 'lot_name', res.json()['obj']['lotName'])
            write_yaml(base_path('data.yaml'), 'order_data', 'pick_task_code', res.json()['obj']['pickTaskNo'])
            response_time = end_time - start_time
            return {"PDA整件详情接口": response_time}

    @staticmethod
    def zj_pick_warehouse():
        url = "http://192.168.111.108:9994/wms/pda/ob/zjPick/scannLotCodeOrContainerNo"
        data = {"pickTaskId": read_yaml(base_path('data.yaml'), 'order_data', 'pick_task_id'),
                "pickTaskDtKey": f"{read_yaml(base_path('data.yaml'), 'order_data', 'pick_data')}",
                "lotCodeOrContainerNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'lot_name')}", }
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"PDA整件拣货货位查询接口": response_time}

    @staticmethod
    def zj_pick():
        url = "http://192.168.111.108:9994/wms/pda/ob/zjPick/savePick"
        data = {"pickTaskId": read_yaml(base_path('data.yaml'), 'order_data', 'pick_task_id'),
                "pickTaskDtKey": f"{read_yaml(base_path('data.yaml'), 'order_data', 'pick_data')}",
                "lotName": f"{read_yaml(base_path('data.yaml'), 'order_data', 'lot_name')}", "pickQty": 1,
                "lotCodeOrContainerNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'lot_name')}"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"PDA整件拣货接口": response_time}

    @staticmethod
    def zj_bz_detail():
        url = f"http://192.168.111.108:9994/wms/pda/ob/sow/pdaScanPickTaskNo/{read_yaml(base_path('data.yaml'), 'order_data', 'pick_task_code')}"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"PDA整件拣货详情接口": response_time}

    @staticmethod
    def zj_bz_commodity():
        url = (f"http://192.168.111.108:9994/wms/pda/ob/sow/pdaScanSkuCode/"
               f"{read_yaml(base_path('data.yaml'), 'order_data', 'pick_task_id')}/M00005662")
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers)
        end_time = time.time()
        write_yaml(base_path('data.yaml'), 'order_data', 'sku_id', res.json()['obj']['skuId'])
        response_time = end_time - start_time
        return {"PDA整件拣货商品接口": response_time}

    @staticmethod
    def zj_bz_details():
        url = f"http://192.168.111.108:9994/wms/pda/ob/sow/pdaScanProductBatch/{read_yaml(base_path('data.yaml'), 'order_data', 'pick_task_id')}/{read_yaml(base_path('data.yaml'), 'order_data', 'sku_id')}/2402071"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        for i in res.json()['obj']['sowSkuList']:
            write_yaml(base_path('data.yaml'), 'order_data', 'sow_id', i['sowInfoTobId'])
            write_yaml(base_path('data.yaml'), 'order_data', 'so_id', i['soId'])
            write_yaml(base_path('data.yaml'), 'order_data', 'so_no', i['soNo'])
            return {"PDA整件拣货明细接口": response_time}

    @staticmethod
    def zj_bz():
        url = "http://192.168.111.108:9994/wms/pda/ob/sow/saveSowInfoTobScanRecord"
        data = {"sowInfoTobId": read_yaml(base_path('data.yaml'), 'order_data', 'sow_id'), "skuId": 1238587950765056,
                "skuCode": "M00005662",
                "skuName": "沙格列汀片", "tradeName": "安立泽", "spec": "5mg*7片/盒",
                "soId": read_yaml(base_path('data.yaml'), 'order_data', 'so_id'),
                "soNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'so_no')}", "sowCode": "1",
                "stagingAreaCode": "机动", "productionBatch": "2402071",
                "productionDate": "2023-05", "invalidDate": "2026-04", "pickQty": 180, "sowQty": 0, "unSowQty": 180,
                "perQty": 180, "pickJianQty": 1, "sowJianQty": 0, "unSowJianQty": 1, "instrumentModel": None,
                "scanSowQty": "1", "pickTaskNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'pick_task_code')}"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"PDA整件一件拣货接口": response_time}

    @staticmethod
    def jh_fh_current_list():
        url = "http://192.168.111.108:9994/wms/ob/outReview/queryOutReviewByTaken"
        data = {"isPda": 1}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核已索取列表接口": response_time}

    @staticmethod
    def jh_fh_wait_list():
        url = "http://192.168.111.108:9994/wms/ob/outReview/statisticsWaitTaskForPDA"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核未索取列表接口": response_time}

    @staticmethod
    def jh_fh_get():
        get_order_id_url = "http://192.168.111.107:9994/wms/ob/outReview/queryOutReviewByWaitTake"
        get_order_id_data = {"cusOrderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                             "orderByColumnList": [], "page": 1, "limit": 50}
        headers = get_token()
        get_order_id = requests.post(url=get_order_id_url, headers=headers, json=get_order_id_data).json()
        for i in get_order_id['obj']:
            get_box_url = f"http://192.168.111.107:9994/wms/ob/outReview/queryOutReviewDt/{i['key']}"
            get_box_data = {}
            get_box = requests.post(url=get_box_url, headers=headers, json=get_box_data).json()
            for box_data in get_box['obj']:
                url = f"http://192.168.111.108:9994/wms/ob/outReview/pda/takeTask?outBoxNo={box_data['outBoxNo']}"
                write_yaml(base_path('data.yaml'), 'order_data', 'box_no', box_data['outBoxNo'])
                headers = get_token()
                start_time = time.time()
                res = requests.post(url=url, headers=headers)
                end_time = time.time()
                write_yaml(base_path('data.yaml'), 'order_data', 'fh_id', res.json()['obj'])
                response_time = end_time - start_time
                return {"集货复核索取任务接口": response_time}

    @staticmethod
    def jh_fh_work():
        url = "http://192.168.111.108:9994/wms/ob/outReview/scanSignForPDA"
        data = {"creator": "lhb", "creatorName": "李鸿宾",
                "id": f"{read_yaml(base_path('data.yaml'), 'order_data', 'fh_id')}",
                "sign": f"{read_yaml(base_path('data.yaml'), 'order_data', 'box_no')}"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核签收接口": response_time}

    @staticmethod
    def jh_fh_review():
        url = "http://192.168.111.108:9994/wms/ob/outReview/reviewSignForPDA"
        data = {"creator": "lhb", "creatorName": "李鸿宾",
                "id": f"{read_yaml(base_path('data.yaml'), 'order_data', 'fh_id')}",
                "sign": f"{read_yaml(base_path('data.yaml'), 'order_data', 'box_no')}"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        write_yaml(base_path('data.yaml'), 'order_data', 'fh_review_id', res.json()['obj']['key'])
        response_time = end_time - start_time
        return {"集货复核复核接口": response_time}

    @staticmethod
    def jh_fh_drug():
        url = "http://192.168.111.108:9994/wms/pda/drug/drugElectrSuperviseCodeCollection/scanDrugSupervisionCode"
        data = {"electrSuperviseCode": "81111111118111111111",
                "reviewId": f"{read_yaml(base_path('data.yaml'), 'order_data', 'fh_review_id')}",
                "orderNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'order_no')}",
                "originId": read_yaml(base_path('data.yaml'), "order_data", "so_id"),
                "originNo": f"{read_yaml(base_path('data.yaml'), 'order_data', 'so_no')}",
                "originType": "OUT", "reviewType": "OUT", "productionBatch": "2402071", "ownerId": 103,
                "skuCode": "M00005662", "orderType": "PFXSD", "skuId": 1238587950765056, "shouldGatherQty": 180,
                "batchNo": "P24041800317"}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核追溯码接口": response_time}

    @staticmethod
    def jh_fh_done():
        url = "http://192.168.111.108:9994/wms/ob/outReview/reviewDoneForPDA"
        data = {"id": read_yaml(base_path('data.yaml'), 'order_data', 'fh_id')}
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"集货复核完成接口": response_time}

    @staticmethod
    def lh_pick_get():
        url = "http://192.168.111.108:9994/wms/pda/ob/lhPick/scannPickTaskNoOrContainerNo/G"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"零货拣货索取任务接口": response_time}

    @staticmethod
    def zj_pick_get():
        url = "http://192.168.111.108:9994/wms/pda/ob/zjPick/scannPickTaskNo/G"
        headers = get_token()
        start_time = time.time()
        res = requests.post(url=url, headers=headers, json=data)
        end_time = time.time()
        response_time = end_time - start_time
        return {"整件拣货索取任务接口": response_time}


#
# # 按顺序调用所有接口
# print(PdaResponseTest.lh_pick_list())
# print(PdaResponseTest.zj_pick_list())
# print(PdaResponseTest.zj_pick_detail())
# print(PdaResponseTest.zj_pick_warehouse())
# print(PdaResponseTest.zj_pick())
# print(PdaResponseTest.zj_bz_detail())
# print(PdaResponseTest.zj_bz_commodity())
# print(PdaResponseTest.zj_bz_details())
# print(PdaResponseTest.zj_bz())
# print(PdaResponseTest.jh_fh_current_list())
# print(PdaResponseTest.jh_fh_wait_list())
# print(PdaResponseTest.jh_fh_get())
# print(PdaResponseTest.jh_fh_work())
# print(PdaResponseTest.jh_fh_review())
# print(PdaResponseTest.jh_fh_drug())
# print(PdaResponseTest.jh_fh_done())

# print(PdaResponseTest.zj_bz_commodity())

# 禁用特定警告
warnings.filterwarnings("ignore", category=UserWarning, module='mpld3')

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# 接口名称和响应时间
data = {
    "PDA零货拣货列表查询接口": PdaResponseTest.lh_pick_list()['PDA零货拣货列表查询接口'],
    "PDA整件拣货列表查询接口": PdaResponseTest.zj_pick_list()['PDA整件拣货列表查询接口'],
    "PDA整件详情接口": PdaResponseTest.zj_pick_detail()['PDA整件详情接口'],
    "PDA整件拣货货位查询接口": PdaResponseTest.zj_pick_warehouse()['PDA整件拣货货位查询接口'],
    "PDA整件拣货接口": PdaResponseTest.zj_pick()['PDA整件拣货接口'],
    "PDA整件拣货详情接口": PdaResponseTest.zj_bz_detail()['PDA整件拣货详情接口'],
    "PDA整件拣货商品接口": PdaResponseTest.zj_bz_commodity()['PDA整件拣货商品接口'],
    "PDA整件拣货明细接口": PdaResponseTest.zj_bz_details()['PDA整件拣货明细接口'],
    "PDA整件一件拣货接口": PdaResponseTest.zj_bz()['PDA整件一件拣货接口'],
    "集货复核已索取列表接口": PdaResponseTest.jh_fh_current_list()['集货复核已索取列表接口'],
    "集货复核未索取列表接口": PdaResponseTest.jh_fh_wait_list()['集货复核未索取列表接口'],
    "集货复核索取任务接口": PdaResponseTest.jh_fh_get()['集货复核索取任务接口'],
    "集货复核签收接口": PdaResponseTest.jh_fh_work()['集货复核签收接口'],
    "集货复核复核接口": PdaResponseTest.jh_fh_review()['集货复核复核接口'],
    "集货复核追溯码接口": PdaResponseTest.jh_fh_drug()['集货复核追溯码接口'],
    "集货复核完成接口": PdaResponseTest.jh_fh_done()['集货复核完成接口'],
    "零货拣货索取任务接口": PdaResponseTest.lh_pick_get()['零货拣货索取任务接口'],
    "整件拣货索取任务接口": PdaResponseTest.zj_pick_get()['整件拣货索取任务接口']
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
