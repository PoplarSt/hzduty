FROM python:3.12.4-slim

WORKDIR  /code


COPY ./requirements.txt /code/requirements.txt
ENV TZ=Asia/Shanghai



RUN  python -m  pip install --upgrade pip && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple pydantic-resolve==1.6.3 --no-cache-dir && \
    pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --no-cache-dir
    # --no-dependencies



ADD . /code
ENV PYTHONPATH=.:/code

EXPOSE 8080

# RUN chmod a+x run.sh
# CMD ./run.sh

CMD ["uvicorn", "main:app","--proxy-headers", "--host", "0.0.0.0", "--port", "8080", "--workers", "2"]
# CMD ["hypercorn", "app:app", "--bind", "0.0.0.0:8080"]

