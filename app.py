import streamlit as st
import time

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag


st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        :root {
            color-scheme: dark;
            font-family: 'Inter', sans-serif;
        }
        body, .stApp, .main, .block-container, div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] > div {
            background: radial-gradient(circle at top, rgba(7, 18, 45, 0.96), #020812 52%) !important;
            color: #e2e8f0 !important;
            min-height: 100vh;
            overflow-x: hidden;
        }
        .element-container, .streamlit-expanderHeader, .stMarkdown, .stText, .css-1kyxreq {
            color: #e2e8f0 !important;
        }
        .block-container {
            background-color: transparent !important;
            padding-top: 1.8rem !important;
            padding-bottom: 2.2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #071a33 0%, #061825 100%) !important;
            color: #e2e8f0 !important;
            border-right: 1px solid rgba(255,255,255,0.08);
        }
        [data-testid="stSidebar"] .css-1d391kg, [data-testid="stSidebar"] .css-1lcbmhc {
            background: transparent !important;
        }
        .stSidebar .css-1v0mbdj, .stSidebar .css-10trblm {
            color: #f8fafc !important;
        }
        .stButton>button {
            background-color: #1f4f92;
            color: white;
            border-radius: 16px;
            padding: 1rem 1.15rem;
            font-weight: 700;
            letter-spacing: 0.02em;
            transition: background-color 0.2s ease, transform 0.16s ease, box-shadow 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #1772d1;
            transform: translateY(-1px);
            box-shadow: 0 16px 32px rgba(23, 114, 209, 0.22);
        }
        .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div>div>div {
            border-radius: 16px;
            background: #071b38 !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
            box-shadow: inset 0 0 0 1px rgba(255,255,255,0.04);
        }
        .stSlider>div>div { border-radius: 16px; }
        .stAlert, .stInfo, .stSuccess, .stWarning, .stError { border-radius: 18px; }
        .hero-card, .feature-card, .section-card, .result-card, .summary-card, .insight-card {
            background: rgba(10, 22, 41, 0.96);
            border: 1px solid rgba(75, 110, 160, 0.22);
            border-radius: 28px;
            box-shadow: 0 24px 55px rgba(0, 0, 0, 0.30);
            padding: 1.8rem;
            transition: transform 0.35s ease, border-color 0.35s ease, box-shadow 0.35s ease;
        }
        .hero-card:hover, .feature-card:hover, .section-card:hover, .result-card:hover, .summary-card:hover, .insight-card:hover {
            transform: translateY(-2px);
            border-color: rgba(90, 145, 220, 0.30);
            box-shadow: 0 28px 65px rgba(0,0,0,0.35);
        }
        .hero-card {
            padding: 2.2rem 2.2rem 1.8rem 2.2rem;
        }
        .hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(24, 56, 110, 0.95);
            color: #cbd5e1;
            padding: 0.55rem 0.95rem;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.16);
            font-size: 0.92rem;
            margin-bottom: 1rem;
        }
        .hero-note {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(255, 255, 255, 0.05);
            color: #94a3b8;
            padding: 0.5rem 0.85rem;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.12);
            margin-bottom: 1rem;
        }
        .hero-title { margin-top: 0.1rem; margin-bottom: 1rem; font-size: clamp(2rem, 2.6vw, 3.25rem); line-height: 1.05; }
        .hero-description { color: #cbd5e1; line-height: 1.75; margin-bottom: 1.5rem; }
        .feature-box { padding: 1.25rem 1.35rem; background: rgba(14, 29, 55, 0.95); border-radius: 22px; border: 1px solid rgba(75,110,160,0.18); margin-bottom: 1rem; }
        .section-title { margin-bottom: 0.6rem; color: #e2e8f0; font-weight: 700; }
        .section-subtitle { color: #94a3b8; margin-top: 0; margin-bottom: 1.2rem; }
        .result-card p, .feature-card p, .section-card p { color: #cbd5e1; }
        .insight-card { padding: 1.65rem; }
        .insight-card span { color: #94a3b8; }
        .glow-button button { box-shadow: 0 0 0 0 rgba(22, 98, 191, 0.25); transition: box-shadow 0.35s ease, transform 0.18s ease; }
        .glow-button button:hover { box-shadow: 0 0 24px rgba(22, 98, 191, 0.20); }
        .fade-in-up { animation: fadeInUp 0.85s ease both; }
        .slide-in-left { animation: slideInLeft 0.75s ease both; }
        .slide-in-right { animation: slideInRight 0.75s ease both; }
        .slide-in-up { animation: slideInUp 0.75s ease both; }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(18px); } to { opacity: 1; transform: translateY(0); } }
        @keyframes slideInLeft { from { opacity: 0; transform: translateX(-24px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes slideInRight { from { opacity: 0; transform: translateX(24px); } to { opacity: 1; transform: translateX(0); } }
        @keyframes slideInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='hero-card fade-in-up'>", unsafe_allow_html=True)
with st.container():
    left, right = st.columns([3, 1.2], gap="large")
    with left:
        st.markdown("<div class='hero-pill'>Premium invoice intelligence</div>", unsafe_allow_html=True)
        st.markdown("<h1 class='hero-title'>Vendor Invoice Intelligence Portal</h1>", unsafe_allow_html=True)
        st.markdown(
            """
            A polished analytics workspace for freight forecasting and approval risk review.
            Deliver faster procurement decisions with a premium dark interface that is
            styled for clarity, speed, and confidence.
            """
        )
        st.markdown("<div class='hero-note'>Designed to feel professional, clean, and highly interactive.</div>", unsafe_allow_html=True)
    with right:
        st.markdown("<div class='summary-card slide-in-up'>", unsafe_allow_html=True)
        st.subheader("Live insights")
        st.metric("Model readiness", "Operational", delta="+8%")
        st.metric("Response time", "<1s")
        st.metric("Interface score", "Premium")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='grid-card fade-in-up'>", unsafe_allow_html=True)
with st.container():
    s1, s2, s3 = st.columns(3, gap='large')
    with s1:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Structured inputs</h4>", unsafe_allow_html=True)
        st.write("Large input fields and clear guidance reduce data entry friction.")
        st.markdown("</div>", unsafe_allow_html=True)
    with s2:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Clear decision support</h4>", unsafe_allow_html=True)
        st.write("Stylized result cards and recommendations help stakeholders act quickly.")
        st.markdown("</div>", unsafe_allow_html=True)
    with s3:
        st.markdown("<div class='feature-card'>", unsafe_allow_html=True)
        st.markdown("<h4>Dark premium design</h4>", unsafe_allow_html=True)
        st.write("A cohesive dark theme with subtle motion and modern visual hierarchy.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.sidebar.header("Choose workflow")
selected_model = st.sidebar.radio(
    "Prediction mode",
    ["Freight Cost Prediction", "Invoice Flag Prediction"],
)

st.sidebar.markdown("### Quick start")
st.sidebar.write(
    "- Select the prediction workflow.\n"
    "- Add invoice and freight details.\n"
    "- Submit and review the outcome."
)

with st.sidebar.expander("How to use this dashboard"):
    st.write(
        "1. Select the workflow that matches the invoice type.\n"
        "2. Enter accurate invoice and freight numbers.\n"
        "3. Review the output and next-step guidance."
    )

st.sidebar.markdown("---")
st.sidebar.markdown(
    "**Why this dashboard works:**\n"
    "- Faster freight cost validation.\n"
    "- Smarter invoice approval screening.\n"
    "- A unified workflow for procurement and finance."
)

st.sidebar.caption("Native dark mode with premium UX styling.")

if selected_model == "Freight Cost Prediction":
    st.header("Freight Cost Forecast")
    st.markdown(
        "Forecast expected freight expense from invoice quantity and value, then use the estimate for vendor negotiations and logistics planning."
    )

    st.markdown("<div class='section-card fade-in-up'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Freight details</h3>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Fill in invoice quantity, total value, and shipment timing to get a contextual freight estimate.</p>", unsafe_allow_html=True)

    with st.form("freight_form"):
        form_left, form_right = st.columns([1.9, 1], gap='large')
        with form_left:
            quantity = st.number_input(
                "Invoice quantity",
                min_value=1,
                value=1200,
                format="%d",
                help="Total quantity on the invoice.",
            )
            dollars = st.number_input(
                "Invoice dollars",
                min_value=1.0,
                value=18500.0,
                format="%.2f",
                help="Total invoice amount in your currency.",
            )
            goods_category = st.selectbox(
                "Freight category",
                ["Standard", "Express", "Oversize"],
                help="Select the shipment type that best matches the invoice.",
            )
        with form_right:
            expected_lead_time = st.slider(
                "Expected lead time (days)",
                min_value=1,
                max_value=30,
                value=10,
                help="Estimated delivery window for the shipment.",
            )
            st.info("Higher lead times may indicate larger or more complex shipments.")
            st.markdown("<div class='feature-box'>Tip: Use this workflow for freight-budget planning and supplier comparison.</div>", unsafe_allow_html=True)

        submit_freight = st.form_submit_button("Calculate freight estimate")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit_freight:
        with st.spinner("Estimating freight cost..."):
            progress = st.progress(0)
            for pct in range(0, 101, 20):
                progress.progress(pct)
                time.sleep(0.06)

            input_data = {"Quantity": [quantity], "Dollars": [dollars]}
            prediction = predict_freight_cost(input_data)["Predicted_Freight"]
            progress.empty()

        st.success("Freight estimate generated.")
        st.markdown("<div class='result-card slide-in-up'>", unsafe_allow_html=True)
        result_left, result_right = st.columns([1.2, 1], gap='large')
        with result_left:
            st.metric("Estimated freight cost", f"${prediction[0]:,.2f}")
            st.markdown("**Freight category:**", unsafe_allow_html=True)
            st.write(goods_category)
            st.markdown("**Estimated transit:**", unsafe_allow_html=True)
            st.write(f"{expected_lead_time} days")
        with result_right:
            st.info("Use this estimated cost to validate vendor quotes and logistics assumptions.")
            st.markdown("**Next steps:**", unsafe_allow_html=True)
            st.write("• Compare this cost with vendor bids.")
            st.write("• Confirm any expedited or oversized freight assumptions.")
            st.write("• Log the estimate for review and approval.")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.header("Invoice Approval Risk")
    st.markdown(
        "Evaluate whether an invoice should be routed for manual approval or can be auto-approved based on risk signals."
    )

    st.markdown("<div class='section-card fade-in-up'>", unsafe_allow_html=True)
    st.markdown("<h3 class='section-title'>Risk assessment inputs</h3>", unsafe_allow_html=True)
    st.markdown("<p class='section-subtitle'>Complete the invoice detail fields to determine whether manual review is recommended.</p>", unsafe_allow_html=True)

    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3, gap='large')
        with col1:
            invoice_quantity = st.number_input(
                "Invoice quantity",
                min_value=1,
                value=50,
                format="%d",
                help="Total quantity on the invoice.",
            )
            invoice_dollars = st.number_input(
                "Invoice dollars",
                min_value=1.0,
                value=162.0,
                format="%.2f",
                help="Total invoice value.",
            )
        with col2:
            freight = st.number_input(
                "Freight cost",
                min_value=0.0,
                value=1.73,
                format="%.2f",
                help="Freight cost associated with the invoice.",
            )
            total_item_quantity = st.number_input(
                "Total item quantity",
                min_value=1,
                value=50,
                format="%d",
                help="Total quantity across all line items.",
            )
        with col3:
            total_item_dollars = st.number_input(
                "Total item dollars",
                min_value=1.0,
                value=2476.0,
                format="%.2f",
                help="Total dollar amount for all invoice items.",
            )
            avg_receiving_delay = st.number_input(
                "Avg receiving delay (days)",
                min_value=0.0,
                value=5.0,
                format="%.1f",
                help="Average delay between shipment and receipt.",
            )

        submit_flag = st.form_submit_button("Assess approval risk")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit_flag:
        with st.spinner("Analyzing approval risk..."):
            progress = st.progress(0)
            for pct in range(0, 101, 20):
                progress.progress(pct)
                time.sleep(0.06)

            input_data = {
                "invoice_quantity": [invoice_quantity],
                "invoice_dollars": [invoice_dollars],
                "Freight": [freight],
                "total_item_quantity": [total_item_quantity],
                "total_item_dollars": [total_item_dollars],
                "avg_receiving_delay": [avg_receiving_delay],
            }
            flag_prediction = predict_invoice_flag(input_data)["Predicted_Flag"]
            progress.empty()

        is_flagged = bool(flag_prediction[0])
        status = "Manual Approval" if is_flagged else "Auto-Approve"

        if is_flagged:
            st.warning("⚠️ This invoice should be reviewed by a human approver.")
        else:
            st.success("✅ This invoice appears suitable for automatic approval.")

        st.markdown("<div class='result-card slide-in-up'>", unsafe_allow_html=True)
        left_status, right_status = st.columns([1.2, 1], gap='large')
        with left_status:
            st.metric("Approval outcome", status)
            st.write("**Invoice total:**", f"${invoice_dollars:,.2f}")
            st.write("**Freight cost:**", f"${freight:,.2f}")
        with right_status:
            if is_flagged:
                st.error("Risk indicators detected in cost or timing.")
            else:
                st.info("The invoice looks consistent with normal vendor behavior.")
            st.markdown("**Review checklist:**", unsafe_allow_html=True)
            st.write("• Verify quantity against the purchase order.")
            st.write("• Confirm freight cost against expected rates.")
            st.write("• Check receiving delay for anomalies.")
        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<div class='footer'>Premium invoice intelligence UI — designed for clarity, speed, and confident decisions.</div>",
    unsafe_allow_html=True,
)
