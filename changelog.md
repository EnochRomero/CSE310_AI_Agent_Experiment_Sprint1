# Changelog

## 2026-10-02 - Initial playable game

### Process

1. Read the workspace's `AGENTS.md` requirements: use Python/Pygame for the 2D platformer, keep gameplay code understandable, add deterministic tests, and document what was verified.
2. Checked the workspace. It initially contained only `AGENTS.md`; there was no existing game code or Git repository to build on.
3. Checked the Python runtime: Python 3.11.9 was available. Pygame was not installed at the start, so the project declares it in `requirements.txt` and the run instructions install it before launch.
4. Added a small platform-jumping game, setup/run instructions, and built-in `unittest` tests for landing and jumping behavior.
5. Installed the declared Pygame dependency in the configured Python 3.11 environment after the first test attempt confirmed it was missing.
6. Ran the focused physics tests, then exercised the actual game startup and one draw-loop iteration using Pygame's dummy video driver.
7. Checked the edited Python files for editor diagnostics; none were reported.

### Files added

- `game.py`: game loop, player movement and collisions, level layout, drawing, controls, and restart.
- `tests/test_game.py`: focused tests for landing, jumping after landing, and preventing an airborne jump.
- `requirements.txt`: Pygame runtime dependency.
- `README.md`: install, run, controls, and test commands.
- `software_infrastructure.txt`: ASCII overview of runtime components, frame flow, project files, and test flow.

### Verification

- `python -m unittest discover -s tests -v`: passed, 3 tests.
- Headless game startup/draw-loop smoke check: passed.
- Python editor diagnostics: no errors found.
- Manual visual gameplay was not performed; the launch check used a dummy display driver.
- Pygame emitted a `pkg_resources` deprecation warning from its installed package; it did not affect the tests or launch check.

## 2026-10-02 - Endless scrolling world

### Changes

- Removed the player's screen-edge clamp so the world position can continue in either horizontal direction.
- Added `PlatformWorld`, which deterministically generates ground and raised platforms in 600-pixel chunks around the camera. Chunks well outside the camera's working range are removed from memory and can be generated again when revisited.
- Changed rendering to follow the player with a horizontal camera and draw world platforms at camera-adjusted screen positions.
- Replaced the fixed star-goal level with open-ended exploration through generated terrain.
- Updated the README, this changelog, and `software_infrastructure.txt` to describe the scrolling world and generation flow.
- Added tests for leftward world travel and platform generation to both the left and right.

### Verification

- `python -m unittest discover -s tests -v`: passed, 5 tests.
- Headless startup and draw-loop smoke check: passed with the generated world and scrolling camera.
- Python editor diagnostics: no errors found in the game and test files.
- Manual visual gameplay was not performed; the startup check used Pygame's dummy display driver.
- Pygame emitted its existing `pkg_resources` deprecation warning; it did not affect tests or startup.

## 2026-10-02 - Patrolling enemy and sprite details

### Changes

- Added one enemy to each generated world chunk. Enemies patrol between chunk-local boundaries and are removed when stomped from above; side contact blocks player movement.
- Reworked each generated chunk to contain both platforms and its enemy, preserving deterministic generation as chunks are revisited.
- Replaced the plain player rectangle with a layered sprite drawn from Pygame shapes, and added a spiked enemy sprite with eyes and directional pupils.
- Updated control guidance, the software infrastructure diagram, and this changelog.
- Added tests for enemy patrol bounds, stomp behavior, and enemy presence in generated chunks.

### Verification

- `python -m unittest discover -s tests -v`: passed, 7 tests.
- Headless startup and sprite-render smoke check: passed with generated enemies.
- Python editor diagnostics: no errors found in the game and test files.
- Manual visual gameplay was not performed; the startup check used Pygame's dummy display driver.
- Pygame emitted its existing `pkg_resources` deprecation warning; it did not affect tests or startup.

## 2026-10-02 - Side-hit death screen

### Changes

- Made enemy collision outcomes explicit: stomping defeats the enemy, while side contact is a fatal hit.
- Added a game-over overlay showing the cause and controls to restart with **R** or quit with **Esc**. Gameplay and enemies pause until restart.
- Updated the README and software infrastructure diagram to reflect death and restart flow.
- Added a regression test for side contact while preserving the stomp test.

### Verification

- `python -m unittest discover -s tests -v`: passed, 8 tests.
- Headless game-loop smoke check triggered a side collision and rendered the death overlay successfully.
- Python editor diagnostics: no errors found in the game and test files.
- Manual visual gameplay was not performed; the death-screen check used Pygame's dummy display driver.
- Pygame emitted its existing `pkg_resources` deprecation warning; it did not affect tests or startup.