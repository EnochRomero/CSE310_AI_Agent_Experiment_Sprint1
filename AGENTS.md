# AGENTS.md

## Purpose

You are an AI coding agent responsible for helping develop, maintain, test, and debug a **2D platformer game written in Python**.

Your primary goals are:

1. Produce working, maintainable Python code.
2. Preserve existing game functionality when making changes.
3. Build gameplay systems in small, testable pieces.
4. Write and run tests for new functionality.
5. Avoid introducing regressions.
6. Keep the game architecture understandable for a human developer.
7. Prefer simple solutions over unnecessary complexity.
8. Never claim that code works without actually testing it when testing is possible.
9. Leave clear comments in all code you write.

The project should be treated as a real software project, not as a collection of disconnected scripts.

---

# 1. General Agent Rules

## 1.1 Inspect Before Changing

Before modifying code:

* Inspect the project structure.
* Identify the game entry point.
* Identify the game engine/framework being used.
* Identify existing player, enemy, level, physics, UI, and asset systems.
* Read relevant existing code before creating replacement code.
* Check whether similar functionality already exists.

Do not unnecessarily rewrite existing systems.

If the project already has an established architecture, follow it unless there is a clear reason to change it.

---

## 1.2 Make Small Changes

Prefer small, focused changes.

For example:

Good:

```text
Add player horizontal acceleration
→ add/update tests
→ run tests
→ run game
→ manually verify movement
```

Avoid:

```text
Rewrite player
Rewrite physics
Rewrite level system
Rewrite collision system
Rewrite game loop
```

all in one change.

Large changes should be broken into logical steps.

---

## 1.3 Preserve Existing Functionality

Before changing an existing system, determine:

* What the system currently does.
* Which files depend on it.
* Which tests cover it.
* Whether the behavior is intentional.

Do not remove functionality simply because it is not immediately relevant to the current task.

---

# 2. Technology

Unless the project specifies otherwise, use:

* Python 3
* Pygame for the 2D game framework
* `pytest` for automated testing
* `ruff` for linting
* `black` for formatting
* Git for version control

Recommended project structure:

```text
project/
├── AGENTS.md
├── README.md
├── requirements.txt
├── pyproject.toml
│
├── src/
│   └── game/
│       ├── __init__.py
│       ├── main.py
│       ├── game.py
│       ├── settings.py
│       │
│       ├── entities/
│       │   ├── __init__.py
│       │   ├── player.py
│       │   ├── enemy.py
│       │   └── projectile.py
│       │
│       ├── systems/
│       │   ├── physics.py
│       │   ├── collision.py
│       │   ├── camera.py
│       │   └── input.py
│       │
│       ├── levels/
│       │   ├── __init__.py
│       │   └── level.py
│       │
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── menu.py
│       │   └── hud.py
│       │
│       └── assets/
│           ├── images/
│           ├── sounds/
│           └── music/
│
└── tests/
    ├── test_player.py
    ├── test_physics.py
    ├── test_collision.py
    ├── test_enemies.py
    ├── test_levels.py
    └── test_game.py
```

If the existing project uses a different structure, do not reorganize the entire project merely to match this example.

---

# 3. Architecture

The game should generally separate:

### Game loop

Responsible for:

* Processing events
* Updating game state
* Rendering
* Maintaining frame timing

### Entities

Examples:

* Player
* Enemy
* Platform
* Projectile
* Collectible
* Moving platform

Entities should primarily contain their own state and behavior.

### Systems

Systems should handle reusable game logic such as:

* Physics
* Collision detection
* Camera movement
* Input
* Level management

### UI

UI should be separated from gameplay logic whenever practical.

Examples:

* Main menu
* Pause menu
* HUD
* Health display
* Score
* Game-over screen

---

# 4. Game Loop Requirements

The main game loop should follow a predictable structure:

```python
while running:
    dt = clock.tick(FPS) / 1000.0

    handle_events()

    update(dt)

    render()

    pygame.display.flip()
```

Do not place large amounts of gameplay logic directly inside the main loop.

Use functions/classes to separate responsibilities.

---

# 5. Delta Time

Movement and physics should generally use delta time (`dt`) rather than assuming a fixed number of frames.

Prefer:

```python
player.x += player.velocity_x * dt
```

over:

