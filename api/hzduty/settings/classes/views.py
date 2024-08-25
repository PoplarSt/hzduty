from datetime import datetime

from fastapi import FastAPI, HTTPException, Depends
from fastapi import APIRouter, Depends
from sqlalchemy import select, delete, and_, insert
from sqlalchemy.orm import joinedload

from api.hzduty.settings.classes.interface import OrgID
from api.hzduty.settings.classes.schemas import *
from core.database import HZDUTY
from api.hzduty.settings.classes.model import 班次, 班次类型
from api.hzduty.settings.classes.crud import read_shift_types

router = APIRouter(tags=["班次管理"])


@router.post("/shift_types/",
             summary="读取",
             )
async def read_shift_types1(id: OrgID, db=Depends(HZDUTY.session)):
    zone_id = id.组织ID
    shift_types = await read_shift_types(zone_id=zone_id, db=db)
    response = Response(code="000000", data=shift_types, message="操作成功")
    return response


@router.post(
    "/addOrUpdateOrDeleteShifts",
    status_code=201,
    summary="添加或更新或删除班次"
)
async def add_update_delete(id: OrgID, new_data: dict, db=Depends(HZDUTY.session)):
    data = await read_shift_types1(id, db=db)

    miss = []
    updated_shifts = []
    # 初始化一个空列表来存储值班班次ID
    new_exists_id = []

        # 假设 new_data["data"] 是一个字典，并且 "班次" 是其中的键
    for new_shift in new_data["data"]:
            for new in new_shift["班次"]:
                if "值班班次ID"  in new:  # 使用 get 方法来避免 KeyError
                    new_exists_id.append(new["值班班次ID"])


    for st in new_data["data"]:
        name = st.get("值班班次类型")
        id = st.get("值班班次类型ID")
        for s in st.get("班次", []):  # 使用 get 方法安全地获取 "班次" 键值
            if "值班班次ID" not in s:
                miss.append({
                    "值班班次类型": name,  # 这里使用变量 name
                    "值班班次类型ID": id,  # 这里使用变量 id
                    "班次": s
                })

    for new_st in new_data["data"]:
        new_type_id = new_st["值班班次类型ID"]
        new_shifts = new_st["班次"]
        # 找到旧数据中对应的班次类型
        for old_st in data.data:
            if old_st.值班班次类型ID == new_type_id:
                old_shifts = old_st.班次
                # 比较新旧班次列表
                for new_shift in new_shifts:
                    for old_shift in old_shifts:
                        if "值班班次ID" in new_shift:
                            if old_shift.值班班次ID == new_shift["值班班次ID"]:
                                #     # 添加新班次
                                #     # 检查属性是否有更新
                                new_shift_time = datetime.strptime(new_shift["开始时间"], "%H:%M:%S").time()
                                if (
                                        new_shift_time != old_shift.开始时间 or
                                        new_shift.get("班次名称") != old_shift.班次名称
                                ):
                                    # 记录更新的班次
                                    updated_shifts.append(new_shift)


    try:
        count1 = []  # 存储更新的班次信息
        count = []  # 存储添加的班次信息


        # 构建删除查询，这里假设 班次 是一个 SQLAlchemy 模型
        query = delete(班次).filter(班次.值班班次ID.not_in(new_exists_id))

        # 执行删除操作，这里不需要 .scalars()，也不需要 await，因为这是一个删除操作
        await db.execute(query)

        # 找到旧数据中值班班次类型ID相同的班次类型

        # for new_st in new_data["data"]:
        #     new_shift_ids = {shift["值班班次ID"] for shift in new_st["班次"] if "值班班次ID" in shift}
        #
        #     for old_shift_type in data.data:
        #        if old_shift_type.值班班次类型ID == new_st["值班班次类型ID"]:
        #         # 查询旧数据中的班次ID
        #           query = select(班次).filter(班次.type == old_shift_type.值班班次类型ID)
        #           old_shifts = await db.scalars(query)
        #           old_shift_ids = {shift.值班班次ID for shift in old_shifts.all()}
        #
        #         # 找出需要删除的班次ID
        #           shifts_to_delete = old_shift_ids - new_shift_ids
        #         # 构建删除操作
        #           for shift_id in shifts_to_delete:
        #             item = await db.scalars(select(班次).filter(班次.值班班次ID == shift_id))
        #             await db.delete(item.first())


        # 更新已有的班次
        for u in updated_shifts:
            if "值班班次ID" in u and u["值班班次ID"] is not None:
                clas = u["班次名称"]
                act = u["开始时间"]
                ID = u["值班班次ID"]
                query = select(班次).filter(班次.值班班次ID == ID)
                existing_shift = await db.scalar(query)
                if existing_shift:
                    existing_shift.班次名称 = clas
                    existing_shift.开始时间 = act
                    await db.commit()
                    await db.refresh(existing_shift)
                    count1.append(existing_shift)

        # 添加缺少值班班次ID的班次
        for m in miss:
            type = m["值班班次类型ID"]
            type_name = m["值班班次类型"]
            data = m["班次"]
            clas = data["班次名称"]
            act = data["开始时间"]
            new_event = 班次(
                type_name=type_name,
                班次名称=clas,
                开始时间=act,
                type=type
                # 假设没有值班班次ID，这里不设置
            )
            db.add(new_event)
            await db.commit()
            await db.refresh(new_event)
            count.append(new_event)
        return {"updated": count1, "added": count}
        return count
    except ValueError as e:
        raise HTTPException(status_code=400, detail="无效的时间格式")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
