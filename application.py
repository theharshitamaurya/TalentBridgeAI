import streamlit as st
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
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


# --- Sidebar Navigation ---
with st.sidebar:
    st.image("image/logo.png", width=80)  # sample icon
    st.markdown("## Artisan Marketplace")
    menu_options = ["Home", "Profile Story Generator", "Craft Listing", "Smart Marketplace Feed"]
    menu_icons = ["house", "person", "shop", "graph-up"]

    page_param = st.query_params.get("page", ["Home"])[0]
    if page_param not in menu_options:
        page_param = "Home"

    selection = option_menu(
        "MENU",
        menu_options,
        icons=menu_icons,
        menu_icon="☰",
        default_index=menu_options.index(page_param),
    )

    # Update query param if menu selection changed
    if st.query_params.get("page", [None])[0] != selection:
        st.query_params["page"] = selection


# --- Helper: Safe number parsing ---
def parse_number(value):
    if not value:
        return None
    value = str(value).replace("%", "").strip()
    try:
        return float(value)
    except ValueError:
        return None


# --- Main Content ---
if selection == "Home":
    st.title("Welcome to Artisan Marketplace Assistant")
    st.write("Empowering local artisans with AI tools to market their craft and reach new audiences. 🚀")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("👤 Profile Story Generator"):
            st.query_params["page"] = "Story Generator"
        st.info("Digital artisan story: Create a compelling digital story for your craft that highlights your tradition, culture, and uniqueness. This feature helps artisans craft an engaging narrative that connects emotionally with buyers and builds a meaningful brand identity.")
    with col2:
        if st.button("🛍️ Craft Listing"):
            st.query_params["page"] = "Craft Listing"
        st.info("Generate complete product listings with SEO-friendly titles, persuasive descriptions, and competitive pricing. This tool simplifies creating effective e-commerce listings ready for platforms like Shopify, making products more visible and attractive to buyers.")
    with col3:
        if st.button("📈 Marketplace Feed"):
            st.query_params["page"] = "Smart Marketplace Feed"
        st.info("Get AI-powered insights into product trends, popular categories, and buyer interests relevant to your craft. These insights help artisans stay updated on market demands, optimize their offerings, and reach the right audience for growth.")

    st.markdown("---")
    st.subheader("Featured Artisans")


    # First row of 3 artisans
    colA, colB, colC = st.columns(3)
    with colA:
        st.image("image/molten glass.jpg", width="stretch")
        st.markdown("### Sandeep Rao")
        st.markdown("<span style='background:#d0e9ff;padding:4px;border-radius:4px;'>Glassblower (Glass Artist)</span>", unsafe_allow_html=True)
        st.write("Sandeep Rao is a molten glass artisan known for hot glass blowing and creating colorful decorative glassware.")
    with colB:
        st.image("image/indian kurta.jpg", width="stretch")
        st.markdown("### Rahul Sinha")
        st.markdown("<span style='background:#d6f5d6;padding:4px;border-radius:4px;'>embroidered ethnic wear</span>", unsafe_allow_html=True)
        st.write("Rahul Sinha is a textile designer specializing in heritage embroidery and handcrafted kurta collections.")
    with colC:
        st.image("image/woman painting.jpg", width="stretch")
        st.markdown("### Ankit Verma")
        st.markdown("<span style='background:#cce0ff;padding:4px;border-radius:4px;'>Watercolor Artist (Painter)</span>", unsafe_allow_html=True)
        st.write("Ankit Verma is a nature-inspired painter best known for delicate bird-and-flower watercolor compositions.")

    # st.markdown("---")
    st.text(" ")


    # Second row of 2 artisans (left empty space for alignment)
    colD, colE, colF = st.columns(3)
    with colD:
        st.image("image/pottary.jpg", width="stretch")
        st.markdown("### Asha Gupta")
        st.markdown("<span style='background:#fff0c2;padding:4px;border-radius:4px;'>Potter (Ceramic Artist)</span>", unsafe_allow_html=True)
        st.write("Asha Gupta is a potter crafting stoneware and terracotta vessels using traditional coil and slab techniques.")
    with colE:
        st.image("image/painting.jpg", width="stretch")
        st.markdown("### Neha Das")
        st.markdown("<span style='background:#cce0ff;padding:4px;border-radius:4px;'>Visual Artist (Painter)</span>", unsafe_allow_html=True)
        st.write("Neha Das is a visual artist specializing in expressive portraits and landscapes using mixed media techniques.")
    with colF:
        st.write("")  # empty for layout balance

elif selection == "Profile Story Generator":
    st.header("👤 Artisan Brand Story Generator")
    with st.form("profile_form"):
        name = st.text_input("Artisan Name")
        location = st.text_input("Location")
        craft_type = st.text_input("Craft Type")
        submitted = st.form_submit_button("Generate Digital Story")

        if submitted:
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


elif selection == "Craft Listing":
    st.header("🛍️ Craft Listing Generator")
    with st.form("listing_form"):
        uploaded_photo = st.file_uploader("Product photo", type=['jpg', 'jpeg', 'png'])
        title = st.text_input("Product Title")
        description = st.text_area("Description (optional)")
        price = st.text_input("Your Price")
        cost = st.text_input("Cost per Item")
        generate_full = st.form_submit_button("Generate Complete Listing")

        if generate_full:
            if not title or not price or not cost:
                st.warning("Please fill in Title, Price, and Cost.")
            else:
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
                        profit_margin = parse_number(profit.get("profit_margin", ""))
                        profit_amount = parse_number(profit.get("profit_amount", ""))

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

elif selection == "Smart Marketplace Feed":
    st.header("📈 Smart Marketplace Feed")
    with st.form("smart_feed_form"):
        prod_name_feed = st.text_input("Product Name for Trend Analysis")
        submitted = st.form_submit_button("Check Product Trends")

        if submitted:
            if prod_name_feed:
                try:
                    category, tags, trend_report = assistant.generate_smart_feed(prod_name_feed)

                    category_clean = category.replace("Category:", "").strip()
                    tags_clean = [t.replace("Tags:", "").strip() for t in tags if t.strip()]

                    st.success(f"Category: {category_clean}")
                    st.write(f"Tags: {', '.join(tags_clean) if tags_clean else '-'}")
                    st.subheader("Trend Insights")
                    st.markdown(trend_report or "No trend insights available.")

                except Exception as e:
                    st.error(f"Error generating smart feed: {e}")
                    logger.error(f"Smart feed error: {e}")
            else:
                st.warning("Please enter a product name for trend analysis.")
st.markdown("---")
st.subheader("How It Works")

st.markdown("""
1. Select a feature from the sidebar menu.
2. Fill in the required details such as artisan info or product info.
3. Let AI generate content: profiles, listings, or trend reports instantly.
4. Copy, use, and share your AI-generated content to expand your craft’s reach on social media.
""")
