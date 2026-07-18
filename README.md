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

[!] RETRO PIPELINE STATUS: LEGACY VERIFICATION PRE-ALPHA (UNASSISTED)
-------------------------------------------------------------------------------

Welcome to Space Flight, a classic 2D retro space arcade shooter.

This repository serves as a dedicated archive showcasing the project's original
unassisted codebase. Built entirely from scratch years ago before utilizing AI
assistants, this release captures a foundational snapshot of manual 
architecture, direct event loops, and custom logic in Python and Pygame.

An optimized, PEP 8 compliant, type-safe, and fully modularized version will
follow in future updates as we prepare this codebase for downstream 3D Voxel
integration.

===============================================================================
                              SYSTEM ENGINE SPEC
===============================================================================

* Core Runtime: Python 3.x
* Dependency:   Pygame-CE / Pygame (standard)
* Architecture: Monolithic direct game execution, sprite-driven states,
                pixel-perfect masks, file-based scoreboard, and parallax stars.

===============================================================================
                             CRITICAL INITIALIZATION
===============================================================================

Due to legacy hardcoded path resolving (`os.getcwd()`), the game expects to
evaluate its working directory directly at the repository root.

[!] IMPORTANT LAUNCH INSTRUCTION:
    To run the game without file-not-found crashes, navigate your terminal
    directly into the root folder containing `main.py` before executing:

    $ python main.py

===============================================================================
                                GAME CONTROLS
===============================================================================

* Movement (Mouse Mode - Default):
  -> Hover / Move:   Track mouse coordinate mapping
  -> Toggle Mode:    Press [M] to activate Mouse Mode

* Movement (Keyboard Mode):
  -> Arrow Keys:     [Up] / [Down] / [Left] / [Right]
  -> Toggle Mode:    Press [K] to activate Keyboard Mode

* Combat:
  -> Primary Fire:   [Spacebar] or [Left Click] (Consumes Energy)
  
* Game State:
  -> Pause Game:     Press [ESC]
  -> Resume/Exit:    Use the interactive back button or close the window

===============================================================================
                               SYSTEM PERSISTENCE
===============================================================================

High scores are organized across three discrete directories:
* Easy:   `highscores/easy scores.txt`   & `highscores/easy names.txt`
* Medium: `highscores/medium scores.txt` & `highscores/medium names.txt`
* Hard:   `highscores/hard scores.txt`   & `highscores/hard names.txt`

[!] NOTE: If these flat-files are missing or corrupted, path execution errors
          will trigger immediately on state change. Keep them intact.

===============================================================================
                             ROADMAP & OPTIMIZATION
===============================================================================

Our next iteration aims to refactor this repository to reflect modern production
standards, improving structural separation of concerns:

[ ] Zero-Global Refactoring: Transition away from global state pools.
[ ] Absolute Layouts: Implement relative box containers over magic coordinates.
[ ] Static Type Safety: Add rigorous Python type hints to all classes/methods.
[ ] Modular Organization: Break the massive monolithic module into structured,
    implicit namespace components (e.g. gameplay, assets, mechanics, engines).
[ ] PyVorengi SDK Integration: Bridge this space combat model as a direct,
    procedurally parsed 3D entity pipeline inside the PyVorengi voxel engine.