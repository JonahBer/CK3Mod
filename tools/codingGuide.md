# Crusader Kings III Modding Guide

This guide explains how to build **standalone** CK3 mods.

## Table of Contents

1. [Mod Setup and Structure](#1-mod-setup-and-structure)
2. [Common Folder — Overview](#2-common-folder--overview)
3. [Decisions](#3-decisions)
4. [Character Interactions](#4-character-interactions)
5. [Traits](#5-traits)
6. [Modifiers](#6-modifiers)
7. [Script Values](#7-script-values)
8. [Scripted Triggers](#8-scripted-triggers)
9. [Scripted Effects](#9-scripted-effects)
10. [Scripted Modifiers](#10-scripted-modifiers)
11. [Events](#11-events)
12. [On Actions (Pulses and Random Events)](#12-on-actions-pulses-and-random-events)
13. [Game Rules](#13-game-rules)
14. [Opinion Modifiers](#14-opinion-modifiers)
15. [Scripted Relations](#15-scripted-relations)
16. [Effect Localization](#16-effect-localization)
17. [Trigger Localization](#17-trigger-localization)
18. [Customizable Localization](#18-customizable-localization)
19. [Messages (Toasts / Notifications)](#19-messages-toasts--notifications)
20. [Localization](#20-localization)
21. [Religion Doctrines](#21-religion-doctrines)
22. [Scripted GUIs](#22-scripted-guis)
23. [Naming and Compatibility](#23-naming-and-compatibility-standalone-mods)
24. [Minimal Standalone Mod Checklist](#24-minimal-standalone-mod-checklist)
25. [Variables (declare, persistent, retrieve)](#25-variables-declare-persistent-retrieve)
26. [Lists / arrays](#26-lists--arrays)
27. [Character interactions and editing (examples)](#27-character-interactions-and-editing-examples)
28. [Custom windows and opening UI](#28-custom-windows-and-opening-ui)

This guide is based on the structure and patterns used in the Carnalitas example mod, but applies to any mod that does not depend on Carnalitas. Use it as a reference for folder layout, file formats, and scripting.

---

## 1. Mod Setup and Structure

### 1.1 Two Required Files

Every mod needs:

1. **`descriptor.mod`** — Inside the mod folder. Defines the mod for the game.
2. **`YourModName.mod`** — In the game’s `mod/` folder (same level as your mod folder). Tells the launcher where the mod lives.

**`descriptor.mod`** (inside `mod/YourModName/`):

```plaintext
version="1.0"
tags={
	"Gameplay"
	"Events"
}
name="Your Mod Name"
supported_version="1.18.*"
```

- **version** — Your mod version (string).
- **tags** — Launcher categories (Gameplay, Events, Character Interactions, etc.).
- **name** — Display name in the launcher.
- **supported_version** — CK3 version; `1.18.*` means any 1.18.x.

**`YourModName.mod`** (in `mod/`, next to the folder):

```plaintext
version="1.0"
tags={
	"Gameplay"
	"Events"
}
name="Your Mod Name"
supported_version="1.18.*"
path="mod/YourModName"
```

The only extra field is **path**: the folder name under `mod/` where your files live.

### 1.2 Folder Structure

Typical layout:

```plaintext
YourModName/
├── descriptor.mod
├── common/           # Game data: traits, decisions, modifiers, scripts
├── events/           # Event files (.txt)
├── gfx/              # Textures, icons (e.g. .dds)
├── gui/              # UI overrides (.gui)
└── localization/     # All text (.yml per language)
	├── english/
	├── french/
	└── ...
```

- **common/** — Most gameplay content: decisions, traits, modifiers, scripted triggers/effects, on_actions, etc.
- **events/** — Event definitions; referenced by ID (e.g. `namespace.id`).
- **localization/** — One folder per language; files use `l_english`, `l_french`, etc.

---

## 2. Common Folder — Overview

Everything under `common/` is data and script logic. Subfolders are fixed names the game expects.

| Subfolder | Purpose |
|-----------|--------|
| `decisions/` | Decisions (e.g. “Start birth control”) |
| `character_interactions/` | Right‑click / character interactions |
| `traits/` | Character traits |
| `modifiers/` | Character/county/etc. modifiers |
| `scripted_triggers/` | Reusable trigger blocks |
| `scripted_effects/` | Reusable effect blocks |
| `script_values/` | Named numeric values (for cooldowns, costs, etc.) |
| `on_action/` | When to fire events (pulses, random events) |
| `game_rules/` | Game rules (options in the lobby) |
| `opinion_modifiers/` | Opinion modifier types |
| `hook_types/` | Hook definitions |
| `scripted_relations/` | Custom relation types (e.g. slave / owner) |
| `scripted_modifiers/` | Dynamic modifier calculations |
| `scripted_guis/` | When/how to show GUI elements |
| `religion/doctrines/` | Faith doctrines |
| `culture/traditions/` | Culture traditions |
| `schemes/scheme_types/` | Scheme type overrides/additions |
| `messages/` | Message types for toasts/notifications |
| `important_actions/` | Important action definitions |
| `effect_localization/` | Text for scripted effects (e.g. relations) |
| `trigger_localization/` | Text for scripted triggers |
| `customizable_localization/` | Conditional text (e.g. by trigger) |
| `modifier_definition_formats/` | How modifier values are displayed |
| `game_concepts/` | Game concept icons/aliases for tooltips |
| `character_memory_types/` | Memory types (for secrets, etc.) |

You only need the folders you use. Below we go through the main ones.

---

## 3. Decisions

**Path:** `common/decisions/your_decisions.txt`

```plaintext
my_start_thing_decision = {
	ai_check_interval = 0
	picture = {
		reference = "gfx/interface/illustrations/decisions/decision_my_thing.dds"
	}

	desc = my_start_thing_decision_desc
	selection_tooltip = my_start_thing_decision_tooltip

	is_shown = {
		is_adult = yes
		NOT = { has_character_modifier = my_thing_modifier }
	}

	is_valid_showing_failures_only = {
		# Optional: extra checks that show failure reasons
	}

	effect = {
		send_interface_toast = {
			type = event_toast_effect_neutral
			title = msg_my_thing_started
			left_icon = root
			add_character_modifier = my_thing_modifier
		}
		trigger_event = { on_action = my_on_decision_used }
	}

	ai_potential = {
		always = no
	}

	ai_will_do = {
		base = 0
	}
}
```

- **root** — The character taking the decision.
- **is_shown** — When the decision appears in the list.
- **is_valid_showing_failures_only** — When it’s clickable; failures are shown in tooltip.
- **effect** — What happens when taken.
- **ai_potential** / **ai_will_do** — AI behavior; `always = no` and `base = 0` = player only.

All `desc`, `selection_tooltip`, `title`, etc. are localization keys (see **Localization**).

---

## 4. Character Interactions

**Path:** `common/character_interactions/your_interactions.txt`

Interactions appear when right‑clicking a character (e.g. “Have sex”, “Enslave”).

```plaintext
my_interaction = {
	category = interaction_category_friendly
	desc = my_interaction_desc
	interface_priority = 40
	use_diplomatic_range = no

	is_shown = {
		scope:actor = { is_adult = yes }
		scope:recipient = { is_adult = yes }
		NOT = { scope:actor = scope:recipient }
	}

	cooldown = { months = my_interaction_cooldown }

	is_valid_showing_failures_only = {
		scope:actor = { gold >= 50 }
	}

	on_accept = {
		scope:actor = {
			pay_gold = 50
			# effects; scope:recipient is the target
		}
	}
}
```

- **scope:actor** — Character who initiates (the one right‑clicking).
- **scope:recipient** — Character being clicked.
- **cooldown** — Uses a script value from `script_values/` (e.g. `months = my_interaction_cooldown`).
- **on_accept** — Runs when the player (or AI) confirms.

---

## 5. Traits

**Path:** `common/traits/your_traits.txt`

```plaintext
my_trait = {
	name = trait_my_trait
	desc = trait_my_trait_desc
	group = my_trait_group
	level = 1

	genetic = no
	physical = no
	good = yes

	birth = 0
	random_creation = 0
	ruler_designer_cost = 0

	opposites = { other_trait }
}
```

- **name** / **desc** — Localization keys.
- **group** / **level** — For grouping and tier (e.g. beauty_1, beauty_2).
- **genetic** — Can be inherited.
- **physical** — Shown on body/portrait.
- **good** — Positive trait for AI/opinion.
- **opposites** — Mutually exclusive traits.

Traits can use **triggered_desc** and **first_valid** for dynamic text (e.g. by game rule or scope).

---

## 6. Modifiers

**Path:** `common/modifiers/your_modifiers.txt`

```plaintext
my_thing_modifier = {
	icon = fertility_positive
	fertility = -1.0
	monthly_income = -0.1
	monthly_piety = -0.05
}
```

Modifiers are referenced by ID (e.g. `add_character_modifier = my_thing_modifier`). You can add duration in the effect: `add_character_modifier = { name = my_thing_modifier months = 12 }`.

**Path:** `common/modifier_definition_formats/your_formats.txt` — Controls how values appear in tooltips (e.g. percent, decimals).

---

## 7. Script Values

**Path:** `common/script_values/your_values.txt`

Used for cooldowns, costs, and other numbers in decisions/interactions/events.

```plaintext
my_cooldown_base = {
	value = 12
}

my_interaction_cooldown = {
	value = my_cooldown_base
	if = {
		limit = { has_game_rule = my_no_cooldown_rule }
		multiply = 0
	}
}
```

Then in an interaction: `cooldown = { months = my_interaction_cooldown }`.

---

## 8. Scripted Triggers

**Path:** `common/scripted_triggers/your_triggers.txt`

Reusable trigger blocks. No scope change unless you use `$PARAM$` or scopes inside.

```plaintext
my_can_do_thing_trigger = {
	OR = {
		is_consort_of = $PARTNER$
		has_relation_lover = $PARTNER$
		has_relation_soulmate = $PARTNER$
	}
}
```

Usage: `my_can_do_thing_trigger = { PARTNER = scope:recipient }`. The trigger runs in the current scope (e.g. `scope:actor`); `$PARTNER$` is the passed scope.

---

## 9. Scripted Effects

**Path:** `common/scripted_effects/your_effects.txt`

Reusable effect blocks. Use **$PARAM$** for scope parameters.

```plaintext
my_do_thing_effect = {
	$ACTOR$ = { save_temporary_scope_as = actor_ref }
	$TARGET$ = { save_temporary_scope_as = target_ref }

	scope:actor_ref = {
		add_gold = 100
	}
	scope:target_ref = {
		add_opinion_modifier = {
			target = scope:actor_ref
			modifier = my_opinion_modifier
		}
	}
}
```

Call with: `my_do_thing_effect = { ACTOR = scope:actor TARGET = scope:recipient }`.

Use **hidden_effect** for effects that must run but should not appear in the tooltip.

---

## 10. Scripted Modifiers

**Path:** `common/scripted_modifiers/your_modifiers.txt`

Dynamic modifiers (e.g. chance or stat that depends on traits, culture, etc.).

```plaintext
my_rank_up_chance_modifier = {
	modifier = {
		factor = 1.0
		has_trait = lustful
	}
	modifier = {
		factor = 0.9
		has_trait = chaste
	}
	modifier = {
		factor = 2
		effective_age <= 21
	}
}
```

Used in events/effects where a **weight_multiplier** or similar expects a scripted modifier.

---

## 11. Events

**Path:** `events/your_events.txt`

### 11.1 Namespace and IDs

```plaintext
namespace = my_events

my_events.1 = {
	# event content
}
```

Event ID is **namespace + number** (e.g. `my_events.1`). Refer to it as `my_events.1` in on_actions and elsewhere.

### 11.2 Basic Event Structure

```plaintext
my_events.1 = {
	type = character_event
	title = my_events.1.t
	desc = my_events.1.desc
	theme = default

	trigger = {
		is_alive = yes
		is_adult = yes
	}

	immediate = {
		# Runs as soon as the event fires (no player choice)
	}

	option = {
		name = my_events.1.a
		trigger = { }   # Optional: when this option is available
		# effects when this option is chosen
	}

	option = {
		name = my_events.1.b
		# effects
	}
}
```

- **trigger** — Event is only considered if this is true (for the event’s recipient/scope).
- **immediate** — Runs before options are shown.
- **option** — Buttons the player (or AI) can pick; each has **name** (localization key) and effects.

### 11.3 Hidden Events

No popup; used for background logic (e.g. yearly pulse, cleanup):

```plaintext
my_events.2 = {
	hidden = yes
	trigger = {
		has_character_modifier = my_thing_modifier
	}
	immediate = {
		add_stress = { value = minor_stress_impact_loss multiply = -1 }
	}
}
```

### 11.4 Scopes in Events

- **root** — Primary character (e.g. the one the event is for).
- **scope:actor** / **scope:recipient** — Set by character interactions.
- **scope:child**, **scope:mother**, etc. — Set by the game or your script (e.g. in birth events).

Use **save_scope_as** / **save_temporary_scope_as** to store a scope and reuse it as **scope:name**.

### 11.5 Firing Events

- From **on_action** (see below): `trigger_event = { id = my_events.1 }` or `random_events = { 100 = my_events.1 }`.
- From decisions/effects: `trigger_event = { id = my_events.1 }`.
- With a specific character: `root = { trigger_event = { id = my_events.1 } }`.

---

## 12. On Actions (Pulses and Random Events)

**Path:** `common/on_action/your_on_actions.txt`

On_actions define **when** events run (e.g. yearly, on character birth).

### 12.1 Hooking Into Existing Pulses

```plaintext
yearly_playable_pulse = {
	events = {
		my_events.1
	}
}
```

Every year, for playable characters, the game will consider firing `my_events.1` (subject to its **trigger** and weight, if any).

### 12.2 Custom Pulses and Random Events

```plaintext
random_yearly_everyone_pulse = {
	on_actions = {
		my_yearly_action
	}
}

my_yearly_action = {
	trigger = {
		has_character_modifier = my_thing_modifier
	}
	effect = {
		save_scope_as = my_char
		random_list = {
			100 = {
				trigger_event = { id = my_events.2 }
			}
			200 = { }
		}
	}
}

my_random_events_pulse = {
	random_events = {
		100 = my_events.2
		100 = my_events.3
	}
}
```

- **trigger** — Who gets the on_action (e.g. everyone with a modifier).
- **effect** — What runs; here, optionally fire an event.
- **random_events** — Picks one event from the list by weight; the event’s **trigger** is still checked.

Events in **random_events** are referenced by ID (e.g. `my_events.2`).

---

## 13. Game Rules

**Path:** `common/game_rules/your_rules.txt`

Options in the game setup (e.g. “My feature: On / Off”).

```plaintext
my_feature_rule = {
	default = my_feature_enabled
	my_feature_disabled = {
		flag = GG_can_change_rule
	}
	my_feature_enabled = {
		flag = GG_can_change_rule
	}
}
```

- **default** — Which option is selected by default.
- **flag = GG_can_change_rule** — Player can change it in the lobby; use **GG_cannot_change_rule** for fixed rules.

In scripts: `has_game_rule = my_feature_enabled` or `has_game_rule = my_feature_disabled`.

---

## 14. Opinion Modifiers

**Path:** `common/opinion_modifiers/your_opinions.txt`

```plaintext
my_enslaved_me_opinion = {
	opinion = -80
	years = 50
	decaying = yes
}

my_crime_opinion = {
	opinion = -50
	imprisonment_reason = yes
	execute_reason = yes
	banish_reason = yes
}
```

Then in effects: `add_opinion_modifier = { target = scope:actor modifier = my_enslaved_me_opinion }`.

---

## 15. Scripted Relations

**Path:** `common/scripted_relations/your_relations.txt`

Custom relation types (e.g. slave / owner):

```plaintext
slave = {
	corresponding = slave_owner
	special_guest = yes
}

slave_owner = {
	corresponding = slave
	opinion = -10
}
```

Use with **set_relation_slave** / **set_relation_slave_owner** (or your own effect that uses the relation system). **effect_localization** (see below) gives readable names for “I gain/lose slave” etc.

---

## 16. Effect Localization

**Path:** `common/effect_localization/your_effects.txt`

Maps effect names to localization keys so the game can show “X gained/lost relation” in the right person (first/third) and tense:

```plaintext
set_relation_slave = {
	first = i_gain_slave
	third = they_gain_slave
	global = they_gain_slave
	first_past = i_got_slave
	third_past = they_got_slave
	global_past = they_got_slave
}
```

---

## 17. Trigger Localization

**Path:** `common/trigger_localization/your_triggers.txt`

Maps scripted trigger names to tooltip text (first/third/global, positive/negative):

```plaintext
my_can_do_thing_trigger = {
	first = i_can_do_thing
	first_not = i_cannot_do_thing
	third = they_can_do_thing
	third_not = they_cannot_do_thing
	global = can_do_thing
	global_not = cannot_do_thing
}
```

---

## 18. Customizable Localization

**Path:** `common/customizable_localization/your_custom_loc.txt`

Conditional text based on triggers (e.g. “High / Medium / Low” by a value):

```plaintext
MyValueDescription = {
	type = character
	text = {
		trigger = { my_high_value_trigger = yes }
		localization_key = my_high_description
	}
	text = {
		trigger = { my_low_value_trigger = yes }
		localization_key = my_low_description
	}
	text = {
		localization_key = my_default_description
	}
}
```

Use in localization with `[GetCustomizableLocalization('MyValueDescription')]` or similar.

---

## 19. Messages (Toasts / Notifications)

**Path:** `common/messages/your_messages.txt`

Defines message types for **send_interface_message** / toasts:

```plaintext
my_event_message = {
	icon = "icon_stress_gain"
	title = my_message_title
	desc = event_message_effect
	style = bad
	soundeffect = "event:/SFX/UI/Notifications/Messages/sfx_ui_message_theme_negative"
}
```

Then in an event/effect: `send_interface_message = { type = my_event_message title = my_specific_title right_icon = this ... }`.

### 19.1 Toasts from character interactions (debug-friendly)

If you want a right-click **character interaction** to immediately show a toast when clicked (no confirmation window), you typically need **all** of the following:

- Put the toast in `on_accept = { ... }` (this is the block that runs when the interaction is accepted).
- Add `common_interaction = yes` to skip the “interaction confirmation” dialog.
- Add `auto_accept = yes` so it executes instantly (useful for debug tools).

Example:

```plaintext
debug_show_slave_flags = {
	...
	common_interaction = yes
	auto_accept = yes

	on_accept = {
		scope:actor = {
			send_interface_toast = {
				title = debug_slave_flags_title
				desc = debug_slave_flags_desc
				tooltip = debug_slave_flags_tt
				left_icon = scope:recipient
				right_icon = scope:actor
			}
		}
	}
}
```

**Note on what you will see:** many CK3 toast styles show **only the title** on-screen. The `desc` and especially `tooltip` are usually visible when you **hover the toast** (and your game’s tooltip settings like “Timer Lock” can make that feel delayed).

## 19.2 Popup “debug inspector” window from a right-click interaction (event window)

If you want a right-click **character interaction** to open a full **event popup** (instead of a toast you must hover),
use `trigger_event` from `on_accept` and pass the clicked character as the event **target**.

### Step 1 — Interaction (right-click)

**Path:** `common/character_interactions/debug_interactions.txt`

```plaintext
debug_show_slave_flags = {
	category = interaction_debug_main
	type = character_interaction

	common_interaction = yes
	auto_accept = yes
	is_shown = { debug_only = yes }
	is_valid_showing_failures_only = { always = yes }

	on_accept = {
		scope:actor = {
			trigger_event = {
				id = slave_debug.1
				target = scope:recipient
			}
		}
	}

	ai_potential = { always = no }
}
```

### Step 2 — Event definition (popup window)

**Path:** `events/slave_debug_events.txt`

```plaintext
namespace = slave_debug

slave_debug.1 = {
	type = character_event
	is_triggered_only = yes

	title = debug_slave_flags_title
	desc = debug_slave_flags_tt

	option = { name = OK }
}
```

### Step 3 — Localization for the event text

**Path:** `localization/english/debug_interactions_l_english.yml` (UTF-8 with BOM)

Use `target` in the text, because we passed `target = scope:recipient` in the interaction:

```yaml
l_english:
 debug_slave_flags_title: "Slave Flags"
 debug_slave_flags_tt: "#T Slave Flags#!\nDecorative: [target.Custom('debug_slave_flag_decorative')]"
```

### Step 4 — Scripted localization (the “Custom(…)” keys)

**Path:** `common/scripted_localization/debug_slave_flags.txt`

**Important:** CK3 scripted localization is loaded from `common/scripted_localization/` and is defined under
`defined_text = { ... }`. If you use a different top-level key, the game will not load your entries and you’ll see
errors like `ERROR:[target.Custom('your_key')]` in-game.

```plaintext
defined_text = {

	debug_slave_flag_decorative = {
		text = {
			trigger = { has_character_flag = is_slave_decorative }
			localization_key = debug_yes
		}
		text = { localization_key = debug_no }
	}

	debug_slave_flag_concubine = {
		text = {
			trigger = { has_character_flag = is_slave_concubine }
			localization_key = debug_yes
		}
		text = { localization_key = debug_no }
	}

	debug_slave_flag_secondary_wife = {
		text = {
			trigger = { has_character_flag = is_slave_secondary_wife }
			localization_key = debug_yes
		}
		text = { localization_key = debug_no }
	}

	debug_slave_flag_great_wife = {
		text = {
			trigger = { has_character_flag = is_slave_great_wife }
			localization_key = debug_yes
		}
		text = { localization_key = debug_no }
	}
}
```

### Troubleshooting checklist

If you see `ERROR:[target.Custom('debug_slave_flag_decorative')]`:

- The scripted localization key is not loaded (wrong folder, wrong filename, or wrong top-level key — it must be `defined_text`).
- The key name in the `.yml` does not exactly match the key defined in `common/scripted_localization/`.
- You forgot to restart the game after changing scripted localization files (they do not reliably hot-reload).


---

## 20. Localization

**Path:** `localization/english/your_file_l_english.yml` (and same under `french/`, etc.)

Format:

```yaml
l_english:

 my_decision_name: "My Decision"
 my_decision_desc: "Description of what this decision does."
 my_decision_tooltip: "Tooltip when hovering."
 msg_my_thing_started: "You started the thing."

 my_events.1.t: "Event Title"
 my_events.1.desc: "Event description with [root.GetFirstName]."
 my_events.1.a: "Option A"
 my_events.1.b: "Option B"
```

- First line is the language tag: **l_english**, **l_french**, etc.
- One space before the key (Paradox convention).
- Use **root**, **scope:actor**, etc. in square brackets: `[root.GetFirstName]`, `[scope:recipient.GetHerHis]`.
- **|E** marks a game concept (e.g. prestige, gold): `[prestige|E]`, `[gold|E]`.

Keep keys stable and unique (e.g. prefix with mod name: `mymod_decision_desc`).

---

## 21. Religion Doctrines

**Path:** `common/religion/doctrines/your_doctrines.txt`

Add or override faith doctrines (tenets). Structure follows vanilla doctrine groups and parameters; use **is_available_on_create** to hide in setup if needed. Carnalitas uses this for custom crime/acceptance doctrines (e.g. slavery, prostitution). Copy the pattern from vanilla or existing mods when adding new doctrines.

---

## 22. Scripted GUIs

**Path:** `common/scripted_guis/your_guis.txt`

Controls when a GUI element (e.g. a button or list) is shown and what it does:

```plaintext
my_button_gui = {
	scope = character
	saved_scopes = { player }
	is_shown = {
		root = scope:player
		has_trait = my_trait
	}
}
```

Used from **.gui** files to show/hide or fill widgets based on script.

---

## 23. Naming and Compatibility (Standalone Mods)

- **Prefix** — Use a short prefix (e.g. `mymod_`) for all IDs: decisions, events, traits, modifiers, triggers, effects, localization keys. Avoids clashes with vanilla and other mods.
- **Namespaces** — One namespace per event file (e.g. `namespace = my_events`). Keep event IDs unique across the mod.
- **No Carnalitas dependency** — Do not reference Carnalitas-specific files, triggers, or effects. Use only vanilla (or your own) script_values, triggers, and effects. Then your mod works with or without Carnalitas.
- **supported_version** — Match the CK3 version you test on (e.g. `1.18.*`). Update when the game patches.

---

## 24. Minimal Standalone Mod Checklist

1. **descriptor.mod** + **YourMod.mod** (with **path**).
2. **common/decisions/** — At least one decision or **common/character_interactions/** — At least one interaction.
3. **common/traits/** or **common/modifiers/** — If you add traits or modifiers.
4. **common/scripted_triggers/** and **common/scripted_effects/** — If you use custom logic.
5. **common/on_action/** — If you want time-based or random events.
6. **events/** — Events referenced by ID from on_actions or effects.
7. **localization/english/** — At least one `.yml` with all keys used in your mod (and other languages if you support them).
8. **common/game_rules/** — Optional; use if you want a lobby toggle for your feature.

---

## 25. Variables (declare, persistent, retrieve)

*Examples in this section are taken from the Carnalitas mod (e.g. `birth_events.txt`, `carn_variable_init.txt`, scripted_effects).*

### 25.1 Declare a variable

Variables are set on a **scope** (character, title, etc.). The scope must be the current scope or a saved scope.

**Store a scope as a variable** (e.g. "this character suspects this child"):

```plaintext
scope:father = {
	set_variable = {
		name = suspect_this_child_of_illegitimacy
		value = scope:child
	}
}
```

**Store a simple value** (yes/no or number):

```plaintext
set_variable = {
	name = recent_taltos_born
	value = yes
	years = 30
}
```

**Temporary value for the current effect/event only** (not saved with the game). Use **save_scope_value_as** when you only need the value in the same chain of effects:

```plaintext
save_scope_value_as = {
	name = newborn_legitimization
	value = yes
}
```

**Pass a flag into a named "value"** for use in scripted effects:

```plaintext
save_scope_value_as = {
	name = carn_new_fetish
	value = flag:$FETISH$
}
```

### 25.2 Variables that persist across saves

- **On a character (or other scope)** — Use **set_variable** with **years** (or no duration for permanent). The variable is saved with that scope (e.g. character) and persists across save/load.

  Example from the example mod:

```plaintext
set_variable = {
	name = recent_taltos_born
	value = yes
	years = 30
}
```

- **Character flags** — **add_character_flag** (optionally with **months** or **years**) also persists with the character. Use for simple on/off state.

- **Game-wide** — **set_global_variable** persists for the whole campaign and is not tied to a character:

```plaintext
set_global_variable = {
	name = carn_active
	value = yes
}
```

  (Example from `common/on_action/carn_variable_init.txt`, run on game start.)

**Note:** **save_scope_value_as** and **save_temporary_scope_value_as** are for temporary use within the same effect/event; they are **not** persisted to save. For persistent state, use **set_variable** (with duration if you want) on the scope, **add_character_flag**, or **set_global_variable**.

### 25.3 Retrieve / check a variable

**Check if a variable exists** (in the current scope):

```plaintext
has_variable = recent_taltos_born
```

**Check on another scope:**

```plaintext
scope:mother = { has_variable = borte_first_child_var }
```

**Numeric comparison** (e.g. `variable >= X`, `variable > X`) — *Not demonstrated in the example mod.* The engine supports comparing variables to numbers in triggers; see the CK3 wiki or vanilla scripts for exact syntax.

**In localization / GUI** — Variables on a character scope can be read in .gui or .yml with the variable system, e.g. `[Character.MakeScope.Var('variable_name').GetValue|0]`. The example mod uses this for display (e.g. lactation value); opening a custom window by name is not shown (see [§28](#28-custom-windows-and-opening-ui)).

---

## 26. Lists / arrays

*Examples from the Carnalitas mod: `carn_fetish_effects.txt`, `carn_sex_scene_effects.txt`, `zzz_carn_00_grant_titles_interaction_overwrite.txt`, scripted_guis.*

Lists (variable lists) live on a scope (e.g. character). They persist with that scope across saves unless you clear them.

### 26.1 Create / add to a list

You do not "create" an empty list explicitly; adding the first entry effectively creates it.

**Add a scope to a list** (e.g. a character, or a flag scope):

```plaintext
add_to_variable_list = {
	name = carn_active_fetishes
	target = scope:carn_new_fetish
}
```

**Add a flag to a list** (e.g. option flags for a scene):

```plaintext
add_to_variable_list = {
	name = carn_sex_scene_option_flag_list
	target = flag:no_pregnancy
}
```

### 26.2 Iterate over a list

**every_in_list** — Run effects for each entry; **this** is the current list element:

```plaintext
every_in_list = {
	variable = carn_active_fetishes
	carn_fetish_tooltip_effect = {
		FETISH = this
	}
}
```

With **list** and **limit** (e.g. filter by tier):

```plaintext
every_in_list = {
	list = target_titles
	limit = { tier = tier_county }
	# effects; 'this' or save_scope_as for the title
}
```

### 26.3 Check list membership and clear / remove

**Has the list at least one entry?**

```plaintext
has_variable_list = candidate_a_knights_tale_achievement
```

**Is a specific target in the list?**

```plaintext
is_target_in_variable_list = {
	name = candidate_a_knights_tale_achievement
	target = scope:recipient
}
```

**Clear the entire list:**

```plaintext
clear_variable_list = carn_active_fetishes
```

**Remove one entry from the list:**

```plaintext
remove_list_variable = {
	name = carn_active_fetishes
	target = flag:$FETISH$
}
```

---

## 27. Character interactions and editing (examples)

*All examples below are from the Carnalitas mod.*

### 27.1 Interaction structure (categories, targets, validation)

**Right-click interaction** — actor = player (or AI) initiating, recipient = character clicked:

```plaintext
carn_enslave_interaction = {
	interface_priority = 100
	common_interaction = yes
	category = interaction_category_prison
	desc = carn_enslave_interaction_desc

	ai_targets = { ai_recipients = prisoners }
	is_shown = {
		scope:recipient = {
			OR = {
				is_courtier_of = scope:actor
				is_imprisoned_by = scope:actor
			}
			NOR = { has_trait = slave has_character_flag = carn_cannot_be_enslaved }
		}
	}
	is_valid_showing_failures_only = {
		scope:recipient = { NOT = { has_strong_hook = scope:actor } }
		# ... more checks with custom_description for tooltip failure text
	}
	on_accept = { ... }
}
```

**Friendly interaction with cooldown and gold cost:**

```plaintext
carn_sex_interaction = {
	category = interaction_category_friendly
	cooldown = { months = carn_sex_interaction_cooldown }
	is_valid_showing_failures_only = {
		scope:actor = { carn_can_have_sex_trigger = yes }
		scope:recipient = { carn_can_have_sex_trigger = yes }
		trigger_if = {
			limit = { ... }
			scope:actor.gold >= scope:recipient.carn_prostitute_sex_interaction_price_value
		}
	}
	on_accept = {
		scope:actor = {
			pay_short_term_gold = { target = scope:recipient gold = ... }
			add_character_flag = { flag = carn_sex_interaction_effect_cd months = ... }
			stress_impact = { ... }
			# custom scripted effects, trigger_event, etc.
		}
	}
}
```

**Free slave** — use **send_option** for multiple "modes" (e.g. demand gold, demand conversion):

```plaintext
carn_free_slave_interaction = {
	on_accept = {
		scope:actor = { save_scope_as = owner }
		scope:recipient = { save_scope_as = slave }
		carn_free_slave_interaction_effect = yes
	}
	send_option = {
		flag = gold
		localization = "RANSOM_GOLD_OPTION"
		is_shown = { scope:recipient = { gold >= ... } }
	}
	send_option = { flag = current_gold ... }
}
```

### 27.2 Editing characters in effects

Examples of common effects used **inside** interactions (or events/decisions), with the relevant scope (actor, recipient, root, or a saved scope):

- **Traits:** `add_trait = slave`, `remove_trait = former_slave`, `add_trait = peasant_leader`
- **Modifiers:** `add_character_modifier = carn_using_birth_control_modifier`, `remove_character_modifier = carn_using_birth_control_modifier`
- **Flags (timed):** `add_character_flag = { flag = carn_sex_interaction_effect_cd months = carn_sex_interaction_cooldown_base }`, `remove_character_flag = father_suspects_this_pregnancy`
- **Prestige / piety / gold:** `add_prestige = { value = ... }`, `add_piety = minor_piety_loss`, `pay_short_term_gold = { target = scope:recipient gold = ... }`, `add_gold = minor_gold_value`
- **Stress:** `stress_impact = { base = minor_stress_impact_loss chaste = activity_stress_gain_impact }`, `add_stress = { value = ... multiply = -1 }`
- **Opinions:** `add_opinion_modifier = { target = scope:actor modifier = my_opinion_modifier }`, or use **add_opinion** with a direct value in interactions that support it (e.g. in the grant titles overwrite)
- **Relations:** `set_relation_slave = scope:new_slave`, `remove_relation_slave_owner = prev` (with **every_relation**)
- **Court:** `add_courtier = scope:new_slave`, `remove_concubine = prev`, `divorce = scope:new_slave`
- **Scopes for later use:** `save_scope_as = owner`, `save_temporary_scope_as = new_slave` then run scripted effects that use **$OWNER$**, **$SLAVE$**, etc.

All of these are used in the example mod's character_interactions and scripted_effects; refer to those files for full context.

---

## 28. Custom windows and opening UI

*What the example mod provides:*

The Carnalitas mod **does not** provide an example of opening a **new, separate custom window** by name (e.g. a dedicated "My Mod" window that you open via a button). It only does the following:

- **Override existing windows** — Replaces or extends vanilla `.gui` (e.g. `window_character.gui`, `window_court.gui`) so that when the game opens the character or court window, your version is used.
- **Scripted GUIs** — Defines when a **widget or list** inside an existing window is shown and what it displays (e.g. `carn_fetish_gui`, `carn_fetish_gui_list` in `common/scripted_guis/carn_fetish_gui.txt`). The GUI file references these scripted_guis to show/hide or fill content (e.g. `every_in_list` over a variable list).
- **Variable system in GUI** — Uses `GetVariableSystem`, `GetPlayer.MakeScope.Var('variable_name').GetValue`, etc., in `.gui` to drive visibility or values. This is used for existing windows, not for "opening" a new window.

### 28.1 Scroll box (in .gui)

*Examples from the Carnalitas mod: `gui/window_character.gui` (family, relations, traits, modifiers, etc.).*

A **scroll box** is a GUI container that scrolls when its content is taller (or wider) than the visible area. In CK3 `.gui` you define it like this:

**Basic scroll box with custom content:**

```plaintext
scrollbox = {
	name = "my_scrollbox"
	layoutpolicy_vertical = expanding
	layoutpolicy_horizontal = expanding

	blockoverride "scrollbox_margins" {}

	blockoverride "scrollbox_content" {
		widget = {
			# Your content here: vbox, hbox, text, dynamicgridbox, etc.
			vbox = {
				spacing = 10
				text_label_center = { text = "MY_TITLE" }
				# ... more widgets
			}
		}
	}
}
```

- **scrollbox** — The scroll container. Give it a **name** and **layoutpolicy_vertical** / **layoutpolicy_horizontal** (usually `expanding`) so it fills the space.
- **blockoverride "scrollbox_margins"** — Optional. Use `{}` for no extra margins, or set **margin**, **margin_right**, **margin_top**, etc. to add padding inside the scroll area.
- **blockoverride "scrollbox_content"** — **Required.** Everything inside this block is the scrollable content. Put your **widget**, **vbox**, **hbox**, **dynamicgridbox**, etc. here.

**Scroll box with a dynamic list (vbox of rows):**

When the content is a list filled by the game (e.g. siblings, children, relations), the mod uses **scrollbox_replace_vbox** and a row template (e.g. `vbox_character_row_item`):

```plaintext
scrollbox = {
	name = "family_siblings_expanded"
	visible = "[CharacterWindow.IsRelationExpanded( 'siblings' )]"
	size = { 100% 100% }

	blockoverride "scrollbox_replace_vbox" {
		vbox_character_row_item = {
			name = "siblings"
			margin_top = 10
			spacing = 5
			# ... datamodel, portrait_datamodel, etc.
		}
	}
}
```

The game then fills the scroll area with one row per list item. For a simple custom scroll area with static or datamodel-driven content, the first pattern ( **scrollbox_content** ) is enough.

### 28.2 Vbox manipulation and relationship to widget / other containers

*Examples from the Carnalitas mod: `gui/window_character.gui`, `gui/carn_widgets.gui`.*

In CK3 GUI you do **not** “transform” a vbox into a widget or vice versa. **vbox**, **hbox**, and **widget** are different **container types**; you **nest** them. A **vbox** stacks its children vertically; an **hbox** stacks them horizontally; a **widget** is a generic container (no built-in layout direction; you still use layout policies and children). You put a **vbox** inside a **widget**, or a **widget** inside a **vbox**, depending on the layout you want.

#### Ways to manipulate a vbox

These are properties and patterns used on **vbox** (and often on **widget** / **hbox** too) in the example mod:

| Property / pattern | Purpose | Example |
|-------------------|--------|--------|
| **name** | Identify the element (debug, scripts) | `name = "main_content"` |
| **layoutpolicy_horizontal** | How it grows in width | `expanding`, `growing`, or fixed |
| **layoutpolicy_vertical** | How it grows in height | `expanding`, `growing`, or fixed |
| **spacing** | Space between children | `spacing = 10` |
| **margin**, **margin_top**, **margin_bottom**, **margin_left**, **margin_right** | Padding inside the box | `margin = { 0 5 }`, `margin_top = 10` |
| **size** | Explicit size | `size = { 100% 100% }` or `{ 0 305 }` |
| **minimumsize**, **maximumsize** | Constrain size | `minimumsize = { -1 110 }` `maximumsize = { -1 110 }` |
| **visible** | Show/hide (expression) | `visible = "[CharacterWindow.IsTabShown('family')]"` |
| **datacontext** | Data binding for children | `datacontext = "[CharacterWindow.GetCharacter]"` |
| **using** | Reuse a style/block (margins, animation) | `using = Window_Margins_Sidebar` |
| **expand** | Take extra space in parent | `expand = {}` |
| **scissor** | Clip overflow | `scissor = yes` |

**Children of a vbox** — A vbox can contain any mix of: **widget**, **hbox**, **vbox**, **scrollbox**, **text_single**, **text_label_center**, **button**, **background**, **fixedgridbox**, **dynamicgridbox**, **divider_light**, **portrait_***, **container**, and specialized types like **vbox_character_row_item**. Layout is vertical (one child under the next).

**blockoverride** — The example mod does **not** use `blockoverride` on a raw **vbox** itself. It uses **blockoverride** on **scrollbox_content**, **scrollbox_replace_vbox**, **portrait_button**, etc. So overriding a vbox’s internal blocks is not shown; you only set the vbox’s properties and children directly.

#### “Transforming” to different objects: nesting and types

You don’t convert vbox → widget. You **nest** containers and, if you want reuse, define **types**.

1. **Widget containing vbox** — Use a **widget** as the outer container (e.g. for size/visibility), and put a **vbox** inside for vertical stacking:

```plaintext
widget = {
	name = "parents_grandparents_spouses"
	layoutpolicy_horizontal = expanding
	layoutpolicy_vertical = expanding
	minimumsize = { -1 110 }
	maximumsize = { -1 110 }
	scissor = yes

	vbox = {
		spacing = 10
		# children: text_single, fixedgridbox, etc.
	}
}
```

2. **Vbox containing widget** — Use a **vbox** for the column, and **widget** (or **hbox**) for a row or custom block:

```plaintext
vbox = {
	name = "name_and_traits"
	layoutpolicy_horizontal = expanding

	vbox = {
		name = "name_health_and_relationship"
		hbox_character_view_name_age_health = { ... }
		hbox_character_relation_and_ai = { ... }
	}
	hbox_traits_list = { ... }
}
```

3. **Vbox and hbox together** — **hbox** for a horizontal row, **vbox** for a vertical column; nest as needed (e.g. hbox of vboxes for a grid-like layout):

```plaintext
hbox = {
	layoutpolicy_horizontal = expanding
	spacing = 5

	vbox = { name = "imprisoned_by" ... }
	vbox = { name = "hostage_home_court" ... }
	vbox = { name = "liege_etc_area" ... }
}
```

4. **Reusable “widget” that contains vbox/hbox: types** — In a **types** block (e.g. `gui/carn_widgets.gui`) you define a **type** that extends **widget** (or **icon**, or **vbox_character_row_item**) and put **vbox** / **hbox** inside. You then use that type by name instead of repeating the whole block:

```plaintext
types carn_widget {
	type carn_widget_slaves = widget {
		name = "carnalitas_slaves_row"
		layoutpolicy_horizontal = expanding
		layoutpolicy_vertical = expanding
		minimumsize = { -1 110 }
		maximumsize = { -1 110 }
		scissor = yes

		hbox = {
			vbox_character_row_relationship_item = { name = "slaves" ... }
		}
	}
}
```

Elsewhere you reference it as **carn_widget_slaves = {}** (or the type name your file uses). So the “transformation” is: **define a type based on widget (or another base), put vbox/hbox inside it, then instantiate that type** where you need that block. You are not converting one element into another; you are composing containers and naming the composition.

So: **opening a custom standalone window** (e.g. a new window type that appears when clicking a custom button) is **not provided** in the example mod. To do that you would need to rely on CK3's GUI system (e.g. defining a new window and a way to open it); consult the CK3 modding wiki or Paradox forums for that. This guide only documents what is present in the Carnalitas mod: overriding existing windows and using scripted_guis + variables within them.

---

This guide uses the same folder and file patterns as the Carnalitas mod, so you can open that mod’s files next to this document and follow along. For more triggers, effects, and scope names, check the official CK3 wiki or Paradox modding forums.
