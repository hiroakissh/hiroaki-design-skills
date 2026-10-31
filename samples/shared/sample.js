"use strict";

const root = document.documentElement;
const themeButtons = [...document.querySelectorAll("[data-set-theme]")];

function setTheme(theme) {
  root.dataset.theme = theme;
  themeButtons.forEach(button => button.setAttribute("aria-pressed", String(button.dataset.setTheme === theme)));
  const url = new URL(location.href);
  url.searchParams.set("theme", theme);
  history.replaceState(null, "", url);
}

themeButtons.forEach(button => button.addEventListener("click", () => setTheme(button.dataset.setTheme)));
setTheme(new URLSearchParams(location.search).get("theme") === "dark" ? "dark" : "light");

const dialog = document.querySelector("dialog");
document.querySelectorAll("[data-open-dialog]").forEach(button => button.addEventListener("click", () => dialog.showModal()));
document.querySelectorAll("[data-close-dialog]").forEach(button => button.addEventListener("click", () => dialog.close()));

const stateSelect = document.querySelector("#demo-state");
if (stateSelect) {
  stateSelect.addEventListener("change", () => {
    document.querySelectorAll("[data-list-state]").forEach(view => { view.hidden = view.dataset.listState !== stateSelect.value; });
    document.querySelector("#app-list-region").setAttribute("aria-busy", String(stateSelect.value === "loading"));
  });
}

const detailTitle = document.querySelector("#detail-title");
if (detailTitle) {
  const projectButtons = [...document.querySelectorAll("[data-project-name]")];
  const taskGroups = new Map(projectButtons.map(button => [button.dataset.projectName, JSON.parse(button.dataset.projectTasks).map(name => ({ name, done: false }))]));
  let currentProject = projectButtons[0].dataset.projectName;
  const taskList = document.querySelector("#task-list");

  function renderTasks() {
    taskList.replaceChildren();
    taskGroups.get(currentProject).forEach(task => {
      const li = document.createElement("li");
      const label = document.createElement("label");
      const checkbox = document.createElement("input");
      checkbox.type = "checkbox";
      checkbox.checked = task.done;
      checkbox.addEventListener("change", () => { task.done = checkbox.checked; });
      label.append(checkbox, document.createTextNode(task.name));
      li.append(label);
      taskList.append(li);
    });
  }

  projectButtons.forEach(button => button.addEventListener("click", () => {
    currentProject = button.dataset.projectName;
    detailTitle.textContent = currentProject;
    document.querySelector("#detail-description").textContent = button.dataset.projectDetail;
    document.querySelector("#detail-progress-value").textContent = button.dataset.projectProgress + "%";
    document.querySelector("#detail-progress-fill").style.width = button.dataset.projectProgress + "%";
    document.querySelector("#detail-meter").setAttribute("aria-valuenow", button.dataset.projectProgress);
    document.querySelector("#app-message").textContent = "";
    renderTasks();
    if (matchMedia("(max-width: 760px)").matches) {
      detailTitle.tabIndex = -1;
      detailTitle.focus();
    }
  }));

  const form = document.querySelector("#task-form");
  const input = form.elements.task;
  form.addEventListener("submit", event => {
    event.preventDefault();
    const name = input.value.trim();
    if (!name) {
      input.setCustomValidity("作業名を入力してください");
      input.reportValidity();
      return;
    }
    taskGroups.get(currentProject).push({ name, done: false });
    renderTasks();
    document.querySelector("#app-message").textContent = "「" + name + "」を追加しました";
    form.reset();
    dialog.close();
  });
  input.addEventListener("input", () => input.setCustomValidity(""));
  renderTasks();
}

