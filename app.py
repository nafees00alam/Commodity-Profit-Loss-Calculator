
import streamlit as st

st.set_page_config(page_title="Profit / Loss Calculator", page_icon="💹", layout="wide")

# ---------- Global styles ----------
st.markdown(
    """
    <style>
      .block-container {padding-top: 1.5rem; padding-bottom: 2rem; max-width: 1400px;}
      .titlebar {border:1px solid #333; padding:12px; border-radius:12px; background:#1f1f1f; text-align:center; margin-bottom: 16px;}
      .big {font-size: 24px; font-weight: 700; color: #ff4d4f;}

      .section {border:1px solid #333; border-radius:12px; background:#1b1b1b; margin-bottom:16px;}
      .section-inner {padding: 16px 16px 18px 16px;}
      .section-header {display:flex; align-items:center; justify-content:space-between;
                       padding:10px 14px; border-bottom:1px solid #333; border-top-left-radius:12px; border-top-right-radius:12px;
                       background:#191919;}
      .header-title {font-size:16px; font-weight:700; color:#ff4d4f;}
      .gap {height: 6px;}

      .card-center {display:flex; align-items:center; justify-content:center; min-height: 190px;}

      /* tighten default widget spacing inside section */
      .stNumberInput, .stRadio, .stText {margin-top: 2px; margin-bottom: 2px;}
      .st-emotion-cache-1dp5vir {padding-bottom: 0 !important;} /* reduce extra padding below radios */
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="titlebar"><span class="big">PROFIT LOSS CALCULATOR</span></div>', unsafe_allow_html=True)

# ---------- Helpers ----------
def fmt(x): return f"{x:,.2f}"

# ---------- Top row ----------
col_inputs, col_commission, col_right = st.columns([1.05, 1.0, 1.35])

with col_inputs:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="header-title">INPUTS</div></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="section-inner">', unsafe_allow_html=True)
        packet_weight = st.number_input("Packet weight (kg)", value=15.0, min_value=0.0, step=0.1)
        num_packets   = st.number_input("Number of packets", value=100, min_value=0, step=1)
        rent_per_packet = st.number_input("Rent per packet", value=35.0, min_value=0.0, step=0.5)
        freight_per_kg  = st.number_input("Freight per kg", value=2.5, min_value=0.0, step=0.1)
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_commission:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="header-title">COMMISSION TO MIDDLEMAN</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-inner">', unsafe_allow_html=True)
    commission_mode = st.radio("Commission mode", ["% of gross revenue", "Flat per packet", "Flat per kg (total weight)"], index=0)
    colc1, colc2 = st.columns(2)
    with colc1:
        commission_pct = st.number_input("Percentage (%)", value=0.0, min_value=0.0, step=0.25)
        commission_pp  = st.number_input("Flat per packet", value=0.0, min_value=0.0, step=0.5)
        commission_kg  = st.number_input("Flat per kg", value=0.0, min_value=0.0, step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    # Header with embedded radio on the right
    st.markdown('<div class="section-header">'
                '<div class="header-title">PRICE INPUT MODE</div>'
                '<div style="display:flex; align-items:center; gap:12px;"></div>'
                '</div>', unsafe_allow_html=True)
    # We simulate embedding: place radio immediately after header with minimal top padding so it looks inside the bar
    st.markdown('<div class="section-inner" style="padding-top:10px;">', unsafe_allow_html=True)
    price_mode = st.radio("Select mode", ["Buying price per kg", "Cost per packet"], index=0, horizontal=True, label_visibility="collapsed")
    colp1, colp2 = st.columns(2)
    with colp1:
        buy_price_per_kg = st.number_input("Buying price per kg", value=0.0, min_value=0.0, step=0.5, key="buykg")
        wastage_pct = st.number_input("Wastage %", value=0.0, min_value=0.0, step=0.5)
    with colp2:
        cost_per_packet_manual = st.number_input("Cost per packet", value=0.0, min_value=0.0, step=1.0, key="cpp")
        selling_price_kg = st.number_input("Selling price per kg", value=0.0, min_value=0.0, step=0.5)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ---------- Sync price fields ----------
if packet_weight > 0:
    if price_mode == "Buying price per kg":
        cost_per_packet = buy_price_per_kg * packet_weight
    else:
        cost_per_packet = cost_per_packet_manual
        buy_price_per_kg = cost_per_packet / packet_weight if packet_weight > 0 else 0.0
else:
    cost_per_packet = 0.0
    buy_price_per_kg = 0.0

# ---------- Calculations ----------
total_weight = packet_weight * num_packets
sellable_weight = total_weight * (1 - wastage_pct/100.0)
total_product_cost = cost_per_packet * num_packets
total_rent = rent_per_packet * num_packets
total_freight = total_weight * freight_per_kg

gross_revenue = sellable_weight * selling_price_kg

if commission_mode == "% of gross revenue":
    commission_amount = gross_revenue * (commission_pct/100.0)
elif commission_mode == "Flat per packet":
    commission_amount = commission_pp * num_packets
else:
    commission_amount = commission_kg * total_weight

grand_total_cost = total_product_cost + total_rent + total_freight + commission_amount
profit = gross_revenue - grand_total_cost

cost_per_kg_total = (grand_total_cost / total_weight) if total_weight > 0 else 0.0
cost_per_sellable_kg = (grand_total_cost / sellable_weight) if sellable_weight > 0 else 0.0
profit_per_sellable_kg = (profit / sellable_weight) if sellable_weight > 0 else 0.0
profit_per_packet = (profit / num_packets) if num_packets > 0 else 0.0

# ---------- Bottom row (centered with padding/gaps) ----------
col_inv, col_results, col_profit = st.columns([1.2, 1.4, 0.8])

with col_inv:
    st.markdown('<div class="section"><div class="section-header"><div class="header-title">INVESTMENT</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-inner">', unsafe_allow_html=True)
    st.write(f"**Total packets:** {num_packets:,d}")
    st.write(f"**Total weight:** {fmt(total_weight)} kg")
    st.write(f"**Cost per packet (buy × weight):** {fmt(cost_per_packet)}")
    st.write(f"**Total product cost:** {fmt(total_product_cost)}")
    st.write(f"**Total rent:** {fmt(total_rent)}")
    st.write(f"**Total freight:** {fmt(total_freight)}")
    st.write(f"**Commission:** {fmt(commission_amount)}")
    st.markdown(f"**🧮 GRAND TOTAL COST:** <span class='header-title'>{fmt(grand_total_cost)}</span>", unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

with col_results:
    st.markdown('<div class="section"><div class="section-header"><div class="header-title">RESULTS</div></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-inner">', unsafe_allow_html=True)
    st.write(f"**Sellable weight (kg):** {fmt(sellable_weight)}")
    st.write(f"**Gross revenue:** {fmt(gross_revenue)}")
    st.write(f"**Commission amount:** {fmt(commission_amount)}")
    st.write(f"**Cost per kg (on total weight):** {fmt(cost_per_kg_total)}")
    st.write(f"**Cost per sellable kg:** {fmt(cost_per_sellable_kg)}")
    st.write(f"**Profit per sellable kg:** {fmt(profit_per_sellable_kg)}")
    st.write(f"**Profit per packet:** {fmt(profit_per_packet)}")
    st.markdown('</div></div>', unsafe_allow_html=True)

with col_profit:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header"><div class="header-title">NET PROFIT</div></div>', unsafe_allow_html=True)
    color = "limegreen" if profit > 0 else ("#ff4d4f" if profit < 0 else "white")
    st.markdown(f"<div class='section-inner card-center'><div style='text-align:center; font-size:36px; font-weight:800; color:{color};'>{fmt(profit)}</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.caption("Tip: switch price mode in the section header — the other price auto-fills.")
