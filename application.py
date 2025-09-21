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

# --- Layout ---
menu_col, content_col = st.columns([0.18, 0.82])  # sidebar 18%, content 82%

# --- Sidebar Menu ---
with menu_col:
    st.markdown("""
        <style>
        .sidebar-menu-panel {
            background: #f7f8fc;
            padding: 15px 10px;
            border-radius: 12px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
        }
        .menu-btn {
            display: block;
            width: 100%;              /* same width */
            height: 50px;             /* same height */
            line-height: 25px;        /* centers text */
            text-align: left;
            background: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            padding: 12px 18px;
            margin-bottom: 10px;
            font-size: 16px;
            font-weight: 600;
            color: #333333;
            cursor: pointer;
            transition: all 0.2s ease-in-out;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        .menu-btn:hover {
            background: #eaf2ff;
            color: #1a73e8;
            border-color: #1a73e8;
        }
        .menu-btn.active {
            background: #1a73e8 !important;
            color: #ffffff !important;
            border-color: #1a73e8 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    if st.button("☰", key="menu_open_btn"):
        st.session_state.menu_open = not st.session_state.menu_open

    if st.session_state.menu_open:
        st.markdown("<div class='sidebar-menu-panel'>", unsafe_allow_html=True)

        def nav_button(label, key, selection):
            is_active = st.session_state.menu_selection == selection
            btn_class = "menu-btn active" if is_active else "menu-btn"
            clicked = st.button(label, key=key)
            st.markdown(f"""
                <script>
                    var btn = window.parent.document.querySelector('button[kind="{key}"]');
                    if (btn) {{
                        btn.className = '{btn_class}';
                    }}
                </script>
            """, unsafe_allow_html=True)
            if clicked:
                st.session_state.menu_selection = selection
                st.session_state.menu_open = True
                st.rerun()

        nav_button("🏠 Home", "nav_home", "🏠 Home")
        nav_button("👤 Profile Creator", "nav_profile", "1️⃣ Artisan Profile Creator")
        nav_button("🛍️ Craft Listing", "nav_listing", "2️⃣ Craft Listing Generator")
        nav_button("📈 Marketplace Feed", "nav_feed", "3️⃣ Smart Marketplace Feed")

        st.markdown("</div>", unsafe_allow_html=True)

# --- Main Content ---
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
