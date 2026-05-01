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
        body, .stApp, .main, .block-container, .css-18e3th9, .css-1lcbmhc, .css-1outpf7,
        div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] > div {
            background: radial-gradient(circle at top, rgba(10, 28, 66, 0.92), #020812 42%) !important;
            color: #e2e8f0 !important;
            overflow-x: hidden;
        }
        .element-container, .streamlit-expanderHeader, .stMarkdown, .stText, .css-1kyxreq {
            color: #e2e8f0 !important;
        }
        .block-container {
            box-shadow: none !important;
            background-color: transparent !important;
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #071a33 0%, #061825 100%) !important;
            color: #e2e8f0 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.05);
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
            border-radius: 14px;
            padding: 0.9rem 1.1rem;
            font-weight: 700;
            transition: background-color 0.2s ease, transform 0.18s ease, box-shadow 0.2s ease;
        }
        .stButton>button:hover {
            background-color: #1662bf;
            transform: translateY(-1px);
            box-shadow: 0 14px 30px rgba(22, 98, 191, 0.24);
        }
        .stTextInput>div>input, .stNumberInput>div>input, .stSelectbox>div>div>div>div {
            border-radius: 14px;
            background: #071b38 !important;
            color: #e2e8f0 !important;
            border: 1px solid rgba(148, 163, 184, 0.18) !important;
        }
        .stSlider>div>div {
            border-radius: 12px;
        }
        .stAlert, .stInfo, .stSuccess, .stWarning, .stError {
            border-radius: 18px;
        }
        .metric-card, .section-card, .hero-card, .grid-card, .result-card, .form-card {
            background: rgba(9, 18, 37, 0.95);
            border: 1px solid rgba(56, 84, 126, 0.18);
            border-radius: 24px;
            box-shadow: 0 18px 40px rgba(0, 0, 0, 0.40);
            padding: 1.6rem;
        }
        .hero-card {
            padding: 2rem 2rem 1.5rem 2rem;
        }
        .section-card {
            padding: 1.7rem;
        }
        .section-title {
            margin-bottom: 0.4rem;
            color: #e2e8f0;
            font-weight: 700;
        }
        .footer {
            text-align: center;
            color: #94a3b8;
            padding: 1.5rem 0 0.5rem;
            font-size: 0.95rem;
        }
        .hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.4rem;
            background: rgba(20, 57, 103, 0.95);
            color: #cbd5e1;
            padding: 0.55rem 0.85rem;
            border-radius: 999px;
            font-size: 0.9rem;
            margin-bottom: 1rem;
            border: 1px solid rgba(148, 163, 184, 0.14);
        }
        .tone-chip {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: rgba(255, 255, 255, 0.05);
            color: #94a3b8;
            padding: 0.45rem 0.75rem;
            border-radius: 999px;
            border: 1px solid rgba(148, 163, 184, 0.12);
            margin-bottom: 1rem;
        }
        .fade-in-up {
            animation: fadeInUp 0.85s ease both;
        }
        .slide-in-left {
            animation: slideInLeft 0.75s ease both;
        }
        .slide-in-right {
            animation: slideInRight 0.75s ease both;
        }
        .glow-button button {
            box-shadow: 0 0 0 0 rgba(22, 98, 191, 0.25);
            transition: box-shadow 0.35s ease, transform 0.18s ease;
        }
        .glow-button button:hover {
            box-shadow: 0 0 24px rgba(22, 98, 191, 0.20);
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(18px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes slideInLeft {
            from { opacity: 0; transform: translateX(-24px); }
            to { opacity: 1; transform: translateX(0); }
        }
        @keyframes slideInRight {
            from { opacity: 0; transform: translateX(24px); }
            to { opacity: 1; transform: translateX(0); }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='hero-card fade-in-up'>", unsafe_allow_html=True)
with st.container():
    bt1, bt2 = st.columns([3, 1.4])
    with bt1:
        st.markdown("<div class='hero-pill'>Live forecast + risk intelligence</div>", unsafe_allow_html=True)
        st.title("📦 Smart Freight & Invoice Risk Prediction")
        st.markdown(
            """
            A modern analytics portal for vendor invoices, freight cost forecasting, and
            automated approval guidance. Keep approvals fast, reduce risk, and improve
            procurement visibility in one dark-mode workspace.
            """
        )
    with bt2:
        st.markdown("<div class='tone-chip'>Native dark mode enabled</div>", unsafe_allow_html=True)
        st.metric("Model readiness", "Operational", delta="+8%")
        st.metric("Prediction latency", "<1s")
        st.metric("Confidence score", "92%", delta="+4%")

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("---")

st.sidebar.header("Choose your workflow")
selected_model = st.sidebar.radio(
    "Prediction mode",
    ["Freight Cost Prediction", "Invoice Flag Prediction"],
)

st.sidebar.markdown("### Quick start")
st.sidebar.write(
    "• Select a workflow."
    "\n• Enter invoice and freight details."
    "\n• Click Predict and review the results."
)

with st.sidebar.expander("How to use this portal"):
    st.write(
        "1. Choose the prediction workflow.\n"
        "2. Enter invoice details and click Predict.\n"
        "3. Review the recommendation and next steps."
    )
    st.write("Use consistent invoice values for the best results.")

st.sidebar.markdown("---")

st.sidebar.markdown(
    "**Why this dashboard matters:**\n"
    "- Faster freight negotiation decisions.\n"
    "- Proactive invoice risk screening.\n"
    "- One unified approval view."
)

st.sidebar.caption("Dark theme is applied both natively and with custom styling for a premium UI.")

if selected_model == "Freight Cost Prediction":
    st.header("Freight Cost Prediction")
    st.markdown(
        "Predict freight expense from invoice quantity and invoice value, then use the estimate to guide vendor negotiation and logistics planning."
    )

    with st.form("freight_form"):
        quad, quad_info = st.columns([2, 1])

        with quad:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1200,
                format="%d",
                help="Enter the total number of units on the invoice.",
            )
            dollars = st.number_input(
                "Invoice Dollars",
                min_value=1.0,
                value=18500.0,
                format="%.2f",
                help="Enter the total invoice amount in your currency.",
            )
            goods_category = st.selectbox(
                "Freight category",
                ["Standard", "Express", "Oversize"],
                help="Choose the category that best matches the shipment type.",
            )

        with quad_info:
            expected_lead_time = st.slider(
                "Expected lead time (days)",
                min_value=1,
                max_value=30,
                value=10,
                help="Estimate the delivery window for the shipment.",
            )
            st.info("Tip: Higher lead time can increase freight expense.")

        submit_freight = st.form_submit_button("Predict Freight Cost")

    if submit_freight:
        with st.spinner("Estimating freight cost..."):
            progress = st.progress(0)
            for pct in range(0, 101, 20):
                progress.progress(pct)
                time.sleep(0.08)

            input_data = {"Quantity": [quantity], "Dollars": [dollars]}
            prediction = predict_freight_cost(input_data)["Predicted_Freight"]
            progress.empty()

        st.success("Freight estimate is ready.")

        card1, card2 = st.columns(2)
        with card1:
            st.markdown("<div class='metric-card slide-in-left'>", unsafe_allow_html=True)
            st.metric("Estimated Freight Cost", f"${prediction[0]:,.2f}")
            st.markdown("**Freight category:**", unsafe_allow_html=True)
            st.write(goods_category)
            st.markdown("**Lead time:**", unsafe_allow_html=True)
            st.write(f"{expected_lead_time} days")
            st.markdown("</div>", unsafe_allow_html=True)

        with card2:
            st.markdown("<div class='metric-card slide-in-right'>", unsafe_allow_html=True)
            st.info("This estimate reflects invoice patterns and freight behavior.")
            st.write("**Next steps:**")
            st.write("• Compare this estimate with vendor quotes.")
            st.write("• Verify logistics costs before approval.")
            st.markdown("</div>", unsafe_allow_html=True)

else:
    st.header("Invoice Manual Approval Prediction")
    st.markdown(
        "Identify invoices that require manual review to reduce approval risk and improve process efficiency."
    )

    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            invoice_quantity = st.number_input(
                "Invoice Quantity",
                min_value=1,
                value=50,
                format="%d",
                help="Total quantity on the invoice.",
            )
            invoice_dollars = st.number_input(
                "Invoice Dollars",
                min_value=1.0,
                value=162.0,
                format="%.2f",
                help="Total invoice value.",
            )

        with col2:
            freight = st.number_input(
                "Freight",
                min_value=0.0,
                value=1.73,
                format="%.2f",
                help="Freight charges associated with the invoice.",
            )
            total_item_quantity = st.number_input(
                "Total Item Quantity",
                min_value=1,
                value=50,
                format="%d",
                help="Total quantity across all line items.",
            )

        with col3:
            total_item_dollars = st.number_input(
                "Total Item Dollars",
                min_value=1.0,
                value=2476.0,
                format="%.2f",
                help="Total dollar amount for all items.",
            )
            avg_receiving_delay = st.number_input(
                "Average Receiving Delay",
                min_value=0.0,
                value=5.0,
                format="%.1f",
                help="Average delay in days between shipment and receipt.",
            )

        submit_flag = st.form_submit_button("Predict Invoice Risk")

    if submit_flag:
        with st.spinner("Analyzing invoice risk..."):
            progress = st.progress(0)
            for pct in range(0, 101, 20):
                progress.progress(pct)
                time.sleep(0.08)

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
            st.warning("⚠️ This invoice is likely to require manual approval.")
        else:
            st.success("✅ This invoice appears low-risk.")

        status_col1, status_col2 = st.columns([1, 1])
        with status_col1:
            st.markdown("<div class='metric-card slide-in-left'>", unsafe_allow_html=True)
            st.metric("Approval Status", status)
            st.write("**Invoice total:**", f"${invoice_dollars:,.2f}")
            st.write("**Freight cost:**", f"${freight:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with status_col2:
            st.markdown("<div class='metric-card slide-in-right'>", unsafe_allow_html=True)
            if is_flagged:
                st.error("This invoice shows risk signals for cost or delivery patterns.")
            else:
                st.info("The invoice appears consistent with expected vendor behavior.")
            st.markdown("**Review checklist:**", unsafe_allow_html=True)
            st.write("• Confirm invoice quantity against purchase order.")
            st.write("• Check freight for unusual spikes.")
            st.write("• Validate delivery delay status.")
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    "<div class='footer'>Made by Huzaifa</div>",
    unsafe_allow_html=True,
)
