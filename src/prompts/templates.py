# Prompt templates for Groq generation

PROFILE_TEMPLATE = (
    "You are a creative storyteller for local artisans. "
    "Generate a compelling digital story for an artisan with the following details:\n"
    "- Name: {name}\n"
    "- Location: {location}\n"
    "- Craft type: {craft_type}\n\n"
    "Guidelines:\n"
    "- Write in a friendly, inspiring tone suitable for social media.\n"
    "- Keep it concise (150–200 words).\n"
    "- Highlight tradition, culture, and uniqueness of the craft.\n"
    "- Make it engaging so buyers feel emotionally connected.\n"
)

LISTING_TEMPLATE = (
    "You are an expert e-commerce copywriter and marketplace analyst. "
    "Using the product details below, generate a complete product listing in valid JSON. "
    "The output MUST be valid JSON only (no explanations, no text outside JSON).\n\n"

    "Product details:\n"
    "- Title: {title}\n"
    "- Description: {description}\n"
    "- Price: {price}\n"
    "- Cost per item: {cost}\n"
    "- Photo info: {photo}\n\n"

    "JSON keys required:\n"
    "1. seo_title: An SEO-optimized product title (≤70 characters, keyword-rich, compelling).\n"
    "2. description: An engaging, persuasive, SEO-optimized description (120–200 words).\n"
    "3. category: Best-fit e-commerce category about it from the given image (e.g., Home Decor, Jewelry, Apparel or more).\n"
    "4. profit: JSON object with 'profit_margin' (percentage) and 'profit_amount' (numeric, same currency as price).\n"
    "5. market_price: Estimated competitive price range for similar products.\n"
    "6. metafields: JSON object compatible with Shopify (keys like 'material', 'care_instructions', 'origin').\n"
    "7. product_type: Recommended product type (specific but not too narrow).\n"
    "8. tags: Array of 5–10 relevant keywords/tags (do not return as a string).\n\n"

    "⚠️ Rules:\n"
    "- Output must be valid JSON ONLY.\n"
    "- Use double quotes for all keys and string values.\n"
    "- No markdown, no comments, no explanations.\n"
    "- Ensure fields are never empty: if unknown, use an empty string \"\" or empty array [].\n"
)

FEED_TEMPLATE = (
    "You are an AI marketplace analyst. For the given product name, suggest where it fits best online.\n\n"
    "Product Name: {product_name}\n\n"
    "Output Format (plain text, 3 lines exactly):\n"
    "1. Category (best marketplace category).\n"
    "2. Tags (comma-separated, 5–10 tags)\n"
    "3. Trend Insights (1–2 sentences on current trends, platforms, or regions where it’s popular)\n"

)

# Mini templates for future extension (not currently used)

SEO_TITLE_TEMPLATE = (
    "You are an SEO expert. Generate a short, compelling, keyword-rich title "
    "for an online product listing.\n\n"
    "Details:\n"
    "- Description: {description}\n"
    "- Photo info: {photo}\n\n"
    "Rules:\n"
    "- Keep under 70 characters.\n"
    "- Make it engaging, clear, and optimized for search engines.\n"
    "- Output the title only, no extra text.\n"
)

DESCRIPTION_TEMPLATE = (
    "You are an e-commerce copywriter. Write a persuasive, SEO-friendly product description.\n\n"
    "Details:\n"
    "- Title: {title}\n"
    "- Photo info: {photo}\n\n"
    "Guidelines:\n"
    "- Length: 100–150 words.\n"
    "- Tone: professional yet friendly.\n"
    "- Focus on benefits, uniqueness, and emotional appeal.\n"
    "- Use simple formatting with short sentences.\n"
    "- Output the description only, no extra text.\n"
)

