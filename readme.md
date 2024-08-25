# 后端接口服务

## 程序文档


### **测试项目使用**

- [**测试接口**](/api/v1.0/test/rapidoc) 

- [**测试代码生成**](/api/v1.0/autoCode/rapidoc) 

- [**测试护民之盾业务**](/api/v2.0/shield/rapidoc) 



## 接口文档图例:

        🔒:超级管理员（非运维人员勿动）
        👮:人防管理员权限（人防单位的人，主要从web端后台进行管理）
        🧑‍💼:普通员工（基层工作人员，如网格员等）
        🙍:普通民众（民众权限，如护民之盾、答题等）
        🧑:有token即可（要求登录账号才能使用的接口）
           :如没有上述图标，则可以直接查询，如APP首页图标的配置

        🛠️:设定项（修改设定需改动程序）
        ⚙️:配置项（运维人员通过修改数据库/配置文件实现功能变化，无需改动程序）
        ⏰:带有缓存

        🔴:开发中，存在已知问题，不能使用
        🟡:测试中，可能存在问题
        🔵:生产中，新增或近期有修改的接口
        🟢:生产中
        🟤:废弃中，即将暂停使用
        ⚪:暂停中，功能不明确，未来可能添加的接口


## 其他服务

### 1、文件预览服务

> 文件预览使用kkfileview，通过接口获取文件路径，返回预览地址，前端通过iframe加载预览地址。
> [**文件预览文档**](/onlinePreview/index)
> 使用方法：'/onlinePreview/onlinePreview?url=' + encodeURIComponent(base64Encode(url));
> 例如：https://example.irenfang.cn/onlinePreview/onlinePreview?officePreviewType=pdf&url=aHR0cHM6Ly9uYW5qaW5nLmlyZW5mYW5nLmNuOjgzMjEvZmlsZS9zaGllbGQvOWJmMGY5NzYyYTZiZGVkNzQzMDQzNjE1ZmE1YmQyNDZmY2I5YWIxZTliOTc3Zjc5MDkyYzY0YTc1MWZlZTVhZC5wbmc%3D
> 这里需要两层onlinePreview，是考虑到nginx反向代理，其中第一个onlinePreview可以有后端人员在部署docker和nginx时配置，第二个onlinePreview是kk本身需要的参数。目前生产环境暂时保持两个onlinePreview的形式。


   部署方案（参考docker-compose）:
   ```yaml
   version: '3'
   services:
      # 文件预览
      fileview:
         image: keking/kkfileview:4.1.0
         restart: always
         ports:
            - 8012:8012
         environment:
            KK_FILE_DIR: "/data/file"  # 文件路径地址
            KK_BASE_URL: "https://example.irenfang.cn/onlinePreview/"  # 配置nginx方向代理转发需要用到，详见官方文档
            KK_CONTEXT_PATH: "/onlinePreview/"  # 配置nginx方向代理转发需要用到，详见官方文档
   ```
   nginx配置：
   ```nginx
   # kkfileview 文件预览服务
   location /onlinePreview/ {
      proxy_set_header Host $host;  
      proxy_set_header X-Real-IP $remote_addr;  
      proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_pass http://172.18.0.1:8012/onlinePreview/;
   }
   ```

# 接口说明

## 列表接口

- 分页功能

- 列表接口排序功能

  排序字段接收两个元素的列表，在前的优先级较高

  对于时间、数字、字符类型可以直接使用是否降序控制

  对于状态，可以按照提供的列表顺序进行排序

  例如：

```
   "排序字段": [
      {
         "字段": "状态",
         "降序": false,
         "顺序": [
            "编辑中",
            "发布"
         ]
      },
      {
         "字段": "创建时间",
         "降序": true
      }
   ]
```

## 经纬度序列

部分接口支持动态修改经纬度序列

headers：
coordinate-system: wgs84



