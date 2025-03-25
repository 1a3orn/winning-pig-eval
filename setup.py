from setuptools import setup, find_packages

setup(
    name="playing-new-games",  # Replace with your desired package name
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    
    # Optional but recommended metadata
    author="1a3orn",
    author_email="1a3orn@protonmail.com",
    description="Can LLMs play newly-invented games?",
    long_description=open("README.md").read() if os.path.exists("README.md") else "",
    long_description_content_type="text/markdown",
    
    # Add any package dependencies here
    install_requires=[
        # "requests>=2.25.1",
        # "pandas>=1.2.0",
    ],
    
    # Python version compatibility
    python_requires=">=3.7",
)
