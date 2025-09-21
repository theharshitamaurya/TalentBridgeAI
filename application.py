
import streamlit as st
from dotenv import load_dotenv
from src.generator.question_generator import ArtisanAssistant
from src.common.logger import get_logger



# --- Setup ---
load_dotenv()
logger = get_logger("main")

st.set_page_config(
    page_title="🪡 Artisan Marketplace Assistant",
    layout="wide"
)

assistant = ArtisanAssistant()

# --- Menu state ---
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False
if "menu_selection" not in st.session_state:
    st.session_state.menu_selection = "🏠 Home"


# --- Hamburger menu button in left column ---
menu_col, content_col = st.columns([0.13, 0.87])  # reserve left for menu


with menu_col:
    st.markdown("""
    <style>
    .stButton > button {
        box-shadow: none !important;
        border-radius: 10px !important;
        background: #f7f7fb !important;
        border: none !important;
        color: #222668 !important;
        font-size: 18px !important;
        padding: 14px 20px !important;
        margin-bottom: 13px !important;
        font-weight: 600 !important;
        transition: background 0.10s;
    }
    .stButton > button:hover {
        background: #dde5fb !important;
        color: #2068d0 !important;
    }
    </style>
""", unsafe_allow_html=True)


    if st.button("☰", key="menu_open_btn"):
        st.session_state.menu_open = not st.session_state.menu_open


    if st.session_state.menu_open:
        st.markdown("""
            <div class="sidebar-menu-panel">
        """, unsafe_allow_html=True)
        if st.button("🏠 Home", key="nav_home", help="Go Home"):
            st.session_state.menu_selection = "🏠 Home"
            st.session_state.menu_open = False
            st.rerun()
        if st.button("👤 Profile Creator", key="nav_profile", help="Go Profile"):
            st.session_state.menu_selection = "1️⃣ Artisan Profile Creator"
            st.session_state.menu_open = False
            st.rerun()
        if st.button("🛍️ Craft Listing", key="nav_listing", help="Go Listing"):
            st.session_state.menu_selection = "2️⃣ Craft Listing Generator"
            st.session_state.menu_open = False
            st.rerun()
        if st.button("📈 Marketplace Feed", key="nav_feed", help="Go Feed"):
            st.session_state.menu_selection = "3️⃣ Smart Marketplace Feed"
            st.session_state.menu_open = False
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# --- Main content always rendered in the wide content_col ---
with content_col:
    if st.session_state.menu_selection == "🏠 Home":
        st.title("Welcome to Artisan Marketplace Assistant")
        st.write("Empowering local artisans with AI tools to market their craft and reach new audiences. 🚀")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👤 Profile Creator", key="card1"):
                st.session_state.menu_selection = "1️⃣ Artisan Profile Creator"
                st.rerun()
            st.info("Digital artisan story: tradition, culture, uniqueness.")
        with col2:
            if st.button("🛍️ Craft Listing", key="card2"):
                st.session_state.menu_selection = "2️⃣ Craft Listing Generator"
                st.rerun()
            st.info("E-commerce listings: SEO titles, persuasive descriptions.")
        with col3:
            if st.button("📈 Marketplace Feed", key="card3"):
                st.session_state.menu_selection = "3️⃣ Smart Marketplace Feed"
                st.rerun()
            st.info("AI-driven insights: categories, trending tags, trends.")

    elif st.session_state.menu_selection.startswith("1️⃣"):
        st.header("👤 Artisan Profile Creator")
        with st.form("profile_form"):
            name = st.text_input("Artisan Name")
            location = st.text_input("Location")
            craft_type = st.text_input("Craft Type")
            submitted1 = st.form_submit_button("Generate Digital Story")
            if submitted1:
                if name and location and craft_type:
                    try:
                        story = assistant.generate_profile_story(name, location, craft_type)
                        st.success("Here’s your artisan story:")
                        st.markdown(story)
                    except Exception as e:
                        st.error(str(e))
                        logger.error(f"Artisan profile error: {e}")
                else:
                    st.warning("Please fill all fields to generate the story.")

    elif st.session_state.menu_selection.startswith("2️⃣"):
        st.header("🛍️ Craft Listing Generator")
        with st.form("listing_form"):
            uploaded_photo = st.file_uploader("Product photo", type=['jpg', 'jpeg', 'png'])
            title = st.text_input("Product Title (optional)")
            description = st.text_area("Description (optional)")
            price = st.text_input("Your Price")
            cost = st.text_input("Cost per Item")
            generate_full = st.form_submit_button("Generate Complete Listing")
            if generate_full:
                try:
                    photo_value = uploaded_photo.name if uploaded_photo else None
                    result = assistant.generate_full_listing(
                        title=title,
                        description=description,
                        photo=photo_value,
                        price=price,
                        cost=cost,
                    )
                    tab1, tab2, tab3 = st.tabs(["Overview", "Business Info", "Technical"])
                    with tab1:
                        st.subheader("SEO Title")
                        st.write(result.get("seo_title", "-") or "-")
                        st.subheader("Description")
                        st.markdown(result.get("description", "-") or "-")
                        st.subheader("Category")
                        st.info(result.get("category", "-") or "-")
                    with tab2:
                        profit = result.get("profit", {})
                        profit_margin_raw = profit.get("profit_margin", "")
                        profit_amount_raw = profit.get("profit_amount", "")
                        def safe_float(value):
                            try:
                                return float(value)
                            except (TypeError, ValueError):
                                return None
                        profit_margin = safe_float(profit_margin_raw)
                        profit_amount = safe_float(profit_amount_raw)
                        st.subheader("Profit & Margin")
                        st.metric("Profit Margin (%)", f"{profit_margin:.2f}" if profit_margin is not None else "-")
                        st.metric("Profit Amount", f"{profit_amount:.2f}" if profit_amount is not None else "-")
                    with tab3:
                        st.subheader("Metafields (Shopify)")
                        st.code(result.get("metafields", "{}") or "{}", language="json")
                        st.subheader("Product Type")
                        st.info(result.get("product_type", "-") or "-")
                        st.subheader("Tags")
                        tags = result.get("tags", [])
                        st.write(", ".join(tags) if tags else "-")
                except Exception as e:
                    st.error(str(e))
                    logger.error(f"Listing error: {e}")

    elif st.session_state.menu_selection.startswith("3️⃣"):
        st.header("📈 Smart Marketplace Feed")
        with st.form("smart_feed_form"):
            prod_name_feed = st.text_input("Product Name for Trend Analysis")
            submitted3 = st.form_submit_button("Check Product Trends")
            if submitted3:
                if prod_name_feed:
                    try:
                        category, tags, trend_report = assistant.generate_smart_feed(prod_name_feed)
                        st.success(f"Category: {category}")
                        st.write(f"Tags: {', '.join(tags)}")
                        st.subheader("Trend Insights")
                        st.markdown(trend_report)
                    except Exception as e:
                        st.error(str(e))
                        logger.error(f"Smart feed error: {e}")
                else:
                    st.warning("Please enter a product name for trend analysis.")