```python
player.x += player.velocity_x
```

when appropriate.

The game should remain reasonably consistent across different frame rates.

Avoid tying gameplay speed directly to FPS.

---

# 6. Player Requirements

The player system should support, when applicable:

* Horizontal movement
* Acceleration/deceleration
* Jumping
* Gravity
* Collision with platforms
* Falling
* Death
* Respawning
* Animation state
* Health
* Damage
* Invulnerability frames
* Checkpoints

Player behavior should be deterministic enough to test.

Avoid embedding rendering-only logic into movement and physics calculations.

---

# 7. Physics

Physics should be predictable and configurable.

Important values should generally be stored in one location:

```python
GRAVITY = 1800
PLAYER_SPEED = 300
PLAYER_JUMP_SPEED = 650
```

Avoid scattering unexplained magic numbers throughout the code.

Physics must correctly handle:

* Gravity
* Horizontal movement
* Vertical movement
* Jumping
* Falling
* Landing
* Slopes if supported
* Moving platforms if supported
* Collision resolution

---

# 8. Collision Detection

Collision code must account for:

* Horizontal collisions
* Vertical collisions
* Landing on platforms
* Hitting ceilings
* Walking into walls
* Falling through platforms when intended
* One-way platforms when supported
* Moving platforms when supported

Use appropriate collision primitives such as:

```python
pygame.Rect
```

when possible.

Collision behavior should be tested independently from rendering.

---

# 9. Levels

Levels should be represented using structured data rather than hardcoding every object into the game loop.

A level may contain:

```text
Platforms
Enemies
Collectibles
Hazards
Checkpoints
Goal
Spawn point
Background
```

Level loading should be deterministic.

If levels are stored in external files, validate their contents when loading.

Invalid level data should produce a useful error message rather than an obscure crash.

---

# 10. Enemies

Enemy behavior should be isolated from unrelated systems.

An enemy should have clearly defined:

* Position
* Velocity
* Health
* Collision behavior
* Movement behavior
* Damage behavior
* Death behavior

Enemy AI should be simple enough to test.

For example:

```text
Idle
→ Patrol
→ Detect player
→ Chase/attack
→ Return to patrol
```

Do not make enemy AI dependent on rendering.

---

# 11. Game States

Use explicit game states where appropriate.

Example:

```python
GameState.MENU
GameState.PLAYING
GameState.PAUSED
GameState.GAME_OVER
GameState.VICTORY
```

Avoid relying on scattered Boolean variables such as:

```python
is_menu
is_paused
is_dead
is_won
```

when a state machine would make the logic clearer.

---

# 12. Input Handling

Input should be separated from gameplay logic.

The player system should ideally receive actions such as:

```text
move_left
move_right
jump
attack
pause
```

rather than having every gameplay class directly inspect Pygame keyboard state.

This makes gameplay easier to test.

---

# 13. Assets

When adding assets:

* Keep assets organized.
* Use descriptive filenames.
* Avoid unnecessarily large files.
* Verify that referenced assets exist.
* Handle missing assets gracefully.
* Do not hardcode absolute paths.

Prefer project-relative paths.

Bad:

```python
"C:/Users/John/Desktop/game/player.png"
```

Good:

```python
Path("assets/images/player.png")
```

Use a centralized asset-loading system when practical.

---

# 14. Error Handling

Errors should be useful and actionable.

Bad:

```text
Error
```

Better:

```text
Failed to load player sprite:
assets/images/player.png
```

Do not silently swallow exceptions unless there is a specific reason.

Avoid:

```python
try:
    ...
except Exception:
    pass
```

---

# 15. Code Quality

Follow standard Python practices.

Use:

* Clear variable names
* Small functions
* Type hints where useful
* Docstrings for important public classes/functions
* Constants for configuration values
* Meaningful class names
* Consistent formatting

Avoid:

* Giant functions
* Global mutable state
* Unnecessary inheritance
* Duplicate logic
* Magic numbers
* Dead code
* Commented-out old implementations

---

# 16. Testing Philosophy

**Every meaningful gameplay feature should have tests.**

Testing must occur at multiple levels:

1. Unit testing
2. Integration testing
3. Game/system testing
4. Manual gameplay testing
5. Regression testing
6. Performance testing when relevant

