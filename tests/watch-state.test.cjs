"use strict";
const assert = require("assert").strict;
const { initialState, transition } = require("../samples/hiro-design-watch/sample.js");

let state = initialState();
const input = state;
const original = { ...state };
state = transition(state, { type: "adjust", minutes: 5 });
assert.deepEqual(input, original, "Transitions must not mutate their input state");
assert.equal(state.duration, 30);
for (let i = 0; i < 50; i++) state = transition(state, { type: "adjust", minutes: 5 });
assert.equal(state.duration, 60, "Duration must not exceed the selectable upper bound");
for (let i = 0; i < 50; i++) state = transition(state, { type: "adjust", minutes: -5 });
assert.equal(state.duration, 5, "Duration must remain positive");

state = transition(initialState(), { type: "primary" });
state = transition(state, { type: "advance" });
assert.equal(state.remaining, 20);
assert.equal(transition(state, { type: "adjust", minutes: 5 }).duration, 25, "A running timer cannot be reconfigured");
state = transition(state, { type: "primary" });
assert.equal(state.status, "paused");
assert.deepEqual(transition(state, { type: "advance" }), state, "A paused timer must not advance");
state = transition(state, { type: "primary" });
assert.equal(state.remaining, 20, "Resume must preserve remaining time");

for (const view of ["aod", "glance"]) {
  const resting = transition(state, { type: "view", view });
  for (const action of [{ type: "primary" }, { type: "advance" }, { type: "reset" }, { type: "adjust", minutes: 5 }]) {
    assert.deepEqual(transition(resting, action), resting, "Comparison surfaces cannot change the timer");
  }
  assert.deepEqual(transition(resting, { type: "view", view: "app" }), state, "Surface changes must preserve the session");
}
for (let i = 0; i < 10; i++) state = transition(state, { type: "advance" });
assert.equal(state.remaining, 0, "A completed timer cannot become negative");
assert.equal(state.status, "complete");
state = transition(state, { type: "primary" });
assert.equal(state.remaining, 25, "A new session uses the selected duration");
assert.equal(state.status, "ready");
assert.deepEqual(transition(state, { type: "view", view: "invalid" }), state);
console.log("Watch simulation: limits, pause/resume, completion, immutable state, and surface transitions passed.");
