import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI


DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEFAULT_MODEL = "deepseek-chat"


load_dotenv()


class TravelPlanner:
    def __init__(self, model=DEFAULT_MODEL, api_key=None):
        api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is not set.")

        self.client = OpenAI(
            api_key=api_key,
            base_url=DEEPSEEK_BASE_URL,
        )
        self.model = model

    def process_request(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                stream=True,
            )

            def stream_response():
                for chunk in response:
                    delta = chunk.choices[0].delta.content
                    if delta is not None:
                        yield delta

            return st.write_stream(stream_response())
        except Exception as exc:
            st.error(f"Error: {exc}")
            return ""


def get_system_prompts():
    return {
        "Trip Itinerary": """You are a travel expert who creates detailed and personalized trip itineraries.
Follow these guidelines:
1. Start with an overview of the destination
2. Include a day-by-day breakdown of activities
3. Suggest must-visit attractions and hidden gems
4. Provide recommendations for local cuisine and dining
5. Include transportation tips and options
6. Add cultural or historical context for key locations
7. Offer packing tips based on the destination's climate""",
        "Travel Tips": """You are a seasoned traveler who provides practical advice for smooth trips.
Provide tips on:
1. Best times to visit specific destinations
2. Budgeting and saving money while traveling
3. Navigating local customs and etiquette
4. Staying safe and healthy during travel
5. Packing efficiently for different types of trips
6. Finding affordable accommodations and flights
7. Making the most of layovers and short trips""",
        "Destination Recommendations": """You are a travel guide who suggests destinations based on user preferences.
Consider:
1. The traveler's interests, such as adventure, relaxation, culture, or food
2. Budget constraints
3. Preferred climate and season
4. Travel duration
5. Group size and demographics, such as family, solo, or couple
6. Accessibility and travel restrictions
7. Unique experiences or events happening at the destination""",
    }


def get_example_prompts():
    return {
        "Trip Itinerary": {
            "placeholder": """Examples:
1. Plan a 5-day trip to Japan focusing on culture and food
2. Create a 7-day itinerary for a family vacation in Italy
3. Suggest a 3-day weekend getaway for adventure lovers in Costa Rica
4. Design a 10-day road trip across the American Southwest
5. Plan a romantic 4-day trip to Paris

Your request:""",
            "default": "한국의 역사와 음식을 위한 7일간의 한국 여행 계획을 작성해 주세요.",
        },
        "Travel Tips": {
            "placeholder": """Ask for travel tips or advice.

Examples:
1. What are the best ways to save money while traveling in Europe?
2. How can I stay safe while traveling solo in South America?
3. What should I pack for a two-week trip to Southeast Asia?
4. What are some tips for traveling with young children?
5. How do I handle language barriers in non-English-speaking countries?""",
            "default": "유럽 여행 중 비용을 절약하는 가장 좋은 방법을 알려 주세요.",
        },
        "Destination Recommendations": {
            "placeholder": """Describe your preferences for destination suggestions.

Examples:
1. I want a relaxing beach vacation with good food and clear water
2. I'm looking for an adventurous trip with hiking and wildlife
3. Suggest a cultural destination with historical sites and museums
4. I need a budget-friendly destination for a family of four
5. Where can I go for a romantic getaway with stunning views?""",
            "default": "맛있는 음식과 맑은 바다가 있는 휴양지를 추천해 주세요.",
        },
    }


def main():
    st.set_page_config(
        page_title="DeepSeek Travel Assistant",
        page_icon="\u2708\ufe0f",
        layout="wide",
    )

    st.title("\u2708\ufe0f DeepSeek Travel Assistant - 2021810009 \uae40\ub450\uc601")
    st.markdown("Powered by DeepSeek API")

    system_prompts = get_system_prompts()
    example_prompts = get_example_prompts()

    with st.sidebar:
        st.title("Settings")
        model = st.text_input("DeepSeek model", value=DEFAULT_MODEL)
        env_api_key = os.getenv("DEEPSEEK_API_KEY")
        api_key = env_api_key or st.text_input(
            "DeepSeek API key",
            type="password",
            help="For Render deployment, set this as DEEPSEEK_API_KEY.",
        )
        mode = st.selectbox(
            "Choose Mode",
            ["Trip Itinerary", "Travel Tips", "Destination Recommendations"],
        )

        st.markdown("---")
        st.markdown(f"**Current Mode**: {mode}")
        st.markdown("**Mode Description:**")
        st.markdown(system_prompts[mode].replace("\n", "\n\n"))

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(f"### Input for {mode}")
        user_prompt = st.text_area(
            "Enter your travel preferences or questions:",
            height=300,
            placeholder=example_prompts[mode]["placeholder"],
            value=example_prompts[mode]["default"],
        )

        process_button = st.button(
            "\u2708\ufe0f Process",
            type="primary",
            use_container_width=True,
        )

    with col2:
        st.markdown("### Output")
        output_container = st.container()

        if process_button:
            if user_prompt.strip():
                if not api_key:
                    st.warning("Please enter your DeepSeek API key.")
                    return
                with st.spinner("Planning your trip..."):
                    with output_container:
                        assistant = TravelPlanner(model=model, api_key=api_key)
                        assistant.process_request(system_prompts[mode], user_prompt)
            else:
                st.warning("Please enter some input.")


if __name__ == "__main__":
    main()
