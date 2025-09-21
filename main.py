import streamlit as st
from google_spreadsheet_connection import conn,sheet_transactions,sheet_targets
import streamlit as st
from numpy.random import default_rng as rng
import pandas as pd
from millify import millify
import numpy as np
import plotly.express as px
css = """
.st-key-first_container1, .st-key-first_container2, .st-key-first_container3, 
.st-key-first_container5,.st-key-first_container6,.st-key-first_container7,.st-key-first_container8,
.st-key-first_container9, .st-key-first_container10, .st-key-first_container11{
    border-radius: 20px;
}

.st-key-second_container {
    background-color: #2d3267;
    padding:20px;
    border-radius:20px;
}

"""

st.html(f"<style>{css}</style>")

st.set_page_config(page_title="Dashboard Dompetku", layout="wide")
st.logo("assets/logo.png", icon_image="assets/logo.png")

# ------------------------
# TODO Title & Control
# ------------------------
title,control,profile = st.columns([1,2,1])
with title:
    st.markdown("""
    <h1 style='margin-bottom:-90px; font-size:30px;'>Available Balance</h1>
    """, unsafe_allow_html=True)
    st.subheader(":green[Rp. 20.000.000]")

with control:
    row = st.container(horizontal=True)
    with row:
        st.date_input(label="",max_value="today",value="today")

with profile:
    st.write("")
    st.write("")
    col1, col2 = st.columns([3,1]) 
    with col1:
        st.markdown(
            """
            <p style='text-align:right; margin-bottom:-5px; font-size:20px; font-weight:bold;'>Andre Mamank</p>
            <p style='text-align:right; color: grey; font-size:16px;'>Marketing Staff</p>
            """,
            unsafe_allow_html=True
        )
    with col2:
        st.image("assets/profile.jpg", width=80)

# ------------------------
# TODO General Info
# ------------------------
a,b,c,d = st.columns([1,1,1,1])
with a:
    with st.container(border=True,key="first_container1",height="stretch"):
        st.metric(label="Total Assets", value=millify(50000000), delta=-0.5, delta_color="inverse",width="stretch",height="stretch")

with b:
    with st.container(border=True,key="first_container2",height="stretch"):
        df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])
        st.metric(
                "Expensse", 10000, 200, chart_data=df, chart_type="area", delta_color="inverse",height="stretch"
            )
with c:
    with st.container(border=True,key="first_container3",height="stretch"):
        st.metric(label="Housing Expenses", value=millify(52000), delta=-0.5, delta_color="inverse",width="stretch",height="stretch")
    
with d:
    with st.container(border=True,key="first_container4",height="stretch"):
        st.metric(label="Income Goal Progress", value=millify(51000), delta=-0.5, delta_color="inverse",width="stretch",height="stretch")

# ------------------------
# TODO Expense Income & update info
# ------------------------
c,d = st.columns([1,1,])

with c:
    with st.container(border=True,height="stretch",key="first_container7",):
        st.write("Expense Type")
        data_df = pd.DataFrame(
            {
                "sales": [200, 550, 1000, 80],
            }
        )

        # bikin kolom baru dengan icon
        data_df["sales_with_icon"] = ["💰 " + str(v) for v in data_df["sales"]]

        st.data_editor(
            data_df,
            column_config={
                "sales": st.column_config.ProgressColumn(
                    "Expense Type",
                    help="The sales volume in USD",
                    format="$%f",
                    min_value=0,
                    max_value=1000,
                ),
                "sales_with_icon": st.column_config.TextColumn("Sales (💰)",width="small"), 
            },
            hide_index=True,
        )
        
    income_source,income=st.columns([1,1])
    with income_source:
        np.random.seed(0)
        
        with st.container(border=True,height="stretch",key="first_container5",):
            st.write("Source of income")
            df = pd.DataFrame({
                "variety": np.random.choice(["Jagung", "Padi", "Kedelai"], size=50),
                "yield": np.random.randint(20, 100, size=50),
                    
            })

            st.bar_chart(df, x="variety", y="yield", x_label="",y_label="", horizontal=False,height=300)
    with income:
        with st.container(border=True,height="stretch",key="first_container6",):
                df = pd.DataFrame(rng(0).standard_normal((20, 3)), columns=["a", "b", "c"])

                st.metric(
                            "Income", millify(10000), 200, chart_data=df, chart_type="area", delta_color="off", height="stretch"
                        )
            
    
