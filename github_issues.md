# GitHub Issues to Create

Since I cannot access the GitHub website directly to create issues, please copy and paste the following content to create the two issues on your repository.

## Issue 1: Add Input Validation

**Title:** Add input validation for season and plant type
**Description:**
Currently, the program accepts any string as input for the season and plant type. If a user enters an invalid season (e.g., "autumn") or plant type, the program just prints a default message or "No advice".

We should improve the user experience by adding a validation loop that keeps asking for input until the user enters a valid option:
- Valid seasons: `summer`, `winter`
- Valid plant types: `flower`, `vegetable`

---

## Issue 2: Refactor Advice Logic to Dictionary

**Title:** Refactor advice logic to use dictionaries
**Description:**
The current implementation uses multiple `if/elif/else` statements to determine the advice to return. This is repetitive and harder to maintain.

We should refactor the code to store the advice strings in a Python dictionary. This will make the `get_season_advice` and `get_plant_advice` functions cleaner and easier to extend in the future.

---

# Pull Request Workflow Status

I have already completed the local development steps for these issues:

**For Issue 1 (Input Validation):**
- [x] Create branch `feature/input-validation`
- [x] Implement changes
- [x] Commit and push to GitHub
- [ ] **Action Required:** Open Pull Request (Link: https://github.com/TheMartin-lab/garden-app/pull/new/feature/input-validation)

**For Issue 2 (Dictionary Refactor):**
- [x] Create branch `refactor/dictionary-lookup`
- [x] Implement changes
- [x] Commit and push to GitHub
- [x] Open Pull Request (Merged)

---

## Issue 3: Add Interactive Loop

**Title:** Allow user to query multiple times
**Description:**
Add a loop to the main program so the user can ask for advice multiple times without restarting the program.

**Workflow Status:**
- [x] Create branch `feature/interactive-loop`
- [x] Implement changes
- [x] Commit and push to GitHub
- [ ] **Action Required:** Open Pull Request (Link: https://github.com/TheMartin-lab/garden-app/pull/new/feature/interactive-loop)
