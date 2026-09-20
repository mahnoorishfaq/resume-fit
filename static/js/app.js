/* ==================================================================
   Resume Fit - front end
   ================================================================== */

const $ = (id) => document.getElementById(id);

const state = { file: null, mode: "custom" };

/* ---------------- file upload ---------------- */
const drop = $("drop");
const fileInput = $("resumeInput");

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length) acceptFile(e.target.files[0]);
});

["dragenter", "dragover"].forEach((evt) =>
  drop.addEventListener(evt, (e) => {
    e.preventDefault();
    drop.classList.add("is-over");
  })
);

["dragleave", "drop"].forEach((evt) =>
  drop.addEventListener(evt, (e) => {
    e.preventDefault();
    drop.classList.remove("is-over");
  })
);

drop.addEventListener("drop", (e) => {
  const file = e.dataTransfer.files[0];
  if (file) acceptFile(file);
});

function acceptFile(file) {
  const ok = [".pdf", ".docx", ".txt"].some((ext) =>
    file.name.toLowerCase().endsWith(ext)
  );
  if (!ok) {
    showAlert("That file type isn't supported. Upload a PDF, DOCX or TXT.");
    return;
  }
  if (file.size > 5 * 1024 * 1024) {
    showAlert("That file is larger than 5 MB. Try exporting a smaller PDF.");
    return;
  }
  state.file = file;
  $("fileName").textContent = file.name;
  $("fileChip").hidden = false;
  drop.hidden = true;
  $("panelResume").classList.add("is-ready");
  hideAlert();
  refreshButton();
}

$("fileClear").addEventListener("click", () => {
  state.file = null;
  fileInput.value = "";
  $("fileChip").hidden = true;
  drop.hidden = false;
  $("panelResume").classList.remove("is-ready");
  refreshButton();
});

/* ---------------- tabs ---------------- */
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => {
      t.classList.remove("is-active");
      t.setAttribute("aria-selected", "false");
    });
    tab.classList.add("is-active");
    tab.setAttribute("aria-selected", "true");

    state.mode = tab.dataset.mode;
    $("modeCustom").hidden = state.mode !== "custom";
    $("modeLibrary").hidden = state.mode !== "library";
    refreshButton();
  });
});

/* ---------------- job text counter ---------------- */
const jobText = $("jobText");

jobText.addEventListener("input", () => {
  const n = jobText.value.trim().length;
  $("charCount").textContent = n.toLocaleString();
  $("charHint").textContent =
    n >= 60 ? "ready to analyse" : "paste at least 60 to analyse";
  $("panelJob").classList.toggle("is-ready", n >= 60);
  refreshButton();
});

/* ---------------- button state ---------------- */
function jobReady() {
  if (state.mode === "library") return true;
  return jobText.value.trim().length >= 60;
}

function refreshButton() {
  const ready = state.file && jobReady();
  $("analyseBtn").disabled = !ready;

  let hint;
  if (!state.file && !jobReady()) hint = "Add a resume and a job description to continue";
  else if (!state.file) hint = "Now upload your resume";
  else if (!jobReady()) hint = "Now paste the job description";
  else hint = "Ready";
  $("actionHint").textContent = hint;

  if (state.mode === "library") $("panelJob").classList.add("is-ready");
}

/* ---------------- alerts ---------------- */
function showAlert(message) {
  const box = $("alert");
  box.textContent = message;
  box.hidden = false;
  box.scrollIntoView({ behavior: "smooth", block: "center" });
}
function hideAlert() { $("alert").hidden = true; }

/* ---------------- analyse ---------------- */
$("analyseBtn").addEventListener("click", async () => {
  hideAlert();
  const btn = $("analyseBtn");
  btn.classList.add("is-busy");
  btn.disabled = true;

  const body = new FormData();
  body.append("resume", state.file);
  body.append("mode", state.mode);

  if (state.mode === "custom") {
    body.append("job_text", jobText.value.trim());
    body.append("job_title", $("jobTitle").value.trim());
  } else {
    const picked = document.querySelector('input[name="job_index"]:checked');
    body.append("job_index", picked ? picked.value : "0");
  }

  try {
    const response = await fetch("/api/analyse", { method: "POST", body });
    const data = await response.json();
    if (!response.ok) {
      showAlert(data.error || "Something went wrong. Try again.");
      return;
    }
    render(data);
  } catch (err) {
    showAlert("Could not reach the server. Is the Flask app still running?");
  } finally {
    btn.classList.remove("is-busy");
    refreshButton();
  }
});