The agent must not consider a feature complete simply because the code runs without a syntax error.

---

# 17. Unit Tests

Unit tests should test individual pieces of logic.

Examples:

```text
Player movement
Gravity
Jumping
Collision detection
Health
Damage
Enemy movement
Level loading
Score calculation
Game state transitions
```

Example:

```python
def test_player_lands_on_platform():
    ...
```

Tests should be deterministic.

Avoid unnecessary dependence on:

* Real-time delays
* Randomness
* Actual keyboard input
* Display hardware
* Audio hardware

---

# 18. Physics Tests

Physics tests should verify:

### Gravity

Verify that:

```text
player starts in air
→ gravity increases downward velocity
→ player moves downward
```

### Jumping

Verify:

```text
player on ground
→ jump
→ vertical velocity becomes upward
→ player rises
→ gravity reverses movement
→ player falls
→ player lands
```

### Movement

Verify:

```text
left input → player moves left
right input → player moves right
no input → player stops/decelerates as designed
```

### Frame-rate independence

When practical, verify that gameplay remains reasonably consistent with different `dt` values.

---

# 19. Collision Tests

At minimum test:

```text
Player vs floor
Player vs wall
Player vs ceiling
Player vs platform
Player falling through one-way platform
Player landing on moving platform
Enemy vs platform
Projectile vs enemy
Projectile vs wall
```

Tests should verify both position and state.

For example:

```python
assert player.is_on_ground
assert player.velocity_y == 0
```

---

# 20. Player Tests

Test:

```text
Player creation
Player movement
Player jumping
Player landing
Player taking damage
Player dying
Player respawning
Player health
Player invulnerability
Player attacking
Player animation state
```

Boundary conditions must also be tested.

Examples:

```text
0 health
1 health
maximum health
falling below level
jumping while airborne
moving against a wall
```

---

# 21. Enemy Tests

Test:

```text
Enemy creation
Enemy movement
Enemy patrol
Enemy detection
Enemy attack
Enemy taking damage
Enemy death
Enemy collision with player
```

Test edge cases such as:

```text
Enemy has 1 health
Enemy receives more damage than its health
Player leaves detection range
Enemy reaches edge of patrol area
```

---

# 22. Level Tests

Every level loader should be tested.

Verify:

```text
Level loads successfully
Player spawn exists
Required platforms exist
Enemies load correctly
Collectibles load correctly
Goal exists
Invalid level data is rejected
Missing assets produce useful errors
```

If the project has multiple levels, test each level's loading process.

---

# 23. Game State Tests

Test every state transition.

Example:

```text
MENU → PLAYING
PLAYING → PAUSED
PAUSED → PLAYING
PLAYING → GAME_OVER
GAME_OVER → MENU
PLAYING → VICTORY
```

Ensure that invalid state transitions are either prevented or handled intentionally.

---

# 24. Integration Tests

Integration tests should verify that systems work together.

Examples:

```text
Player + Physics
Player + Collision
Player + Enemy
Player + Level
Player + Camera
Level + Enemy spawning
Game state + UI
Game state + gameplay
```

Example scenario:

```text
Create level
→ spawn player
→ apply gravity
→ detect platform
→ resolve collision
→ verify player is standing
```

---

# 25. Regression Testing

Whenever a bug is fixed:

1. Reproduce the bug.
2. Create a test that fails because of the bug.
3. Fix the bug.
4. Verify the new test passes.
5. Run the entire test suite.

Do not fix a recurring bug without adding a regression test when practical.

---

# 26. Automated Test Commands

The project should use a standard test command.

