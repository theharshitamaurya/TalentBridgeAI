# TalentBridgeAI – AI Marketplace Assistant for Artisans

TalentBridgeAI empowers local artisans to share authentic stories, create SEO-friendly product listings, and access real-time market insights—without needing digital marketing expertise.

---

## Table of Contents

* [Project Overview](#project-overview)
* [Setup & Installation](#setup--installation)
* [Usage](#usage)
* [Project Structure](#project-structure)
* [Configuration & Environment](#configuration--environment)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [Contacts](#contacts)
* [License](#license)

---

## Project Overview

TalentBridgeAI is an AI-powered assistant built for artisans to overcome digital marketing challenges.
It helps artisans:

* Build authentic digital profiles
* Create compelling product descriptions
* Discover craft trends in real time

By automating storytelling, content generation, and market analytics, TalentBridgeAI allows artisans to focus on their craft while AI manages the digital presence.

---

## Setup & Installation

### Prerequisites

* Python 3.9+
* Streamlit (for frontend)
* Access to Groq LLM API (or configured LLM backend)

### Installation Steps

1. Clone the repository:

   ```
   git clone https://github.com/theharshitamaurya/talentbridgeai.git
   cd talentbridgeai
   ```
2. Set up a Python environment:

   ```
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:

   ```
   pip install -e .
   ```
4. Run the application:

   ```
   streamlit run application.py
   ```

---

## Usage

* Open the app in your browser ([https://talentbridgeai.streamlit.app/?](https://talentbridgeai.streamlit.app/?page=Smart+Marketplace+Feed)).
* Create artisan profiles by entering basic info.
* Upload craft details or images to generate SEO-friendly listings.
* Explore real-time marketplace insights and trending crafts.
* Export or share content directly to supported channels.

---

## Project Structure

```
src/
├── common/
│   ├── custom_exception.py
│   ├── logger.py
├── config/
│   ├── setting.py
├── generators/
│   ├── question_generator.py
├── llm/
│   ├── groq_client.py
├── models/
│   ├── question_schemas.py
├── templates/
│   ├── templates.py
├── utils/
│   ├── helpers.py
application.py
requirements.txt
setup.py
.env
```

---

## Configuration & Environment

* Update `.env` with API keys, database URIs, and logging configurations.
* Modify `config/setting.py` for environment-specific variables.
* Custom templates can be adjusted in `templates/templates.py`.

---

## Contributing

Contributions are welcome!

* For major changes, open an issue first to discuss ideas.
* Submit pull requests with detailed descriptions.
* Follow repository coding standards and logging practices.

---

## Contacts

* GitHub Repository: [GitHub Repository](https://github.com/theharshitamaurya/talentbridgeai)
* Maintainer: \[Harshita Maurya / harshita20maurya@gmail.com]
---

*Last updated: September 22, 2025*

---

