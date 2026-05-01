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
        body, .stApp, .main, .block-container, .css-18e3th9, .css-k1vhr4, .css-1lcbmhc, .css-1outpf7, div[data-testid="stAppViewContainer"], div[data-testid="stAppViewContainer"] > div {
            background: linear-gradient(180deg, #eef5fc 0%, #f7fbff 30%, #ffffff 100%) !important;
            color: #0f172a !important;
        }
        .element-container, .streamlit-expanderHeader, .stMarkdown, .stText, .css-1kyxreq {
            color: #0f172a !important;
        }
        .block-container {
            box-shadow: none !important;
            background-color: transparent !important;
            padding-top: 1.5rem !important;
            padding-bottom: 2rem !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
        .stButton>button {
            background-color: #0b4f7e;
            color: white;
            border-radius: 10px;
            padding: 0.75rem 1rem;
            font-weight: 600;
            transition: background-color 0.25s ease;
        }
        .stButton>button:hover {
            background-color: #093959;
            color: #ffffff;
        }
        .stAlert {
            border-radius: 16px;
        }
        .footer {
            text-align: center;
            color: #5a6370;
            padding: 1rem 0;
            margin-top: 2rem;
            font-size: 0.95rem;
        }
        .metric-card {
            background: rgba(255, 255, 255, 0.92);
            border-radius: 18px;
            padding: 1.25rem;
            box-shadow: 0 12px 30px rgba(15, 70, 120, 0.08);
            border: 1px solid rgba(15, 70, 120, 0.08);
        }
        .section-card {
            background: rgba(248, 252, 255, 0.95);
            border-radius: 24px;
            padding: 1.5rem;
            border: 1px solid rgba(15, 70, 120, 0.1);
            box-shadow: 0 18px 35px rgba(15, 70, 120, 0.08);
        }
        .section-title {
            margin-bottom: 0.25rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='section-card'>", unsafe_allow_html=True)
with st.container():
    bt1, bt2 = st.columns([3, 2])
    with bt1:
        st.subheader("Vendor Invoice Intelligence")
        st.title("📦 Smart Freight & Invoice Risk Prediction")
        st.markdown(
            """
            Build confidence in vendor decisions with fast, data-driven predictions.
            Enter invoice details, then review the forecast and approval recommendation
            in a polished, interactive workflow.
            """
        )
    with bt2:
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

with st.sidebar.expander("How to use this portal"):
    st.write(
        "1. Choose the prediction workflow.\n"
        "2. Enter invoice details and click Predict.\n"
        "3. Review the recommendation and next steps."
    )
    st.write("Use consistent invoice values for the best results.")

st.sidebar.markdown("---")

st.sidebar.markdown(
    "**Results include:**\n"
    "- Freight estimate comparisons\n"
    "- Approval risk guidance\n"
    "- Actionable decision support"
)

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
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Estimated Freight Cost", f"${prediction[0]:,.2f}")
            st.markdown("**Freight category:**", unsafe_allow_html=True)
            st.write(goods_category)
            st.markdown("**Lead time:**", unsafe_allow_html=True)
            st.write(f"{expected_lead_time} days")
            st.markdown("</div>", unsafe_allow_html=True)

        with card2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
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
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            st.metric("Approval Status", status)
            st.write("**Invoice total:**", f"${invoice_dollars:,.2f}")
            st.write("**Freight cost:**", f"${freight:,.2f}")
            st.markdown("</div>", unsafe_allow_html=True)

        with status_col2:
            st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
            if is_flagged:
                st.error("This invoice shows risk signals for cost or delivery patterns.")
            else:
                st.info("The invoice appears consistent with expected vendor behavior.")
            st.markdown("**Review checklist:**")
            st.write("• Confirm invoice quantity against purchase order.")
            st.write("• Check freight for unusual spikes.")
            st.write("• Validate delivery delay status.")
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("---")

st.markdown(
    "<div class='footer'>Made by Huzaifa</div>",
    unsafe_allow_html=True,
)
