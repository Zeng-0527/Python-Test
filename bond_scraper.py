import requests
import csv
import time
import json

base_url = "https://www.chinamoney.com.cn/ags/ms/"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.chinamoney.com.cn/english/bdInfo/",
    "Content-Type": "application/x-www-form-urlencoded",
}


# 第一步：先获取bondType的编号，因为接口需要传编号不是传名字
def getTypeCode():
    url = base_url + "cm-u-bond-md/BondBaseInfoSearchConditionEN"
    response = requests.get(url, headers=headers, timeout=15)
    data = response.json()
    for item in data["data"]["bondType"]:
        if item["bondDisplayType"] == "Treasury Bond":
            return item["bondTypeCode"]
    return None


# 第二步：根据pageNo去请求每一页的数据
def getData(bondTypeCode, year, pageNo, pageSize=15):
    url = base_url + "cm-u-bond-md/BondMarketInfoListEN"

    params = {
        "pageNo": pageNo,
        "pageSize": pageSize,
        "bondType": bondTypeCode,
        "issueYear": str(year),
        "isin": "",
        "bondCode": "",
        "issueEnty": "",
        "couponType": "",
        "rtngShrt": "",
        "bondSpclPrjctVrty": "",
    }
    response = requests.post(url, headers=headers, data=params, timeout=30)
    return response.json()


def main():
    print("开始爬取数据...")
    print("网站是: https://www.chinamoney.com.cn/english/bdInfo/")
    print("筛选条件: Bond Type = Treasury Bond, Issue Year = 2023")
    print("========================================")

    bondTypeCode = getTypeCode()
    print("Treasury Bond 的编号是: " + str(bondTypeCode))

    # 先请求第一页看看总共有多少条数据
    firstPage = getData(bondTypeCode, 2023, 1)
    total = firstPage["data"]["total"]
    totalPages = firstPage["data"]["pageTotal"]

    print("一共有 " + str(total) + " 条数据")
    print("需要爬 " + str(totalPages) + " 页")
    print("========================================")

    allData = []

    # 把第一页的数据先加进去
    for bond in firstPage["data"]["resultList"]:
        allData.append({
            "ISIN": bond["isin"],
            "Bond Code": bond["bondCode"],
            "Issuer": bond["entyFullName"],
            "Bond Type": bond["bondType"],
            "Issue Date": bond["issueStartDate"],
            "Latest Rating": bond["debtRtng"],
        })

    # 从第2页开始继续爬
    for page in range(2, totalPages + 1):
        time.sleep(0.5)  # 睡一下，太快怕被封
        print("正在爬第 " + str(page) + " 页...")
        result = getData(bondTypeCode, 2023, page)
        for bond in result["data"]["resultList"]:
            allData.append({
                "ISIN": bond["isin"],
                "Bond Code": bond["bondCode"],
                "Issuer": bond["entyFullName"],
                "Bond Type": bond["bondType"],
                "Issue Date": bond["issueStartDate"],
                "Latest Rating": bond["debtRtng"],
            })

    print("爬完了！一共 " + str(len(allData)) + " 条")

    filename = "treasury_bonds_2023.csv"
    file = open(filename, "w", newline="", encoding="utf-8-sig")
    writer = csv.writer(file)

    # 先写表头
    writer.writerow(["ISIN", "Bond Code", "Issuer", "Bond Type", "Issue Date", "Latest Rating"])

    # 逐行写入数据
    for item in allData:
        writer.writerow([
            item["ISIN"],
            item["Bond Code"],
            item["Issuer"],
            item["Bond Type"],
            item["Issue Date"],
            item["Latest Rating"],
        ])

    file.close()
    print("数据已经保存到: " + filename)

    # 打印前5条看看
    print("\n=== 前5条数据预览 ===")
    for i in range(5):
        print("第" + str(i + 1) + "条: " + allData[i]["ISIN"] + " | " + allData[i]["Bond Code"] + " | " + allData[i]["Issuer"][:30] + "... | " + allData[i]["Issue Date"])


if __name__ == "__main__":
    main()
