```text
 ____                                        ______  ___                __      __      
/\  _`\                                     /\  ___\/\_ \    __        /\ \    /\ \__   
\ \,\L\_\  _____      __      ___     __    \ \ \__/\//\ \  /\_\     __\ \ \___\ \ ,_\  
 \/_\__ \ /\ '__`\  /'__`\   /'___\ /'__`\   \ \ ,__\ \ \ \ \/\ \  /'_ `\ \  _ `\ \ \/  
   /\ \L\ \ \ \L\ \/\ \L\.\_/\ \__//\  __/    \ \ \_/  \_\ \_\ \ \/\ \L\ \ \ \ \ \ \ \_ 
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

This repository serves as a showcase of manual arcade layout design.
It has been fully modernized from its monolithic snapshot to demonstrate
explicit dependency injection, centralized routing, strict PEP 8 naming schemes,
static type safety, and a zero-global state architecture.

The code features an optimized, dynamic scaling physics loop that unifies
projectile speeds, weapon fire rates, item drop frequencies, spawning delays,
and mechanical movement speeds on smooth, dampened curves to provide an
engaging, responsive retro combat experience.

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
  uniform whether rendering at 30 FPS, 60 FPS, or 144 FPS.

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
                       WEB-SAFE AUDIO & MIXER ARCHITECTURE
===============================================================================

To ensure reliable audio playback across both native desktop engines and
sandboxed WebAssembly browser environments, the sound systems implement
two key upgrades:

* Web-Safe Autoplay Context Unlocker:
  Modern web browsers aggressively block web applications from playing audio
  before the user has explicitly interacted with the page. To prevent the audio
  mixer context from crashing or running in silent mode when compiled to Web-
  Assembly and hosted on itch.io, the engine defers starting the menu music
  until the first mouse click or keypress is registered in the event queue.

* Channel Saturation Guard (SafeSound):
  In intense combat scenarios, multiple explosion and laser effects can trigger
  simultaneously, leading to audio channel saturation and volume clipping. The
  sound system wraps native mixer objects in a guard class that dynamically caps
  concurrent overlapping playback requests to safe channel thresholds.

===============================================================================
                             ROBUST LAUNCH SYSTEM
===============================================================================

File resolution is fully resolved relative to the file-structure of the
package. You can execute the entry point from any working terminal directory:

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
                    GLOBAL SPEED & TRANSITION STATE RESETS
===============================================================================

To prevent persistent variables from leaking between combat and menu
transitions, the game implements unified resets:

* Game Speed Multiplier:
  Automatically restored to its baseline value of 1.0 immediately 
  upon player death.

* Centrally Isolated Score & Name:
  Scores and name buffers are preserved during highscore submission 
  but reset centrally upon entering the menu transition.

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

* `SHOW_FPS` (True)
  Toggles the real-time diagnostic performance overlay.

* Difficulty Score Thresholds (`DIFFICULTY_EASY` / `MEDIUM` / `HARD`)
  These settings values act as the baseline triggers for the physical
  speed-progression curve of the simulation.

* `BASE_GAME_SPEED_SCALING_DAMPENER` (1.0)
  Controls the dampening curve applied to the core gameplay physics and
  spawning loops (renamed from `SCALING_DAMPENER`).

* `KEYBOARD_MOVE_SPEED_SCALING_DAMPENER` (5.0)
  Dampens player ship manual keyboard movement scaling independent of raw
  game speed acceleration, keeping controls comfortable.

* `BASE_ENEMY_SPEED_X_MIN` / `BASE_ENEMY_SPEED_X_MAX` (180.0 / 360.0)
  Configures the base horizontal movement boundaries for enemy UFOs.

* `BASE_ENEMY_SPEED_Y` (60.0)
  Sets the base downward vertical speed for enemy UFOs.

* `BASE_ENEMY_LASER_LOCK_MIN` / `BASE_ENEMY_LASER_LOCK_MAX` (2.0 / 4.0)
  Establishes the minimum and maximum initial target alignment times for
  enemy weapon cooldowns (corrected from OCK).

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
                 UNIFIED DYNAMIC SCALING & GAMEPLAY PHYSICS
===============================================================================

Rather than scaling gameplay speeds directly in a linear fashion—which would
make projectiles blindingly fast, deplete player fuel instantly, and crowd the
screen with entities—the engine runs a unified, dampened mathematical scaling
loop.

All real-time velocity, weapon fire rate, item drop frequency, and spawning
pacing are governed by a central, dynamic Scaling Multiplier (Sm) calculated
as follows:

