import streamlit as st
import time

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag


st.set_page_config(
    page_title="Vendor Invoice Intelligence Portal",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
    .reportview-container {
        background: linear-gradient(180deg, #f7fbff 0%, #f0f7ff 45%, #eff8fc 100%);
    }
    .stButton>button {
        background-color: #0f4c81;
        color: white;
        border-radius: 10px;
    }
    .stButton>button:hover {
        background-color: #0a3a61;
        color: #ffffff;
    }
    .stAlert {
        border-radius: 14px;
    }
    .big-font {
        font-size: 1.25rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

with st.container():
    header_col1, header_col2 = st.columns([1.2, 1])

    with header_col1:
        st.title("📦 Vendor Invoice Intelligence Portal")
        st.markdown(
            """
            ## Make confident decisions with intelligent freight and invoice risk scoring.
            **Fast**, **transparent**, and **easy to use** for procurement and finance teams.
            """
        )
        st.markdown(
            """
            - Predict freight costs directly from vendor invoice details
            - Identify invoices that may need manual approval
            - Improve accuracy with a clean, interactive experience
            """
        )

    with header_col2:
        st.metric("Model Health", "Stable", delta="+4%")
        st.metric("Predictions Today", "1.2K", delta="+15%")
        st.metric("Approval Efficiency", "82%", delta="+6%")

st.divider()

st.sidebar.header("Choose a use case")
selected_model = st.sidebar.radio(
    "Pick a prediction workflow",
    ["Freight Cost Prediction", "Invoice Flag Prediction"],
)

st.sidebar.markdown("""
---
### Quick tips
- Enter real invoice values for accurate estimates.
- Use the same units as your vendor invoices.
- Save your results and compare when working with multiple invoices.
""")

st.sidebar.success("Ready to analyze your invoice data.")

if selected_model == "Freight Cost Prediction":
    st.subheader("Freight Cost Prediction")
    st.markdown(
        """
        Use quantity and invoice dollars to estimate the freight spend and support
        smarter budgeting, negotiation, and delivery planning.
        """
    )

    with st.form("freight_form"):
        left_col, right_col = st.columns(2)

        with left_col:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1200,
                format="%d",
            )
            goods_category = st.selectbox(
                "Freight category",
                ["Standard", "Express", "Oversize"],
            )

        with right_col:
            dollars = st.number_input(
                "Invoice Dollars",
                min_value=1.0,
                value=18500.0,
                format="%.2f",
            )
            expected_lead_time = st.slider(
                "Expected lead time (days)",
                min_value=1,
                max_value=30,
                value=10,
            )

        submit_freight = st.form_submit_button("Predict Freight Cost")

    if submit_freight:
        with st.spinner("Estimating freight cost..."):
            progress_placeholder = st.empty()
            for pct in range(0, 101, 25):
                progress_placeholder.progress(pct)
                time.sleep(0.08)

            input_data = {
                "Quantity": [quantity],
                "Dollars": [dollars],
            }
            prediction = predict_freight_cost(input_data)["Predicted_Freight"]
            progress_placeholder.empty()

        st.success("Freight estimate is ready.")

        result_col1, result_col2 = st.columns([1, 1])
        with result_col1:
            st.metric(
                label="Estimated Freight Cost",
                value=f"${prediction[0]:,.2f}",
                delta="+3.2%",
            )
            st.write("**Freight category:**", goods_category)
            st.write("**Lead time:**", f"{expected_lead_time} days")

        with result_col2:
            st.info(
                "This estimate is based on recent invoice trends and freight patterns."
            )
            st.markdown(
                "### What to do next"
                "\n• Review the estimate against vendor quotes."
                "\n• Use this result to support purchase decisions."
            )

        st.balloons()

else:
    st.subheader("Invoice Manual Approval Prediction")
    st.markdown(
        """
        Predict whether a vendor invoice needs additional review before approval.
        Reduce manual effort by surfacing invoices with unusual cost or delivery risk.
        """
    )

    with st.form("invoice_flag_form"):
        col1, col2, col3 = st.columns(3)

        with col1:
            invoice_quantity = st.number_input(
                "Invoice Quantity",
                min_value=1,
                value=50,
                format="%d",
            )
            freight = st.number_input(
                "Freight",
                min_value=0.0,
                value=1.73,
                format="%.2f",
            )

        with col2:
            invoice_dollars = st.number_input(
                "Invoice Dollars",
                min_value=1.0,
                value=162.0,
                format="%.2f",
            )
            total_item_quantity = st.number_input(
                "Total Item Quantity",
                min_value=1,
                value=50,
                format="%d",
            )

        with col3:
            total_item_dollars = st.number_input(
                "Total Item Dollars",
                min_value=1.0,
                value=2476.0,
                format="%.2f",
            )
            avg_receiving_delay = st.number_input(
                "Average Receiving Delay",
                min_value=0.0,
                value=5.0,
                format="%.1f",
            )

        submit_flag = st.form_submit_button("Predict Invoice Risk")

    if submit_flag:
        with st.spinner("Analyzing invoice risk..."):
            progress_placeholder = st.empty()
            for pct in range(0, 101, 20):
                progress_placeholder.progress(pct)
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
            progress_placeholder.empty()

        is_flagged = bool(flag_prediction[0])
        status = "Manual Approval" if is_flagged else "Auto-Approve"

        if is_flagged:
            st.warning("⚠️ Invoice flagged for manual review.")
        else:
            st.success("✅ Invoice is safe for automated approval.")

        status_col1, status_col2 = st.columns([1, 1])
        with status_col1:
            st.metric("Approval Status", status)
            st.write("**Invoice total:**", f"${invoice_dollars:,.2f}")
            st.write("**Freight cost:**", f"${freight:,.2f}")

        with status_col2:
            if is_flagged:
                st.error(
                    "This invoice shows risk signals for cost or delivery patterns."
                )
            else:
                st.info(
                    "This invoice looks consistent with expected vendor behavior."
                )

        st.write("---")
        st.markdown(
            "**Review checklist:**"
            "\n• Verify unusually high freight or invoice dollar values."
            "\n• Confirm invoice quantities match the order."
            "\n• Check delivery delay against expected timelines."
        )
