# IDS2018-DDoS-Traffic-Classify

杭电综合项目实践源代码，主要包括：
- **模型训练**：基于公开的入侵检测数据集IDS 2018中Thursday-15-02这一天的数据，使用LightGBM和XGBoost算法训练DDoS流量分类模型，实现对正常流量和DDoS流量的分类，模型五折交叉验证AUC达到0.99
- **流量采集与分类**：基于软件定义网络虚拟环境Mininet搭建了一个简单的网络拓扑，通过使用sFlow RT采集网络流量，并利用DDoS流量分类模型进行检测，模型AUC为0.81

## 目录
- [依赖](#依赖)
- [使用](#使用)
    - [数据集下载](#数据集下载)
    - [模型训练](#模型训练)
    - [流量采集与分类](#流量采集与分类)
- [License](#License)

## 依赖

- Anaconda 3环境
- pip install lightgbm
- pip install xgboost

## 使用

### 数据集下载

数据集存储在AWS上，因此首先需要安装[AWS CLI](https://aws.amazon.com/cn/cli/)。

安装完成后，在命令行中输入以下命令查看目录下的所有文件：
```shell
aws s3 ls --no-sign-request "s3://cse-cic-ids2018" --recursive --human-readable --summarize
```

下载数据集：
```shell
aws s3 cp --no-sign-request "s3://cse-cic-ids2018/Processed Traffic Data for ML Algorithms/Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv" G:\
```

AWS CLI下载并不稳定，可以直接访问http://cse-cic-ids2018.s3.amazonaws.com/Processed%20Traffic%20Data%20for%20ML%20Algorithms/Thursday-15-02-2018_TrafficForML_CICFlowMeter.csv 下载。

### 模型训练

| 文件 | 内容 |
| - | - |
| dataset_understanding.ipynb | 数据理解 |
| EDA.ipynb | 数据探索性分析 |
| feature_engineering.ipynb | 特征工程 |
| baseline.ipynb | initial baseline |
| baseline2.ipynb | final baseline |

### 流量采集

两台虚拟机，安装Ubuntu，一台作为sFlow Collector，另一台作为sFlow Agent。

#### sFlow Collector

配置JDK环境，下载sFlow RT 3.0，安装sFlow RT流量分析APP flow-trend和browse-metrics：
```shell
./sflow-rt/get-app.sh sflow-rt flow-trend
./sflow-rt/get-app.sh sflow-rt browse-metrics
```
启动
```shell
./sflow-rt/start.sh
```
访问localhost:8008打开Web界面，sFlow Collector接收sFlow Agent数据在6343端口。

#### sFlow Agent

配置Mininet环境，mn创建拓扑。

设置交换机开启sFlow功能：
```shell
ovs-vsctl -- --id=@sflow create sflow agent=eth0 target=\"192.168.222.129:6343\" sampling=10 polling=1 -- set bridge s1 sflow=@sflow
```
查看已配置的sFlow Agent：
```shell
ovs-vsctl list sflow
```

查看网络链路情况：
```shell
ip link
```

#### 定义流

./sflow_traffic/define_flow.py

#### 采集流量

./sflow_traffic/get_data_from_sflow.py

### 流量分类

./sflow_traffic/sflow_traffic_classift.ipynb

## License

[GPL](https://github.com/Bil369/IDS2018-DDoS-Traffic-Classify/blob/main/LICENSE) © [Bil369](https://github.com/Bil369)