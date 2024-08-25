data={
  "code": "000000",
  "data": [
    {
      "值班班次类型": "节假日班次",
      "值班班次类型ID": 13,
      "可删除": 0,
      "班次": [
        {
          "值班班次ID": 12,
          "开始时间": "10:56:06",
          "班次名称": "晚班"
        },
{
          "值班班次ID": 13,
          "开始时间": "10:56:06",
          "班次名称": "晚班"
        }
      ]
    },
    {
      "值班班次类型": "平时班次",
      "值班班次类型ID": 14,
      "可删除": 1,
      "班次": []
    }
  ],
  "message": "操作成功"
}
new_data={
  "code": "000000",
  "data": [
    {
      "值班班次类型": "节假日班次",
      "值班班次类型ID": 13,
      "可删除": 0,
      "班次": [
        {
          "值班班次ID": 12,
          "开始时间": "10:56:06",
          "班次名称": "晚班改了改了改了"
        },
{
          "值班班次ID": 13,
          "开始时间": "10:56:06",
          "班次名称": "晚班改了改了改了"
        }

      ]
    },
    {
      "值班班次类型": "平时班次",
      "值班班次类型ID": 14,
      "可删除": 1,
      "班次": []
    }
  ],
  "message": "操作成功"
}
updated_shifts = []

# 遍历新数据中的每个班次类型
for new_st in new_data["data"]:
    new_type_id = new_st["值班班次类型ID"]
    new_shifts = new_st["班次"]

    # 找到旧数据中对应的班次类型
    for old_st in data["data"]:
        if old_st["值班班次类型ID"] == new_type_id:
            old_shifts = old_st["班次"]

            # 比较新旧班次列表
            for new_shift in new_shifts:
                for old_shift in old_shifts:
                    if new_shift["值班班次ID"] == old_shift["值班班次ID"]:
                        # 检查属性是否有更新
                        if (
                                new_shift.get("开始时间") != old_shift.get("开始时间") or
                                new_shift.get("班次名称") != old_shift.get("班次名称")
                        ):
                            # 记录更新的班次
                               updated_shifts.append(new_shift)

# 打印更新的班次信息
# for update in updated_shifts:
#     print("更新的班次属性：")
#     print("值班班次ID:", update["值班班次ID"])
#     print("旧属性:", update["旧属性"])
print(updated_shifts)