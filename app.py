
import streamlit as st

st.set_page_config(page_title="Profit / Loss Calculator", page_icon="💹", layout="wide")

# ---------- Styles ----------
st.markdown(
    """
    <style>
    .section {border:1px solid #DDD; padding:18px; border-radius:10px; background:#fafafa;}
    .titlebar {border:1px solid #DDD; padding:16px; border-radius:10px; background:#f2f2f2; text-align:center;}
    .big {font-size: 28px; font-weight: 700;}
    .med {font-size: 18px; font-weight: 600;}
    .profit {font-size: 36px; font-weight: 800;}
    .label {font-weight: 600;}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="titlebar"><span class="big">PROFIT LOSS CALCULATOR</span></div>', unsafe_allow_html=True)
st.write("")

# ---------- Helpers ----------
def ffloat(x, d=0.0):
    try:
        return float(x)
    except Exception:
        return d

def fint(x, d=0):
    try:
        return int(float(x))
    except Exception:
        return d

def fmt(x):
    return f"{x:,.2f}"

# ---------- Top row (3 columns) ----------
col_inputs, col_commission, col_right = st.columns([1.1, 1, 1])

with col_inputs:
    st.markdown('<div class="section"><div class="med">INPUTS</div>', unsafe_allow_html=True)
    packet_weight = st.number_input("Packet weight (kg)", value=15.0, min_value=0.0, step=0.1)
    num_packets   = st.number_input("Number of packets", value=100, min_value=0, step=1)
    rent_per_packet = st.number_input("Rent per packet", value=35.0, min_value=0.0, step=0.5)
    freight_per_kg  = st.number_input("Freight per kg", value=2.5, min_value=0.0, step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

with col_commission:
    st.markdown('<div class="section"><div class="med">COMMISSION TO MIDDLEMAN</div>', unsafe_allow_html=True)
    commission_mode = st.radio("Commission mode", ["% of gross revenue", "Flat per packet", "Flat per kg (total weight)"], index=0)
    colc1, colc2 = st.columns(2)
    with colc1:
        commission_pct = st.number_input("Percentage (%)", value=0.0, min_value=0.0, step=0.25)
        commission_pp  = st.number_input("Flat per packet", value=0.0, min_value=0.0, step=0.5)
        commission_kg  = st.number_input("Flat per kg", value=0.0, min_value=0.0, step=0.1)
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="med">PRICE INPUT MODE</div>', unsafe_allow_html=True)
    price_mode = st.radio("", ["Buying price per kg", "Cost per packet"], index=0, horizontal=True)

    colp1, colp2 = st.columns(2)
    with colp1:
        buy_price_per_kg = st.number_input("Buying price per kg", value=0.0, min_value=0.0, step=0.5, key="buykg")
    with colp2:
        cost_per_packet_manual = st.number_input("Cost per packet", value=0.0, min_value=0.0, step=1.0, key="cpp")

    wastage_pct = st.number_input("Wastage %", value=0.0, min_value=0.0, step=0.5)
    selling_price_kg = st.number_input("Selling price per kg", value=0.0, min_value=0.0, step=0.5)
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

# ---------- Core calculations ----------
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

# ---------- Bottom row (3 columns) ----------
col_inv, col_results, col_profit = st.columns([1.1, 1.2, 0.9])

with col_inv:
    st.markdown('<div class="section"><div class="med">INVESTMENT</div>', unsafe_allow_html=True)
    st.write(f"**Total packets:** {num_packets:,d}")
    st.write(f"**Total weight:** {fmt(total_weight)} kg")
    st.write(f"**Cost per packet (buy × weight):** {fmt(cost_per_packet)}")
    st.write(f"**Total product cost:** {fmt(total_product_cost)}")
    st.write(f"**Total rent:** {fmt(total_rent)}")
    st.write(f"**Total freight:** {fmt(total_freight)}")
    st.write(f"**Commission:** {fmt(commission_amount)}")
    st.markdown(f"**🧮 GRAND TOTAL COST:** <span class='med'>{fmt(grand_total_cost)}</span>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_results:
    st.markdown('<div class="section"><div class="med">RESULTS</div>', unsafe_allow_html=True)
    st.write(f"**Sellable weight (kg):** {fmt(sellable_weight)}")
    st.write(f"**Gross revenue:** {fmt(gross_revenue)}")
    st.write(f"**Commission amount:** {fmt(commission_amount)}")
    st.write(f"**Cost per kg (on total weight):** {fmt(cost_per_kg_total)}")
    st.write(f"**Cost per sellable kg:** {fmt(cost_per_sellable_kg)}")
    st.write(f"**Profit per sellable kg:** {fmt(profit_per_sellable_kg)}")
    st.write(f"**Profit per packet:** {fmt(profit_per_packet)}")
    st.markdown('</div>', unsafe_allow_html=True)

with col_profit:
    st.markdown('<div class="section" style="display:flex; align-items:center; justify-content:center; min-height:220px;">', unsafe_allow_html=True)
    color = "green" if profit > 0 else ("red" if profit < 0 else "black")
    st.markdown(f"<div style='text-align:center;'><div class='med'>NET PROFIT</div><div class='profit' style='color:{color};'>{fmt(profit)}</div></div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer note
st.caption("Tip: switch price mode to enter either Buying price per kg or Cost per packet — the other auto-fills.")
