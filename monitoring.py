import streamlit as st
import psutil
import time

st.set_page_config(page_title="실시간 자원 모니터링", layout="wide")

st.title("🔍 실시간 Python 자원 모니터링 대시보드")

# 실시간 업데이트 간격 (초)
refresh_interval = st.slider("업데이트 간격 (초)", 0.5, 5.0, 1.0, step=0.5)

cpu_chart = st.empty()
mem_chart = st.empty()

cpu_usage_list = []
mem_usage_list = []

max_points = 60  # 그래프에 표시할 최대 시간 (초)

# 실시간 루프
while True:
    cpu = psutil.cpu_percent()
    mem = psutil.virtual_memory().percent

    cpu_usage_list.append(cpu)
    mem_usage_list.append(mem)

    # 리스트 길이 제한
    if len(cpu_usage_list) > max_points:
        cpu_usage_list.pop(0)
        mem_usage_list.pop(0)

    # 그래프 갱신
    cpu_chart.line_chart(cpu_usage_list, height=200, use_container_width=True)
    mem_chart.line_chart(mem_usage_list, height=200, use_container_width=True)

    time.sleep(refresh_interval)
