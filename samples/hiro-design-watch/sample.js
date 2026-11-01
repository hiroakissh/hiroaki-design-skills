(function () {
  "use strict";

  function initialState() {
    return { duration: 25, remaining: 25, status: "ready", view: "app" };
  }

  function transition(state, action) {
    if (action.type === "view" && ["app", "glance", "aod"].includes(action.view)) return { ...state, view: action.view };
    if (state.view !== "app") return state;
    if (action.type === "adjust" && state.status === "ready" && [-5, 5].includes(action.minutes)) {
      const duration = Math.max(5, Math.min(60, state.duration + action.minutes));
      return { ...state, duration, remaining: duration };
    }
    if (action.type === "primary") {
      if (state.status === "running") return { ...state, status: "paused" };
      if (["ready", "paused"].includes(state.status)) return { ...state, status: "running" };
      if (state.status === "complete") return { ...state, remaining: state.duration, status: "ready" };
    }
    if (action.type === "advance" && state.status === "running") {
      const remaining = Math.max(0, state.remaining - 5);
      return { ...state, remaining, status: remaining === 0 ? "complete" : "running" };
    }
    if (action.type === "reset") return { ...state, remaining: state.duration, status: "ready" };
    return state;
  }

  if (typeof module !== "undefined" && module.exports) module.exports = { initialState, transition };
  if (typeof document === "undefined" || !document.querySelector("#watch-stage")) return;

  let state = initialState();
  const stage = document.querySelector("#watch-stage");
  const primaryButtons = [...stage.querySelectorAll("[data-watch-primary]")];
  const shapes = ["角型", "丸型", "縦長バンド"];
  const labels = { ready: "開始", running: "中断", paused: "再開", complete: "もう一度" };
  const statuses = { ready: "開始できます", running: "集中しています", paused: "中断しています", complete: "おつかれさま" };

  function render() {
    const aod = state.view === "aod";
    const glance = state.view === "glance";
    stage.dataset.watchMode = state.view;
    stage.querySelectorAll("[data-watch-task]").forEach(item => { item.textContent = aod ? "集中タイマー" : "資料の構成を考える"; });
    stage.querySelectorAll("[data-watch-value]").forEach(item => { item.textContent = aod ? "--:--" : String(state.remaining).padStart(2, "0") + ":00"; });
    stage.querySelectorAll("[data-watch-status]").forEach(item => { item.textContent = aod ? "更新を休止中" : statuses[state.status]; });
    primaryButtons.forEach((button, index) => {
      button.textContent = aod ? "操作を休止中" : glance ? "開く" : labels[state.status];
      button.disabled = aod;
      button.setAttribute("aria-label", shapes[index] + "の" + (aod ? "操作を休止中" : glance ? "タイマーを開く" : "タイマーを" + labels[state.status]));
    });
    document.querySelectorAll("[data-watch-view]").forEach(button => { button.setAttribute("aria-pressed", String(button.dataset.watchView === state.view)); });
    document.querySelector("#watch-less").disabled = state.view !== "app" || state.status !== "ready" || state.duration <= 5;
    document.querySelector("#watch-more").disabled = state.view !== "app" || state.status !== "ready" || state.duration >= 60;
    document.querySelector("#watch-advance").disabled = state.view !== "app" || state.status !== "running";
    document.querySelector("#watch-reset").disabled = state.view !== "app";
    document.querySelector("#watch-feedback").textContent = aod
      ? "常時表示の比較中。作業名と秒を隠し、値の更新と操作を休止しています。"
      : state.remaining + "分のタイマー。" + statuses[state.status] + "。";
    document.querySelector("#watch-mode-description").textContent = aod
      ? "通常画面と主情報の位置をそろえ、作業名を隠した低電力表示の概念例。値は更新停止のため --:-- に置換します。実OSの操作可否や更新条件は対象SDKで確認します。"
      : glance
        ? "一つの値から目的のアプリへ移る情報面の概念例です。実際のcomplication・Tile・Glanceは、各OSのfamilyと部品で別々に設計します。"
        : "主情報と一つの操作に絞ったアプリの概念例。3つの時計は同じ状態を共有します。";
  }

  function dispatch(action) { state = transition(state, action); render(); }
  document.querySelectorAll("[data-watch-view]").forEach(button => button.addEventListener("click", () => dispatch({ type: "view", view: button.dataset.watchView })));
  primaryButtons.forEach(button => button.addEventListener("click", () => dispatch({ type: state.view === "glance" ? "view" : "primary", view: "app" })));
  document.querySelector("#watch-less").addEventListener("click", () => dispatch({ type: "adjust", minutes: -5 }));
  document.querySelector("#watch-more").addEventListener("click", () => dispatch({ type: "adjust", minutes: 5 }));
  document.querySelector("#watch-advance").addEventListener("click", () => dispatch({ type: "advance" }));
  document.querySelector("#watch-reset").addEventListener("click", () => dispatch({ type: "reset" }));
  document.querySelector("#watch-monochrome").addEventListener("change", event => { stage.dataset.monochrome = String(event.target.checked); });
  render();
}());
