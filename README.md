### 运行依赖
同时运行前端和后端后，访问前端端口进行交互。
#### 后端（`backend`）
请先确保python已安装好库：
- `Flask`
- `openpyxl`
- `pyechart`
- `scikit-learning`(模型占位)
  
再使用以上解释器运行`\backend\flaskr`目录下的`app.py`文件，终端输出端口号时运行成功。

#### 前端（`frontend`）
可参考[教程](https://blog.csdn.net/Javachichi/article/details/132868889)完成npm、vue的安装。\
在`\frontend`目录下，首先运行`npm install`安装所需依赖，再运行指令`npm run serve`启动前端，终端输出端口号时运行成功。
- 根据经验可能还需要手动运行`npm install echarts`指定安装ECharts