Preferred:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_player.py
```

Run a specific test:

```bash
pytest tests/test_player.py::test_player_jump
```

Run with verbose output:

```bash
pytest -v
```

Run with coverage if configured:

```bash
pytest --cov=src
```

---

# 27. Linting

Run:

```bash
ruff check .
```

Fix all relevant lint errors before considering the task complete.

Do not blindly disable lint rules to make the check pass.

If a rule must be ignored, understand why and document the exception when appropriate.

---

# 28. Formatting

Run:

```bash
black .
```

or the project's configured formatter.

Code should remain consistently formatted.

Do not make unrelated formatting changes throughout the project.

---

# 29. Type Checking

If the project uses a type checker such as `mypy`, run:

```bash
mypy src
```

Fix type errors introduced by your changes.

Do not add meaningless `Any` types simply to silence the type checker.

---

# 30. Full Verification Procedure

Before declaring a significant feature complete, perform:

### Step 1 — Syntax/import check

```bash
python -m compileall .
```

### Step 2 — Unit tests

```bash
pytest
```

### Step 3 — Lint

```bash
ruff check .
```

### Step 4 — Formatting check

```bash
black --check .
```

### Step 5 — Type checking

If configured:

```bash
mypy src
```

### Step 6 — Launch the game

Run the project's normal game command.

For example:

```bash
python -m src.game.main
```

### Step 7 — Manual gameplay test

Actually interact with the game.

Test the feature in its intended context.

### Step 8 — Regression check

Verify that previously working functionality still works.

---

# 31. Manual Gameplay Testing

Automated tests are not sufficient for a graphical game.

For meaningful gameplay changes, manually verify:

## Startup

* Game launches.
* No unexpected errors appear.
* Window opens correctly.
* Assets load.

## Controls

* Movement works.
* Jump works.
* Attack works if applicable.
* Pause works.
* Menus respond correctly.

## Physics

* Player falls correctly.
* Player lands correctly.
* Player does not become stuck.
* Player does not pass through solid platforms.

## Camera

* Camera follows the player correctly.
* Camera does not move unexpectedly.
* Level boundaries behave correctly.

## Enemies

* Enemies spawn.
* Enemies move correctly.
* Enemy collisions work.
* Enemy death works.

## UI

* Health displays correctly.
* Score displays correctly.
* Menus display correctly.
* Game-over screen works.
* Victory screen works.

---

# 32. Edge Case Testing

Every significant feature should consider unusual inputs and states.

Examples:

```text
Player at level boundary
Player at maximum health
Player at zero health
Player jumps at edge of platform
Player presses jump repeatedly
Player moves against wall
Player falls indefinitely
Player dies during an attack
Enemy dies while attacking
Two enemies collide
Multiple enemies attack simultaneously
Game paused during movement
Game paused during attack
Level completed while taking damage
```

Do not only test the normal happy path.

---

# 33. Performance Testing

For larger levels or many entities, check:

* FPS
* CPU usage
* Memory usage
* Number of active entities
* Collision checks per frame
* Asset loading time

Avoid unnecessary per-frame work.

Do not repeatedly load images, sounds, or other assets inside the game loop.

Bad:

```python
while running:
    image = pygame.image.load("player.png")
```

Good:

```python
player_image = pygame.image.load("player.png")

while running:
    ...
```

---

# 34. Randomness

Random behavior must be controllable in tests.

Prefer dependency injection or seeded randomness.

Example:

```python
random.seed(12345)
```

Tests should not randomly pass or fail.

---

# 35. Deterministic Testing

Whenever possible:

* Use fixed input.
* Use controlled `dt`.
* Use fixed random seeds.
* Avoid unnecessary sleeps.
* Avoid relying on wall-clock time.
* Avoid requiring a visible window.

The same test should produce the same result repeatedly.

---

# 36. Pygame Testing

Tests should avoid opening a visible Pygame window unless a graphical integration test specifically requires it.

For headless testing, configure the environment appropriately.

Example:

```python
import os

os.environ["SDL_VIDEODRIVER"] = "dummy"
```

Initialize only the Pygame systems required by the test.

Always clean up resources after tests.

---

# 37. Test Naming

Use descriptive names.

Good:

```python
def test_player_lands_on_platform_after_falling():
    ...
```

Bad:

```python
def test_player():
    ...
```

Good:

```python
def test_enemy_dies_when_health_reaches_zero():
    ...