const search = document.querySelector("#project-search");
if (search) {
  const filter = document.querySelector("#status-filter");
  const tbody = document.querySelector("#project-rows");
  const selectAll = document.querySelector("#select-all");
  const rows = () => [...tbody.querySelectorAll("tr")];

  function updateSelection() {
    const visible = rows().filter(row => !row.hidden);
    const checked = rows().filter(row => row.querySelector("input").checked).length;
    const visibleChecked = visible.filter(row => row.querySelector("input").checked).length;
    selectAll.checked = visible.length > 0 && visibleChecked === visible.length;
    selectAll.indeterminate = visibleChecked > 0 && visibleChecked < visible.length;
    selectAll.disabled = visible.length === 0;
    document.querySelector("#selection-count").textContent = checked + "件を選択中";
    document.querySelector("#clear-selection").disabled = checked === 0;
  }

  function applyFilter() {
    const query = search.value.trim().toLocaleLowerCase("ja");
    let count = 0;
    rows().forEach(row => {
      row.hidden = !(row.dataset.name.toLocaleLowerCase("ja").includes(query) && (filter.value === "all" || row.dataset.status === filter.value));
      if (!row.hidden) count++;
      else row.querySelector("input").checked = false;
    });
    document.querySelector("#result-count").textContent = count + "件";
    document.querySelector("#no-results").hidden = count !== 0;
    updateSelection();
  }

  search.addEventListener("input", applyFilter);
  filter.addEventListener("change", applyFilter);
  document.querySelector("#clear-filters").addEventListener("click", () => {
    search.value = "";
    filter.value = "all";
    applyFilter();
    search.focus();
  });
  selectAll.addEventListener("change", () => {
    rows().filter(row => !row.hidden).forEach(row => { row.querySelector("input").checked = selectAll.checked; });
    updateSelection();
  });
  tbody.addEventListener("change", updateSelection);
  document.querySelector("#clear-selection").addEventListener("click", () => {
    rows().forEach(row => { row.querySelector("input").checked = false; });
    updateSelection();
  });

  const form = document.querySelector("#project-form");
  const input = form.elements.project;
  form.addEventListener("submit", event => {
    event.preventDefault();
    const name = input.value.trim();
    if (!name) {
      input.setCustomValidity("プロジェクト名を入力してください");
      input.reportValidity();
      return;
    }
    const tr = document.createElement("tr");
    tr.dataset.name = name;
    tr.dataset.status = "未着手";
    const cell = document.createElement("td");
    const label = document.createElement("label");
    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.setAttribute("aria-label", name + "を選択");
    label.append(checkbox, document.createTextNode(name));
    cell.append(label);
    tr.append(cell);
    ["共通基盤", "未着手", "0%"].forEach((value, index) => {
      const td = document.createElement("td");
      td.textContent = value;
      if (index === 2) td.className = "num";
      tr.append(td);
    });
    tbody.append(tr);
    document.querySelector("#all-project-count").textContent = String(rows().length);
    document.querySelector("#webapp-message").textContent = "「" + name + "」を追加しました。このデモでは再読み込みすると初期データに戻ります。";
    form.reset();
    dialog.close();
    search.value = "";
    filter.value = "all";
    applyFilter();
  });
  input.addEventListener("input", () => input.setCustomValidity(""));
  applyFilter();
}

const slides = [...document.querySelectorAll("[data-slide]")];
if (slides.length) {
  let position = 0;
  const previous = document.querySelector("#previous-slide");
  const next = document.querySelector("#next-slide");
  function showSlide(index) {
    position = Math.max(0, Math.min(slides.length - 1, index));
    slides.forEach((slide, index) => { slide.hidden = index !== position; });
    document.querySelector("#slide-position").textContent = (position + 1) + " / " + slides.length;
    previous.disabled = position === 0;
    next.disabled = position === slides.length - 1;
  }
  previous.addEventListener("click", () => showSlide(position - 1));
  next.addEventListener("click", () => showSlide(position + 1));
  document.addEventListener("keydown", event => {
    if (event.altKey || event.ctrlKey || event.metaKey || /INPUT|TEXTAREA|SELECT/.test(event.target.tagName)) return;
    if (event.key === "ArrowRight") { event.preventDefault(); showSlide(position + 1); }
    if (event.key === "ArrowLeft") { event.preventDefault(); showSlide(position - 1); }
  });
  showSlide(0);
}
