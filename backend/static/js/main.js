function trunc(s, n) {
    if (!s) return "";
    s = String(s);
    return s.length > n ? s.slice(0, n - 1) + "…" : s;
}

function esc(s) {
    return (s || "").replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[c]));
}

async function getJson(url) {
    const r = await fetch(url);
    const ct = r.headers.get("content-type") || "";
    const body = ct.includes("application/json") ? await r.json() : await r.text();
    if (!r.ok) throw new Error(body.error || body || `HTTP ${r.status}`);
    return body;
}

function renderMovies(movies) {
    const grid = document.getElementById("movies-grid");
    if (!grid) return;

    grid.innerHTML = "";

    movies.forEach(m => {
        const card = document.createElement("div");
        card.className = "movie-card";

        const title = document.createElement("h3");
        title.textContent = m.title;

        const meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent =
            `${m.genre || ""}` +
            (m.year ? ` • ${m.year}` : "") +
            ((m.rating !== null && m.rating !== undefined) ? ` • Rating: ${m.rating}` : "");

        const desc = document.createElement("div");
        desc.className = "description";
        desc.textContent = trunc(m.description || "", 120);

        const link = document.createElement("a");
        link.className = "link-btn";
        link.href = `/movie/${m.id}`;
        link.textContent = "Watch now";

        card.appendChild(title);
        card.appendChild(meta);
        card.appendChild(desc);
        card.appendChild(link);

        grid.appendChild(card);
    });
}

function openModal(rec) {
    const modal = document.getElementById("recommend-modal");
    const title = document.getElementById("rec-title");
    const meta = document.getElementById("rec-meta");
    const desc = document.getElementById("rec-desc");
    const link = document.getElementById("rec-link");

    if (!modal || !title || !meta || !desc || !link) return;

    title.textContent = rec.title || "Recommendation";
    meta.textContent =
        `${rec.genre || ""}` +
        (rec.year ? ` • ${rec.year}` : "") +
        ((rec.rating !== null && rec.rating !== undefined) ? ` • Rating: ${rec.rating}` : "");

    desc.textContent = rec.description || "";
    link.href = `/movie/${rec.id}`;

    modal.classList.remove("hidden");
}

function closeModal() {
    const modal = document.getElementById("recommend-modal");
    if (!modal) return;
    modal.classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", async () => {
    // Render movies
    try {
        const movies = await getJson("/api/movies");
        renderMovies(movies);
    } catch (e) {
        console.error("Failed to load movies:", e);
    }

    // Recommendation button
    const btn = document.getElementById("btn-recommend");
    if (btn) {
        btn.addEventListener("click", async () => {
            try {
                const recs = await getJson("/api/recommendations?limit=1");
                if (!Array.isArray(recs) || recs.length === 0) {
                    alert("No recommendations yet.");
                    return;
                }
                openModal(recs[0]);
            } catch (e) {
                console.error(e);
                alert(e.message || "Failed to get recommendation");
            }
        });
    }

    // Modal close
    const closeBtn = document.getElementById("modal-close");
    if (closeBtn) closeBtn.addEventListener("click", closeModal);

    const modal = document.getElementById("recommend-modal");
    if (modal) {
        modal.addEventListener("click", (e) => {
            if (e.target === modal) closeModal();
        });
    }
});