/* ---------------- render ---------------- */
function render(d) {
  const results = $("results");
  results.hidden = false;
  results.classList.remove("is-in");
  void results.offsetWidth;          // restart the entrance animation
  results.classList.add("is-in");

  $("verdictLabel").textContent = d.verdict;
  $("verdictNote").textContent = d.verdict_note;
  $("jobLabel").textContent = d.job_label;

  $("statCoverage").textContent = d.coverage + "%";
  $("statMatched").textContent = d.matched.length;
  $("statMissing").textContent = d.missing.length;
  $("statHealth").textContent = d.health_score;

  countUp($("score"), d.score);
  setTimeout(() => { $("scoreFill").style.width = d.score + "%"; }, 80);

  renderChips($("matchedChips"), d.matched, "have",
              "None of this role's skills were found in your resume.");
  renderChips($("missingChips"), d.missing, "gap",
              "Nothing missing. This one is worth sending.");

  renderPlan(d.plan);
  renderChecks(d.checks);
  renderRecs(d.recommendations);

  results.scrollIntoView({ behavior: "smooth", block: "start" });
}

function renderChips(container, items, cls, emptyText) {
  container.innerHTML = "";
  if (!items.length) {
    container.innerHTML = `<span class="chip none">${emptyText}</span>`;
    return;
  }
  items.forEach((name, i) => {
    const el = document.createElement("span");
    el.className = "chip " + cls;
    el.textContent = name;
    el.style.animationDelay = Math.min(i * 28, 400) + "ms";
    container.appendChild(el);
  });
}

function renderPlan(plan) {
  const block = $("planBlock");
  const list = $("planList");
  list.innerHTML = "";

  if (!plan.length) {
    block.hidden = true;
    return;
  }
  block.hidden = false;

  plan.forEach((item) => {
    const el = document.createElement("div");
    el.className = "learn" + (item.priority ? " key" : "");
    el.innerHTML = `
      <div class="learn-name">${item.skill}${
        item.priority ? '<span class="learn-flag">high leverage</span>' : ""
      }</div>
      <div class="learn-cat">${item.category}</div>
      <div class="learn-note">${item.note}</div>`;
    list.appendChild(el);
  });
}

function renderChecks(checks) {
  const list = $("checkList");
  list.innerHTML = "";
  const marks = { pass: "✓", warn: "!", fail: "✕" };

  checks.forEach((c) => {
    const el = document.createElement("div");
    el.className = "check " + c.state;
    el.innerHTML = `
      <div class="check-mark">${marks[c.state]}</div>
      <div>
        <div class="check-name">${c.name}</div>
        <div class="check-msg">${c.message}</div>
      </div>`;
    list.appendChild(el);
  });
}

function renderRecs(recs) {
  const list = $("recList");
  list.innerHTML = "";
  recs.forEach((r) => {
    const el = document.createElement("div");
    el.className = "rec";
    el.innerHTML = `
      <div class="rec-score">${r.score}<small>%</small></div>
      <div>
        <div class="rec-title">${r.title}</div>
        <div class="rec-meta">${r.company} · ${r.level} · ${r.location}</div>
      </div>`;
    list.appendChild(el);
  });
}

/* count the score up rather than snapping to it */
function countUp(el, target) {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    el.innerHTML = target + '<span class="pct">%</span>';
    return;
  }
  const duration = 900;
  const start = performance.now();

  function frame(now) {
    const t = Math.min((now - start) / duration, 1);
    const eased = 1 - Math.pow(1 - t, 3);
    el.innerHTML = Math.round(target * eased) + '<span class="pct">%</span>';
    if (t < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

/* ---------------- misc ---------------- */
$("againBtn").addEventListener("click", () => {
  window.scrollTo({ top: 0, behavior: "smooth" });
});

const dialog = $("howDialog");
$("howBtn").addEventListener("click", () => dialog.showModal());
$("howClose").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (e) => {
  if (e.target === dialog) dialog.close();
});

document.querySelectorAll('input[name="job_index"]').forEach((radio) =>
  radio.addEventListener("change", refreshButton)
);

refreshButton();
