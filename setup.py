
from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ARTISANASSISTANT",
    version="0.1",
    author="TalentBridgeAi",
    packages=find_packages(),
    install_requires = requirements,
)

'''
from setuptools import setup, find_packages

setup(
    name="groq_artisan_marketplace",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi",
        "uvicorn[standard]",
        "pydantic",
        "requests",
        "python-dotenv",
        "langchain",
        "Pillow",
        "python-multipart",
    ],
    python_requires=">=3.10",
) 
'''