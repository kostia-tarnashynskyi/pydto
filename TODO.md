Here is an English TODO list based on your notes:

---

**🛠 What can be improved?**

**Documentation:**
- Add an "Advanced usage" section (e.g., FastAPI integration, nested DTOs, working with aliases/schema export).

**Tests:**
- Add property-based tests (hypothesis) to ensure DTOs behave as expected with random data.

**API:**
- Consider supporting custom validators/methods (optionally via mixins or function injection).

**Integration:**
- Add an example of integration with a cookiecutter template or FastAPI endpoint.

**DevOps:**
- Add a GitHub Actions workflow for CI (pytest, ruff, pyright, build).

**Security:**
- In the future, add filtering of sensitive data (e.g., hiding password/email fields during serialization).

**🎯 Best practices**
- Use ruff as the main formatting and linting tool (black is not needed).
- Use pyright only for type-checking, run in CI.
- Keep documentation minimalistic with examples.
- Add docstrings to all public functions and classes.
- Keep tests short and focused.