# SpacePilot

**SpacePilot** is a 2D idle-style space game originally written in Python. The goal is to navigate through space while collecting dark matter and golden orbs, boosting speed, and surviving random cosmic events.

## Game Overview

- The spaceship is made of **6 modular parts**, randomly assembled on game start:
  - Top Engine
  - Top Storage
  - Cabin
  - Bottom Engine
  - Bottom Storage
  - Weapon

- The ship flies through a **scrolling starfield** with motion blur trails.

- Players collect:
  - **Dark Matter** (M): Increases score
  - **Gold Orbs** (G): Rare collectible

- A **boost mechanic** temporarily increases speed, changes the flame animation, and enables full star blur.

- The HUD displays the player's resource totals and active boost timer.

- **Random Events** appear periodically with 1–3 button choices (e.g., explore a planet, repair the ship, take damage).

## Planned Port to Web

This version is being rebuilt from scratch in **JavaScript with Phaser.js**, designed to run directly in the browser.

### Key Features to Rebuild:
- Sprite-based modular ship
- Scrolling starfield background
- Orbs that animate toward the ship
- Boost button that alters game state
- Animated HUD (score + boost time)
- Random events (story-driven or interactive)

## Current State

This repo contains the original Python version of the game (using pygame or st7789/PIL). The port to JavaScript is in progress.

## Assets

All sprite assets are located in the `/sprites` folder and are used to build ships, orbs, and effects. These will be reused or converted for the Phaser.js version.

---

