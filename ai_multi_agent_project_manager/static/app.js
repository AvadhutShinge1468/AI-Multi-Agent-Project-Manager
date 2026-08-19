async function analyzeProject() {
    const description = document.getElementById("description").value.trim();
    const error = document.getElementById("error");
    const loading = document.getElementById("loading");
    const dashboard = document.getElementById("dashboard");

    error.textContent = "";

    if (!description) {
        error.textContent = "Please enter a project description.";
        return;
    }

    loading.classList.remove("hidden");
    dashboard.classList.add("hidden");

    try {
        const response = await fetch("/api/analyze", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({description})
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Something went wrong.");
        }

        render(data);
        dashboard.classList.remove("hidden");
    } catch (e) {
        error.textContent = e.message;
    } finally {
        loading.classList.add("hidden");
    }
}

function render(data) {
    const agentIcons = ["📋", "🧠", "📅", "💻", "🧪", "📊", "📈"];
    document.getElementById("agents").innerHTML =
        data.agents.map((a, i) => `<div class="agent">${agentIcons[i]}<br>${a}</div>`).join("");

    const p = data.progress;
    document.getElementById("totalTasks").textContent = p.total_tasks;
    document.getElementById("completedTasks").textContent = p.completed_tasks;
    document.getElementById("pendingTasks").textContent = p.pending_tasks;
    document.getElementById("percentage").textContent = p.percentage + "%";
    document.getElementById("highRisks").textContent = p.high_risk_count;
    document.getElementById("health").textContent = p.health;

    document.getElementById("modules").innerHTML =
        data.requirements.modules.map(x => `<li>${escapeHtml(x)}</li>`).join("");

    document.getElementById("functional").innerHTML =
        data.requirements.functional_requirements.map(x => `<li>${escapeHtml(x)}</li>`).join("");

    document.getElementById("nonfunctional").innerHTML =
        data.requirements.non_functional_requirements.map(x => `<li>${escapeHtml(x)}</li>`).join("");

    document.getElementById("tasks").innerHTML =
        data.tasks.map(t =>
            `<tr><td>${escapeHtml(t.task)}</td><td>${t.duration}</td><td>${t.priority}</td><td>${t.status}</td></tr>`
        ).join("");

    document.getElementById("totalDays").textContent = data.scheduling.total_days;
    document.getElementById("completion").textContent = data.scheduling.estimated_completion;

    document.getElementById("schedule").innerHTML =
        data.scheduling.schedule.map(s =>
            `<tr><td>${escapeHtml(s.task)}</td><td>${s.start}</td><td>${s.end}</td></tr>`
        ).join("");

    document.getElementById("tests").innerHTML =
        data.tests.map(t =>
            `<tr><td>${escapeHtml(t.module)}</td><td>${escapeHtml(t.test_case)}</td><td>${t.status}</td></tr>`
        ).join("");

    document.getElementById("risks").innerHTML =
        data.risks.map(r =>
            `<tr>
                <td>${escapeHtml(r.risk)}</td>
                <td>${r.probability}</td>
                <td>${r.impact}</td>
                <td>${r.score}</td>
                <td>${escapeHtml(r.mitigation)}</td>
            </tr>`
        ).join("");
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}
