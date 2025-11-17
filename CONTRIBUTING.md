# Contributing to Mac Health Pulse

Hey! Thanks for checking out Mac Health Pulse. I appreciate any contributions, whether it's a bug fix, new feature, or just fixing a typo in the docs.

## Getting Started

1. Fork the repo
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Mac-Health-Pulse.git`
3. Create a new branch: `git checkout -b your-feature-name`
4. Make your changes
5. Run the tests to make sure nothing broke: `./run_tests.sh`
6. Commit your changes: `git commit -m "Add some feature"`
7. Push to your fork: `git push origin your-feature-name`
8. Open a Pull Request

## Running the Project Locally

Make sure you have Python 3.8+ installed, then:

```bash
pip install -r requirements.txt
python main.py
```

## Running Tests

```bash
# Run all tests
./run_tests.sh

# Or use pytest directly
pip install -r requirements-test.txt
pytest
```

Check out `TESTING.md` for more details on the test suite.

## Code Style

Nothing too strict here, but try to:
- Follow PEP 8 (mostly)
- Add type hints where it makes sense
- Write docstrings for public functions
- Keep it readable

If you're unsure, just look at the existing code and try to match the style.

## Reporting Bugs

Found a bug? Open an issue and include:
- What you were trying to do
- What happened instead
- Steps to reproduce it
- Your macOS version and Python version

## Feature Requests

Got an idea? Open an issue and let's discuss it! I'm open to new ideas, especially if they improve the UX or add useful monitoring capabilities.

## Questions?

Feel free to open an issue if you have questions. I'll try to respond when I can.

Thanks for contributing!
