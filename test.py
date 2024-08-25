from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, delete, and_
from sqlalchemy.orm import Session
from api.hzduty.settings.TTest.model import 班次类型, 班次  # 假设这是您的模型定义
from api.hzduty.settings.TTest.database import HZDUTY  # 假设这是您的数据库依赖

router = APIRouter(tags=["Test"])

@router.post(
    "/teamstest/",
    summary="读取班次类型"
)
async def query_teams_type(zone_id: int, db: Session = Depends(HZDUTY.session)):
    try:
        # 获取所有班次类型
        query = select(班次类型).filter(班次类型.行政区划 == zone_id).options(joinedload(班次类型.班次))
        db_shift_types = await db.execute(query)
        shift_types = db_shift_types.scalars().all()

        # 假设 new_data 是从前端接收的新班次数据
        new_data = {
            1: {"shift_id_exists": [101, 102], "new_shift": [
                {"值班班次类型": "Type A", "班次名称": "Shift 1", "开始时间": "08:00"},
                {"值班班次类型": "Type A", "班次名称": "Shift 2", "开始时间": "09:00"}
            ]},
            2: {"shift_id_exists": [103], "new_shift": [
                {"值班班次类型": "Type B", "班次名称": "Shift 3", "开始时间": "10:00"}
            ]},
        }

        for shift_type_id, data in new_data.items():
            for j in data["new_shift"]:
                print(j)  # 打印原始的 j
                print(j.model_dump())  # 打印 j.model_dump() 的结果
                if isinstance(j, 班次):  # 确保 j 是 班次 类型实例
                    new_shift = 班次(**j.model_dump())  # 创建新的 班次 实例
                    shift_type = db.query(班次类型).filter_by(行政区划=zone_id, 值班班次类型ID=shift_type_id).first()
                    if shift_type:
                        shift_type.班次.append(new_shift)
                        db.add(new_shift)
                        db.commit()

        return {"message": "班次更新成功"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=503, detail=str(e))

    finally:
        await db.close()