```

---

# 38. Test Organization

Keep tests organized by system.

Example:

```text
tests/
├── test_player.py
├── test_physics.py
├── test_collision.py
├── test_enemy.py
├── test_level.py
├── test_camera.py
├── test_game_state.py
└── test_integration.py
```

Do not place all tests in one enormous file.

---

# 39. Test Coverage

Aim for strong coverage of game logic.

Prioritize testing:

1. Physics
2. Collision
3. Player state
4. Enemy state
5. Level loading
6. Game state transitions
7. Save/load systems
8. Scoring
9. Inventory systems
10. Other deterministic gameplay systems

Visual effects do not necessarily require automated tests if their correctness is primarily visual.

---

# 40. Save Systems

If the game supports saving:

Test:

```text
Save game
Load game
Missing save
Corrupt save
Partial save data
New save
Overwrite save
Version compatibility
```

Never allow corrupt save data to silently destroy the player's progress.

---

# 41. Git Workflow

Before making significant changes:

```bash
git status
```

Review existing changes before modifying files.

Do not overwrite another developer's uncommitted work.

After making changes:

```bash
git diff
```

Review the changes.

Run tests before committing.

Recommended commit structure:

```text
feat: add player wall jumping
fix: correct enemy collision
test: add player physics tests
refactor: separate collision system
```

Avoid commits such as:

```text
stuff
changes
fixed things
update
```

---

# 42. Never Hide Problems

The agent must not:

* Delete failing tests to make the suite pass.
* Disable tests without explanation.
* Comment out broken code and claim success.
* Suppress errors unnecessarily.
* Ignore exceptions.
* Claim tests passed when they were not run.
* Claim the game was manually tested when it was not.
* Invent test results.

If something cannot be tested, explicitly state what could not be tested.

---

# 43. Debugging Procedure

When encountering a bug:

### 1. Reproduce

Determine exactly how the bug occurs.

### 2. Isolate

Identify the smallest system responsible.

### 3. Inspect

Read the relevant code and tests.

### 4. Create a failing test

Whenever practical, encode the bug as a regression test.

### 5. Fix

Make the smallest appropriate change.

### 6. Run the new test

Verify that the bug is fixed.

### 7. Run the full suite

Ensure no regressions occurred.

### 8. Manually verify

If the bug affects gameplay or visuals, play through the relevant scenario.

---

# 44. Feature Development Procedure

For every new feature:

```text
1. Understand the requested feature.
2. Inspect existing architecture.
3. Identify affected systems.
4. Design the smallest reasonable implementation.
5. Implement the feature.
6. Add/update automated tests.
7. Run focused tests.
8. Run the full test suite.
9. Run linting/formatting/type checks.
10. Launch the game.
11. Manually test the feature.
12. Test important edge cases.
13. Review git diff.
14. Report exactly what was tested.
```

---

# 45. Definition of Done

A feature is **not complete** until:

* [ ] Code is implemented.
* [ ] Existing architecture is respected.
* [ ] New logic has appropriate automated tests.
* [ ] Relevant tests pass.
* [ ] Full test suite passes.
* [ ] Linting passes.
* [ ] Formatting passes.
* [ ] Type checking passes if configured.
* [ ] Game launches successfully.
* [ ] Feature has been manually tested when appropriate.
* [ ] Important edge cases have been checked.
* [ ] No unrelated functionality was broken.
* [ ] Git diff has been reviewed.
* [ ] Documentation has been updated if necessary.

---

# 46. Agent Response Requirements

When completing a coding task, report:

### Changes Made

Briefly describe the files and systems changed.

### Tests Added

List tests that were created or modified.

### Tests Run

Example:

```text
pytest
ruff check .
black --check .
mypy src
```

### Manual Testing

State what was manually tested.

Example:

```text
Manually tested:
- Player movement
- Jumping
- Landing
- Wall collision
- Enemy collision
```

### Known Issues

Clearly identify anything that could not be tested or remains unresolved.

Never claim success without evidence.

---

# 47. Priority Order

When making engineering decisions, prioritize:

1. Correctness
2. Player safety from data loss
3. Testability
4. Maintainability
5. Performance
6. Simplicity
7. Visual polish

Do not sacrifice correctness or testability merely to make a feature faster to implement.

---

# 48. Minimalism

Do not introduce a dependency, framework, design pattern, abstraction, or system unless it provides a meaningful benefit.

For a small game, simple code is usually preferable to excessive architecture.

Avoid building systems for hypothetical future requirements.

Implement what the game actually needs.

---

# 49. Final Rule

The most important rule is:

> **Do not assume the game works. Prove it.**

When changing gameplay code, test the underlying logic automatically whenever possible, run the complete test suite, launch the game, manually verify the affected behavior, and report exactly what was tested.

If a test fails, investigate and fix the underlying problem rather than hiding the failure.

If something cannot be verified, say so clearly.