with d:
    with st.container(height=100):
        st.progress(50, text="Beli Rumah", width="stretch")
    with st.container(key="second_container",border=True,height="stretch"):
        st.warning("Pemberitahuan **23 tagihan terlambat**. Bayar segera untuk menghindari denda keterlambatan.")
        st.write('ℹ️ Notification')
        notifications = pd.DataFrame({
            "Deadline": ["14", "20", "25"],
            "Activities": ["Routine veterinarian", "Pay credit card", "Monthly report"]
        })

        st.dataframe(
            notifications,
            hide_index=True,
            column_config={
                "Deadline": st.column_config.TextColumn("📅 Deadline", width="small"),
                "Activities": st.column_config.TextColumn("📝 Activities", width="medium"),
            },
            use_container_width=True,
        )
# ------------------------
# TODO Chart
# ------------------------
chart1,chart2,chart3 = st.columns([5,3,4])
with chart1:
    with st.container(border=True,key="first_container9",):
        st.write('Income and Expenses')
        with st.container(horizontal=True,):
            st.metric(label="Maximum Expenses",value=millify(100000),)
            st.metric(label="Maximum Income",value=millify(400000),)
        df = pd.DataFrame(
            {
                "col1": list(range(20)) * 3,
                "col2": rng(0).standard_normal(60),
                "col3": ["a"] * 20 + ["b"] * 20 + ["c"] * 20,
            }
        )

        st.line_chart(df, x="col1", y="col2", color="col3")
with chart2:
    with st.container(border=True,height="stretch", key="first_container10"):
        st.write('Assets')
        from streamlit_elements import elements, mui
        from streamlit_elements import nivo

        with elements("nivo_pie_chart"):

            DATA = [
                {"id": "css", "label": "css", "value": 58, "color": "hsl(309, 70%, 50%)"},
                {"id": "php", "label": "php", "value": 582, "color": "hsl(229, 70%, 50%)"},
                {"id": "ruby", "label": "ruby", "value": 491, "color": "hsl(78, 70%, 50%)"},
                {"id": "scala", "label": "scala", "value": 254, "color": "hsl(278, 70%, 50%)"},
                {"id": "stylus", "label": "stylus", "value": 598, "color": "hsl(273, 70%, 50%)"},
            ]

            # Atur ukuran container chart (400px tinggi, full lebar)
            with mui.Box(sx={"height": 400, "width": "100%"}):
                nivo.Pie(
                    data=DATA,
                    innerRadius={0.5},
                    padAngle={0.6},
                    cornerRadius={2},
                    activeOuterRadiusOffset={8},
                    enableArcLinkLabels=False,
                    legends=[
                    {
                        "anchor": "bottom",
                        "direction": "column",
                        "justify": False,
                        "translateX": 0,
                        "translateY": 0,
                        "itemsSpacing": 0,
                        "itemWidth": 100,
                        "itemHeight": 20,
                        "itemTextColor": "#999",
                        "itemDirection": "left-to-right",
                        "itemOpacity": 1,
                        "symbolSize": 18,
                        "symbolShape": "circle",
                        "effects": [
                            {"on": "hover", "style": {"itemTextColor": "#000"}}
                        ],
                    }],
                    theme={
                        "tooltip": {
                            "container": {
                                "color": "#999"
                            }
                        }
                    },
                )



with chart3:
    with st.container(border=True,height="stretch",key="first_container11",):
        st.write('Assets')
        
        df = pd.DataFrame(
            {
                "col1": list(range(20)) * 3,
                "col2": rng(0).standard_normal(60),
                "col3": ["a"] * 20 + ["b"] * 20 + ["c"] * 20,
            }
        )

        st.line_chart(df, x="col1", y="col2", color="col3")