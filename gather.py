import re
import sys
import requests
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem



headers = {
    "X-QuakeToken": "",
    "Content-Type": "application/json"
}

data = {
     "query":'',
     "size":20,
     "ignore_cache": True,
}

def xinxi(url, key):
    data['query'] = url
    headers['X-QuakeToken'] = key
    response = requests.post(url="https://quake.360.net/api/v3/search/quake_service", headers=headers, json=data)
    a = response.json()
    results = []
    for i in range(data["size"]):
        host = a["data"][i]["service"]["http"]['host']
        status = a["data"][i]["service"]["http"]['status_code']
        ip = a["data"][i]["ip"]
        port = a["data"][i]["port"]
        icp = a["data"][i]["service"]["http"]['information']['icp']
        components = a["data"][i]["components"]
        match = re.search('\d+', host)
        if match:
            components_str = " ".join([f" {d['product_name_cn']}" for d in components])
            if icp:
                result = f"http://{host}:{port}  port:{port} ip:{ip}   status:{status} icp:{icp} 组件:{components_str}"
                results.append(result)
            else:
                result = f"http://{host}:{port}  port:{port} ip:{ip}   status:{status} icp:空 组件:{components_str}"
                results.append(result)
        else:
            components_str = " ".join([f"{d['product_name_cn']}" for d in components])
            if icp:
                result = f"https://{host}  port:{port} ip:{ip}   status:{status} icp:{icp} 组件:{components_str}"
                results.append(result)
            else:
                result = f"https://{host}  port:{port} ip:{ip}   status:{status} icp:空 组件:{components_str}"
                results.append(result)
    return results

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("星航一代")
        self.resize(800, 600)

        # 创建主窗口部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建布局管理器
        main_layout = QVBoxLayout(central_widget)
        url_layout = QHBoxLayout()
        key_layout = QHBoxLayout()
        button_layout = QHBoxLayout()

        # 创建 URL 标签、文本框和布局
        url_label = QLabel("查询语句:")
        self.url_edit = QLineEdit()
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_edit)

        # 创建 Key 标签、文本框和布局
        key_label = QLabel("token:")
        self.key_edit = QLineEdit()
        key_layout.addWidget(key_label)
        key_layout.addWidget(self.key_edit)

        # 创建搜索按钮和布局
        search_button = QPushButton("导入")
        search_button.clicked.connect(self.daoru_data)
        button_layout.addWidget(search_button)

        # 创建表格控件
        self.table_widget = QTableWidget()
        main_layout.addLayout(url_layout)
        main_layout.addLayout(key_layout)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(self.table_widget)


    def daoru_data(self):
        # 先设置表格控件的列数
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(["域名", "端口", "ip", "状态", "备案", "组件"])

        # 调用 xinxi 函数获取响应数据
        url = self.url_edit.text()
        key = self.key_edit.text()
        results = xinxi(url, key)

        # 将结果添加到表格控件中
        # 将结果添加到表格控件中
        for i, result in enumerate(results):
            data = result.strip().split()
            url = data[0]
            port = data[1].split(':')[1]
            ip = data[2].split(':')[1]
            status = data[3].split(':')[1]
            icp = data[4].split(':')[1]
            component = ','.join(data[5:]).split('组件:')[1]
            self.table_widget.insertRow(i)
            self.table_widget.setItem(i, 0, QTableWidgetItem(url))
            self.table_widget.setItem(i, 1, QTableWidgetItem(port))
            self.table_widget.setItem(i, 2, QTableWidgetItem(ip))
            self.table_widget.setItem(i, 3, QTableWidgetItem(status))
            self.table_widget.setItem(i, 4, QTableWidgetItem(icp))
            self.table_widget.setItem(i, 5, QTableWidgetItem(component))

        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
