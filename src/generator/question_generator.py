import json
from src.llm.groq_client import GroqClient
from src.prompts.templates import PROFILE_TEMPLATE, LISTING_TEMPLATE, FEED_TEMPLATE
from src.common.custom_exception import CustomException
from src.config.setting import settings
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import io
import base64


class ArtisanAssistant:
    def __init__(self):
        self.llm = GroqClient(
            api_key=settings.GROQ_API_KEY,
            api_url=settings.GROQ_API_URL,
            model_name=settings.MODEL_NAME
        )

    def generate_profile_story(self, name: str, location: str, craft_type: str) -> str:
        prompt = PROFILE_TEMPLATE.format(name=name, location=location, craft_type=craft_type)
        try:
            story = self.llm.generate_text(prompt)
            return story.strip()
        except Exception as e:
            raise CustomException("Profile story generation failed", e)

    def generate_full_listing(self, title=None, description=None, photo=None, price=None, cost=None) -> dict:
        prompt = LISTING_TEMPLATE.format(
            title=title or "(let AI decide)",
            description=description or "(let AI decide)",
            price=price or "N/A",
            cost=cost or "N/A",
            photo=str(photo) if photo else "none",
        )
        try:
            output = self.llm.generate_text(prompt)
            result = json.loads(output)
        except Exception:
            result = {
                "seo_title": "",
                "description": "",
                "category": "",
                "profit": {},
                "market_price": "",
                "metafields": "{}",
                "product_type": "",
                "tags": [],
            }
        return result

    def generate_smart_feed(self, product_name: str):
        prompt = FEED_TEMPLATE.format(product_name=product_name)
        try:
            output = self.llm.generate_text(prompt).strip()
            lines = output.split("\n")
            category = lines[0] if len(lines) > 0 else "Uncategorized"
            tags = [tag.strip() for tag in lines[1].split(",")] if len(lines) > 1 else []
            trend_report = "\n".join(lines[2:]) if len(lines) > 2 else ""
            return category, tags, trend_report
        except Exception as e:
            raise CustomException("Feed generation failed", e)
        
def fetch_google_trends_graph(product_name: str):
    pytrends = TrendReq()
    pytrends.build_payload([product_name], timeframe='today 3-m')
    data = pytrends.interest_over_time()
    if data.empty:
        return None

    plt.figure(figsize=(8,3))
    plt.plot(data.index, data[product_name], label=product_name)
    plt.title(f'Google Trends interest for "{product_name}"')
    plt.xlabel('Date')
    plt.ylabel('Interest')
    plt.legend()
    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64
