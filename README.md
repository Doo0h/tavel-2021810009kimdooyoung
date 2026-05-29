# DeepSeek Travel Assistant

2021810009 김두영

Streamlit travel planning app powered by the DeepSeek API.

## Local Run

Create a `.env` file:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key_here
```

Install dependencies and run:

```bash
pip install -r requirements.txt
streamlit run travel_planner.py
```

## Render

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
streamlit run travel_planner.py --server.port $PORT --server.address 0.0.0.0
```

Environment variable:

```text
DEEPSEEK_API_KEY
```
