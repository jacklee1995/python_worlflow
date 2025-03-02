from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="workflow_engine",
    version="0.0.1",
    author="Jack Lee",
    author_email="291148484@163.com",
    description="A flexible and extensible workflow automation framework designed to streamline task execution, resource management, and configuration handling for developers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacklee1995/python_worlflow",
    packages=find_packages(include=["workflow_engine", "workflow_engine.*"]),
    include_package_data=True,
    install_requires=[
        "aiohappyeyeballs==2.4.6",
        "aiohttp==3.11.12",
        "aiosignal==1.3.2",
        "aiosmtplib==4.0.0",
        "attrs==25.1.0",
        "certifi==2025.1.31",
        "cffi==1.17.1",
        "charset-normalizer==3.4.1",
        "colorama==0.4.6",
        "configparser==7.1.0",
        "cryptography==44.0.1",
        "frozenlist==1.5.0",
        "greenlet==3.1.1",
        "idna==3.10",
        "kafka==1.3.5",
        "load-dotenv==0.1.0",
        "lxml==5.3.1",
        "Markdown==3.7",
        "multidict==6.1.0",
        "numpy==2.2.3",
        "pandas==2.2.3",
        "propcache==0.2.1",
        "pycparser==2.22",
        "python-dateutil==2.9.0.post0",
        "python-dotenv==1.0.1",
        "pytz==2025.1",
        "PyYAML==6.0.2",
        "requests==2.32.3",
        "six==1.17.0",
        "SQLAlchemy==2.0.38",
        "typing_extensions==4.12.2",
        "tzdata==2025.1",
        "urllib3==2.3.0",
        "watchdog==6.0.0",
        "yarl==1.18.3",
    ],
    extras_require={
        'yaml': ['PyYAML>=6.0.2'],  # 可选依赖
    },
    classifiers=[  # PyPI 分类器
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",  # Python 版本要求
    entry_points={  # 命令行入口点
        "console_scripts": [
            "workflow=workflow.cli.main:main",  # 示例：workflow 命令
        ],
    },
)
