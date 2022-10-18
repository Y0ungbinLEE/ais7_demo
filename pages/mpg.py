import streamlit as st
import pandas as pd
import seaborn as sns
import plotly.express as px
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 공식 문서를 찾아 프로젝트에 적용해보기
#head 부분
st.set_page_config(
    page_title="Likelion AI School 자동차 연비 App",
    page_icon="🚗",
    layout="wide",
)

st.markdown("# 자동차 연비 🚗")
st.sidebar.markdown("# 자동차 연비 🚗")



#깃헙에 파일업로드 후 raw 클릭해서 주소 가져오기
url = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mpg.csv"
# data = pd.read_csv(url)

@st.cache  # 데이터용량이 큰 경우 데이터 로드가 오래 걸리기 때문에 한번 로드했으면 새로 로드하지 않고 기존 데이터를 사용해 부담을 줄이기 위해, 속도문제도 해결 
def load_data():
    data = pd.read_csv(url)
    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year',
   list(reversed(range(data.model_year.min(),data.model_year.max())))
   ) #연도 선택할수 있게 값을 넣음 연도 정렬해서 최근 연도가 위에 오게 하기 위해 reversed값

if selected_year > 0 : #선택된 값이 0보다 클때
   data = data[data.model_year == selected_year]


# Sidebar - origin
sorted_unique_origin = sorted(data.origin.unique())
selected_origin = st.sidebar.multiselect('origin', sorted_unique_origin, sorted_unique_origin)

if len(selected_origin) > 0:
   data = data[data.origin.isin(selected_origin)]


st.dataframe(data)

st.line_chart(data["mpg"])

st.bar_chart(data["mpg"])


fig, ax = plt.subplots(figsize=(10, 3))
sns.countplot(data=data, x="origin").set_title("지역별 자동차 연비 데이터 수")
st.pyplot(fig)

pxh = px.histogram(data, x="origin", title="지역별 자동차 연비 데이터 수")
st.plotly_chart(pxh)


fig1 = px.scatter(
    data, x='origin', y='weight',  trendline_color_override='darkblue')
st.pyplot(fig1)
