
document.addEventListener("DOMContentLoaded", function () {
    // 1. Кнопка «Позначити пройденим» (стан зберігаємо в браузері)
    var doneBtn = document.getElementById("done-btn");
    if (doneBtn) {
        var key = "lms-done-" + doneBtn.dataset.key;
        var render = function (isDone) {
            doneBtn.textContent = isDone ? "Пройдено ✓" : "Позначити пройденим";
            doneBtn.classList.toggle("done", isDone);
        };
        try { render(localStorage.getItem(key) === "1"); } catch (e) { render(false); }
        doneBtn.addEventListener("click", function () {
            var isDone = !doneBtn.classList.contains("done");
            try { localStorage.setItem(key, isDone ? "1" : "0"); } catch (e) { /* ігноруємо */ }
            render(isDone);
        });
    }

    // 2. Миттєвий фільтр карток курсів під час введення тексту
    var search = document.getElementById("course-search");
    if (search) {
        search.addEventListener("input", function () {
            var q = search.value.trim().toLowerCase();
            document.querySelectorAll(".card").forEach(function (card) {
                card.hidden = q !== "" && card.dataset.title.indexOf(q) === -1;
            });
        });
    }

    document.querySelectorAll(".dashboard-course").forEach(function (row) {
        var orders = row.dataset.lessonOrders ? row.dataset.lessonOrders.split(",") : [];
        var completed = 0;
        try {
            completed = orders.filter(function (order) {
                return localStorage.getItem("lms-done-" + row.dataset.courseSlug + "-" + order) === "1";
            }).length;
        } catch (e) { /* ігноруємо */ }

        var progress = orders.length ? Math.round(completed / orders.length * 100) : 0;
        row.querySelector("[data-progress]").textContent = progress + "%";
        row.querySelector("[data-progress-bar]").style.width = progress + "%";
        row.querySelector("[data-progress-status]").textContent = orders.length === 0
            ? "Немає уроків"
            : progress === 100 ? "Завершено" : "У процесі";
    });
});