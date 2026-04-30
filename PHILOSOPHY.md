# Philosophy

Seven values thread every guideline in this repo. When two guidelines disagree, prefer the one that better honors these values.

## 1. Clarity over cleverness

Names that read aloud beat clever abbreviations. `customer-onboarding/` over `cst-onbrd/`. Future-you will thank present-you.

## 2. Discoverability

A stranger should find the right file in <30 seconds. If they can't, the layout has failed regardless of how elegant it is.

## 3. Predictability

Same kind of thing, same kind of place, every time. If "third-party libs go in `vendor/`" in one project and `third_party/` in another, both projects pay the cost.

## 4. Separation of concerns

One directory, one responsibility. A directory that mixes app code, build scripts, and ad-hoc notes is three directories pretending to be one.

## 5. Shallow over deep

Every level of nesting costs cognitive load. Keep your tree as flat as the domain allows. See [`principles/depth-vs-breadth/`](principles/depth-vs-breadth/).

## 6. Stable boundaries

What changes daily and what changes yearly should not share a directory. Mixing temporal scales is what creates "the dir I'm scared to clean up."

## 7. Fewest surprises

Follow ecosystem conventions before inventing your own. A Python project that looks like a Python project costs nothing to learn; a snowflake costs every reader 30 minutes.
