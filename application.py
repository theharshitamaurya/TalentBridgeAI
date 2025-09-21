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

# --- CSS for sidebar, hover, and active states ---
st.markdown("""
    <style>
    /* Sidebar panel */
    .sidebar-menu-panel {
        background-color: #f7f7fb;
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 0 8px rgba(0,0,0,0.05);
        transition: max-height 0.3s ease;
        max-width: 200px;
    }
    /* Sidebar buttons */
    .stButton > button {
        box-shadow: none !important;
        border-radius: 10px !important;
        background: #f7f7fb !important;
        border: none !important;
        color: #222668 !important;
        font-size: 18px !important;
        padding: 14px 20px !important;
        margin-bottom: 8px !important;
        font-weight: 600 !important;
        width: 100%;
        text-align: left;
        transition: background 0.2s, color 0.2s;
    }
    .stButton > button:hover {
        background: #dde5fb !important;
        color: #2068d0 !important;
    }
    /* Active menu highlight */
    .stButton > button[aria-pressed="true"] {
        background: #2068d0 !important;
        color: #fff !important;
    }
    /* Hamburger button */
    .hamburger-btn {
        font-size: 24px !important;
        padding: 12px 20px !important;
        margin-bottom: 15px !important;
        text-align: center;
    }
    /* Responsive columns */
    @media (max-width: 768px) {
        .main-content {
            width: 100% !important;
            padding: 10px !important;
        }
    }
    </style>
""", unsafe_allow_html=True)

# --- Hamburger menu button in left column ---
menu_col, content_col = st.columns([0.13, 0.87])  # reserve left for menu

with menu_col:

    # Hamburger toggle button with accessibility attrs
    hamburger_pressed = st.button(
        "☰",
        key="menu_open_btn",
        help="Toggle menu",
        args=None,
        kwargs=None,
    )

    if hamburger_pressed:
        st.session_state.menu_open = not st.session_state.menu_open

    if st.session_state.menu_open:
        st.markdown('<div class="sidebar-menu-panel" role="menu" aria-label="Main menu">', unsafe_allow_html=True)
        # Define buttons with aria-pressed for active highlight and keyboard nav
        menu_items = [
            ("🏠 Home", "🏠 Home", "Go Home"),
            ("👤 Profile Creator", "1️⃣ Artisan Profile Creator", "Go Profile"),
            ("🛍️ Craft Listing", "2️⃣ Craft Listing Generator", "Go Listing"),
            ("📈 Marketplace Feed", "3️⃣ Smart Marketplace Feed", "Go Feed"),
        ]
        for label, selection, desc in menu_items:
            is_active = (st.session_state.menu_selection == selection)
            if st.button(label, key=f"nav_{selection}", help=desc, type="secondary", disabled=False):
                st.session_state.menu_selection = selection
                st.session_state.menu_open = False
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# --- Main content always rendered in the wide content_col ---
with content_col:
    st.markdown('<div class="main-content">', unsafe_allow_html=True)

    if st.session_state.menu_selection == "🏠 Home":
        st.title("Welcome to Artisan Marketplace Assistant")
        st.write("Empowering local artisans with AI tools to market their craft and reach new audiences. 🚀")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("👤 Profile Creator", key="card1"):
                st.session_state.menu_selection = "1️⃣ Artisan Profile Creator"
                st.experimental_rerun()
            st.info("Digital artisan story: tradition, culture, uniqueness.")
        with col2:
            if st.button("🛍️ Craft Listing", key="card2"):
                st.session_state.menu_selection = "2️⃣ Craft Listing Generator"
                st.experimental_rerun()
            st.info("E-commerce listings: SEO titles, persuasive descriptions.")
        with col3:
            if st.button("📈 Marketplace Feed", key="card3"):
                st.session_state.menu_selection = "3️⃣ Smart Marketplace Feed"
                st.experimental_rerun()
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

    st.markdown("</div>", unsafe_allow_html=True)
