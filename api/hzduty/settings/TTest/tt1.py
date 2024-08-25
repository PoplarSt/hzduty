
# @router.post(
#     "/addOrUpdateOrDeleteShifts2",
#     status_code=201,
#     summary="添加或更新或删除班次2"
# )
# async def add_update_delete2(zone_id: str, new_data: list[ShiftType], db=Depends(HZDUTY.session)):
#     print(new_data)
#     print(zone_id)
#     # 从数据库删除前端删掉的班次类型
#     shift_type_id_exists = []
#     new_shift_type = []
#
#     shift_id_exists = []
#     new_shift = []
#
#     for shift_type in new_data:
#         if (shift_type.值班班次类型ID):
#
#             shift_type_id_exists.append(shift_type.值班班次类型ID)
#         else:
#             new_shift_type.append(shift_type.model_dump())
#
#         for shift in shift_type.班次:
#             if (shift.值班班次ID):
#                 shift_id_exists.append(
#                     shift.值班班次ID)
#             else:
#                 new_shift.append(shift.model_dump())
#     print(new_shift)
#     query = delete(班次类型).where(and_(
#         班次类型.行政区划 == zone_id,
#         班次类型.值班班次类型ID not in shift_type_id_exists
#     ))
#     query1 = delete(班次).where(and_(
#         班次.值班班次ID not in shift_id_exists,
#     ))
#
#     await db.execute(query)
#     await db.execute(query1)
#     # 插入新增的班次类型
#
#     if (new_shift_type):
#         print(new_shift_type)
#         # query2 = insert(班次类型).values(new_shift_type)
#         # await db.bulk_insert_mappings(班次类型, new_shift_type)
#     if (new_shift):
#         print(new_shift)
#
#         query3 = insert(班次).values(new_shift)
#
#         await db.execute(query3)
#         # await db.bulk_insert_mappings(班次, new_shift)
#
#     return new_data
