```text
 ____                                        ____    ___                __      __      
/\  _`\                                     /\  _`\ /\_ \    __        /\ \    /\ \__   
\ \,\L\_\  _____      __      ___     __    \ \ \L\_\//\ \  /\_\     __\ \ \___\ \ ,_\  
 \/_\__ \ /\ '__`\  /'__`\   /'___\ /'__`\   \ \  _\/ \ \ \ \/\ \  /'_ `\ \  _ `\ \ \/  
   /\ \L\ \ \ \L\ \/\ \L\.\_/\ \__//\  __/    \ \ \/   \_\ \_\ \ \/\ \L\ \ \ \ \ \ \ \_ 
   \ `\____\ \ ,__/\ \__/.\_\ \____\ \____\    \ \_\   /\____\\ \_\ \____ \ \_\ \_\ \__\
    \/_____/\ \ \/  \/__/\/_/\/____/\/____/     \/_/   \/____/ \/_/\/___L\ \/_/\/_/\/__/
             \ \_\                                                   /\____/            
              \/_/                                                   \_/__/ 
===============================================================================
                                PROJECT PROFILE
===============================================================================

[!] RETRO PIPELINE STATUS: PRODUCTION MODERNIZATION STAGE
-------------------------------------------------------------------------------

Welcome to Space Flight, a classic 2D retro space arcade shooter.

This repository serves as a dedicated showcase of manual arcade layout design.
It has been fully modernized from its monolithic snapshot to demonstrate explicit
dependency injection, centralized routing, strict PEP 8 naming schemes, static
type safety, and a zero-global state architecture.

This structured setup prepares the combat models and coordinates for downstream
3D procedural voxel parsing inside the PyVorengi SDK pipeline.

===============================================================================
                              SYSTEM ENGINE SPEC
===============================================================================

* Core Runtime: Python 3.x
* Dependency:   Pygame-CE / Pygame (standard local desktop environment)
* Architecture: Centralized State-Router pattern, decoupled entity modules,
                Time-Delta physics scaling, direct-index mouse controls,
                pixel-perfect masks, file-based scoreboard, and parallax stars.

===============================================================================
                       TIME-DELTA & PHYSICS ARCHITECTURE
===============================================================================

To ensure visual consistency and high-performance physics across all modern
desktop environments, this engine implements three core structural upgrades:

* Time-Delta Scaling (dt):
  Traditional games tie their movement speeds directly to how fast the computer
  draws graphics. If the system experiences lag, the gameplay runs in slow 
  motion; if the screen has a high refresh rate, it runs at double speed. 
  Space Flight resolves this using "Time-Delta" scaling. By calculating the 
  exact fraction of a second that elapsed between frames (`dt`) and scaling 
  all motion and animation frames by it, ship and projectile speeds remain 
  perfectly uniform whether rendering at 30 FPS, 60 FPS, or 144 FPS.

* Index-Direct Mouse Handling:
  Pygame returns mouse button states as a coordinate list. Newer frameworks 
  (like Pygame-CE) support extended gaming mice with 5 buttons, while older 
  versions only return 3. By evaluating click states via explicit index checks
  (e.g., checking index `0` directly for left-click) instead of matching exact
  list sizes, the user interface remains immune to button-count mismatches
  across different systems and runtimes.

* Timeline Millisecond Spawning:
  Instead of relying on the operating system's background event queue (which
  can drop spawning signals when the processor is busy), the game schedules 
  spawning delays as precise timestamps on a master timeline. By comparing 
  the CPU's clock directly against these timeline thresholds, combat hazards
  spawn smoothly and reliably without losing events.

===============================================================================
                             ROBUST LAUNCH SYSTEM
===============================================================================

File resolution is fully resolved relative to the file-structure of the package.
You can execute the entry point from any working terminal directory:

$ python main.py

===============================================================================
                                GAME CONTROLS
===============================================================================

* Movement (Mouse Mode - Default):
  -> Hover / Move:   Track mouse coordinate mapping
  -> Toggle Mode:    Press [M] to activate Mouse Mode
  -> Cursor Capture: The mouse cursor is captured, bound, and clamped strictly 
                     inside the ship's flight corridor during combat. This 
                     completely prevents coordinate drift when hitting edge
                     limits. Press [ESC] to pause and release the cursor.

* Movement (Keyboard Mode):
  -> Arrow Keys:     [Up] / [Down] / [Left] / [Right]
  -> Toggle Mode:    Press [K] to activate Keyboard Mode

* Combat:
  -> Primary Fire:   [Spacebar] or [Left Click] (Consumes Energy)
  
* Game State:
  -> Pause Game:     Press [ESC] (Locks/Unlocks inputs automatically)
  -> Resume/Exit:    Use the interactive back button or close the window

===============================================================================
                               SYSTEM PERSISTENCE
===============================================================================

High scores are organized across three discrete directories:
* Easy:   `highscores/easy scores.txt`   & `highscores/easy names.txt`
* Medium: `highscores/medium scores.txt` & `highscores/medium names.txt`
* Hard:   `highscores/hard scores.txt`   & `highscores/hard names.txt`

The file-handling systems in `Game` automatically generate these directories
and base templates if they are missing or corrupted on startup.

===============================================================================
                         CONFIGURATION & SETTINGS MANUAL
===============================================================================

The configuration variables declared in `src/settings.py` control the core
rendering, game-loop mechanics, and physics progression curves:

* `SCREEN_WIDTH` / `SCREEN_HEIGHT` (800 x 800)
  Defines the logical screen space boundary. All entities utilize this box
  for coordinate clamp checks and viewport wrap/kill checks.

* `FPS` (60)
  Controls the target rendering limit and synchronizes timing loops.

* Difficulty Score Thresholds (`DIFFICULTY_EASY` / `MEDIUM` / `HARD`)
  These settings values act as the baseline triggers for the physical
  speed-progression curve of the simulation.

--- DIFFICULTY ACCELERATION MECHANICS ---

The game speed scaling ratio (`game_speed`) is directly connected to the active
difficulty threshold and the player's current session score. 

The scaling calculation is evaluated as follows during the update loop:
`self.game_speed = 1.0 + (self.score / self.difficulty) / 25.0`

This creates the following progressive relationships:
1. Trigger Point: Acceleration only triggers once the score exceeds the active
   difficulty setting. On HARD (200), acceleration starts almost immediately,
   whereas on EASY (1000), it remains at a static 1.0 pace for much longer.
2. Progression Steepness: Because the chosen difficulty setting acts as the
   mathematical divisor, a lower value (e.g., HARD = 200) causes the speed
   multiplier to increase exponentially faster per point scored.
   * On HARD (200): Dividing by 200 * 25 (5000) causes the speed to ramp up
     significantly faster.
   * On EASY (1000): Dividing by 1000 * 25 (25000) results in a highly
     gradual, forgiving speed-increase curve.

===============================================================================
                             ROADMAP & OPTIMIZATION
===============================================================================

The modern architectural refactoring milestones have been completed:

[x] Zero-Global Refactoring: State variables and sprite groups are inside Game.
[x] Absolute Layouts: Centralized state routing and drawing systems.
[x] Static Type Safety: Rigorous Python type hints integrated on all classes.
[x] Modular Organization: Decoupled into src/entities/ and src/screens/.
[x] Delta-Time & Frame-rate Independence: Fully integrated physics clock.
[ ] PyVorengi SDK Integration: Bridge this space combat model as a direct,
    procedurally parsed 3D entity pipeline inside the PyVorengi voxel engine.