scaling_factor = (BASE_GAME_SPEED_SCALING_DAMPENER + game_speed) / \
                 (BASE_GAME_SPEED_SCALING_DAMPENER + INITIAL_GAME_SPEED)

This coefficient acts as a mathematical "shock absorber." By adjusting the
dampener values in your settings, you can flatten or sharpen the difficulty
acceleration curve to prevent extreme speed spikes while keeping gameplay
tense.

This Scaling Multiplier controls the following systems in tandem:

* Symmetrical Enemy Targeting:
  Instead of checking offsets from one side of your ship, the targeting system
  now checks if the enemy's center (line of fire) points anywhere inside the
  player's horizontal boundaries. When the relative speed is low, the enemy
  fires directly. If the speed is high, it automatically calculates a
  predictive offset (using relative velocity) to lead its shots, preventing
  "lazy" stationary gameplay.

* Dampened Projectile Velocities (Player & Enemy):
  Both player and enemy lasers increase their travel speed as the game speed
  rises, but they do so on a smoothed curve. This keeps projectiles highly
  visible, dodgeable, and fair even when flying at maximum score velocities.

* Energy-Saving Laser Cost:
  As the player's firing rate accelerates at higher difficulties, holding down
  constant fire would normally empty the energy bar in seconds. To balance
  this, each shot's energy cost is divided by a customized dampening factor:

  Cost per Shot = BASE_PLAYER_LASER_COST / \
                  (1.0 + (scaling_factor - 1.0) * ENERGY_SAVING_FACTOR)

  By tuning the ENERGY_SAVING_FACTOR (from 0.0 to 1.0) in your settings, you
  can smoothly cushion this drain. At a value of 0.5, the rate of fuel drain
  per second rises only moderately, preserving the classic arcade pressure
  without crippling your offensive capabilities.

* Star Background & Powerup Fall Acceleration:
  Distant stars and falling powerup items scroll faster as your score climbs,
  using our dampened Scaling Multiplier. This keeps your visual forward
  acceleration and item pickups perfectly in sync with combat pacing while
  preventing powerups from feeling visually "heavy" or slow relative to stars.

* Adaptive Hazard Speeds:
  Tumbling space asteroids scale their vertical and horizontal velocities
  based on our uniform multiplier. At high scores, they remain fast and
  challenging but always physically reactable, avoiding impossible
  "instant-spawn" deaths.

* Adaptive Spawning Frequencies (Enemies, Obstacles & Drops):
  Spawning rates for support items, hostile enemies, and space rocks scale
  dynamically on a dampened curve rather than scaling linearly. This prevents
  excessive screen congestion at high speeds while ensuring that helpful items
  and challenges appear reliably as the pacing accelerates.

* Dampened Keyboard Handling:
  To prevent keyboard controls from becoming unplayable during high-velocity
  runs, translation speeds dynamically adjust using a dedicated dampener
  parameter (KEYBOARD_MOVE_SPEED_SCALING_DAMPENER), ensuring responsive and
  reliable manual maneuvering.

===============================================================================
                             ROADMAP & OPTIMIZATION
===============================================================================

The modern architectural refactoring milestones have been completed:

[x] Zero-Global Refactoring: State variables and sprite groups are inside Game.
[x] Absolute Layouts: Centralized state routing and drawing systems.
[x] Static Type Safety: Rigorous Python type hints integrated on all classes.
[x] Modular Organization: Decoupled into src/entities/ and src/screens/.
[x] Delta-Time & Frame-rate Independence: Fully integrated physics clock.
[x] Dynamic Score Caching: Optimizes score drawing by caching text surfaces.
    Instead of regenerating the text on every frame (a common CPU bottleneck
    in Pygame), the engine only re-draws the scoreboard when your score actually
    changes, resulting in dramatic CPU savings and consistent frame delivery.
[x] Centralized Asset Pre-Caching: Startup loading, alpha-converting, scaling,
    and mask pre-calculation. Completely eliminates on-the-fly disk reads and
    CPU collision mask compilation, ensuring stable, fluid frame pacing.
[x] Symmetrical Lead-Aim Targeting: Corrected enemy horizontal firing logic to
    resolve un-reactable "fly-overs" and support relative targeting.
[x] Unified Dynamic Scaling Loop: Integrated dynamic math scaling across player
    and enemy laser speeds, firing delays, powerup drops and falls, background
    stars, keyboard movement, and enemy/obstacle spawn rates.

===============================================================================
Distributed under the MIT License. Copyright (c) 2026 herbal1st.