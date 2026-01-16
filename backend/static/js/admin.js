async function sendJson(url, method = "GET", data = null) {
    const cfg = { method };
    if (data) {
        cfg.headers = { "Content-Type": "application/json" };
        cfg.body = JSON.stringify(data);
    }
    const r = await fetch(url, cfg);
    const ct = r.headers.get("content-type") || "";
    const body = ct.includes("application/json") ? await r.json() : await r.text();
    if (!r.ok) throw new Error(body.error || body || `HTTP ${r.status}`);
    return body;
}

async function sendForm(url, method = "POST", formData) {
    const r = await fetch(url, { method, body: formData });
    const ct = r.headers.get("content-type") || "";
    const body = ct.includes("application/json") ? await r.json() : await r.text();
    if (!r.ok) throw new Error(body.error || body || `HTTP ${r.status}`);
    return body;
}

function esc(s) {
    return (s || "").replace(/[&<>"']/g, c => ({
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
    }[c]));
}

async function fetchMovies() {
    return await sendJson("/api/movies");
}

function renderAdminMovies(movies) {
    const root = document.getElementById("admin-movie-list");
    root.innerHTML = "";

    movies.forEach(m => {
        const card = document.createElement("div");
        card.className = "movie-card";

        const title = document.createElement("h3");
        title.textContent = m.title;

        const meta = document.createElement("div");
        meta.className = "meta";
        meta.textContent = `${m.genre}${m.year ? " • " + m.year : ""}${m.rating !== null && m.rating !== undefined ? " • Rating: " + m.rating : ""}`;

        const d = document.createElement("div");
        d.className = "description";
        d.textContent = m.description || "";

        const actions = document.createElement("div");
        actions.className = "actions";

        const openBtn = document.createElement("a");
        openBtn.className = "link-btn";
        openBtn.href = `/movie/${m.id}`;
        openBtn.textContent = "Open";

        const delBtn = document.createElement("button");
        delBtn.className = "delete-btn";
        delBtn.textContent = "Delete";
        delBtn.onclick = async () => {
            try {
                await sendJson(`/api/movies/${m.id}`, "DELETE");
                await refresh();
            } catch (e) {
                alert(e.message);
            }
        };

        actions.appendChild(openBtn);
        actions.appendChild(delBtn);

        card.appendChild(title);
        card.appendChild(meta);
        card.appendChild(d);
        card.appendChild(actions);

        root.appendChild(card);
    });
}

async function refresh() {
    const movies = await fetchMovies();
    renderAdminMovies(movies);
}

document.addEventListener("DOMContentLoaded", async () => {
    const form = document.getElementById("admin-add-movie-form");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const fd = new FormData(form);

        // If user uploaded a file, ignore manual URL (server will set it anyway)
        const file = fd.get("video_file");
        if (file && file.name) {
            fd.set("video_url", "");
        }

        try {
            await sendForm("/api/movies", "POST", fd);
            form.reset();
            await refresh();
        } catch (err) {
            alert(err.message);
        }
    });

    await refresh();
});
