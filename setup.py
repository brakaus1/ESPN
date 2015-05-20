from setuptools import setup

install_requires = [
    'beautifulsoup4',
    'Click',
]

tests_require = [
    'nose',
    'coverage',
]

setup(
    name="ESPNScraper",
    version=.01,
    author="Victor Brakauskas",
    author_email="victor brakauskas",
    url="victorbrakauskas.com",
    description="lil scraper for ESPN stats",
    packages=["nba"],
    setup_requires=['nose'],
    install_requires=install_requires,
    tests_require=tests_require,
    entry_points={
        'console_scripts': [
            'nbaespn = nba:parser',
        ],
    }
)
