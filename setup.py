from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="workflow-engine",
    version="0.0.1",
    author="Jack Lee",
    author_email="291148484@163.com",
    description="A Python library for defining and executing workflows",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacklee1995/python_worlflow",
    packages=find_packages(include=["workflow", "workflow.*"]),
    include_package_data=True,
    install_requires=[
        "requests>=2.25.1",
        "python-dotenv>=1.0.1",
        "PyYAML>=6.0.2; extra == 'yaml'",
        "watchdog>=6.0.0",
        "markdown>=3.7",
        "pandas>=2.2.3",
        "sqlite3>=3.0.0",
        "configparser>=5.3.0",
        "lxml>=5.2.1",
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
