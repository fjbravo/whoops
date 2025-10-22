import { API } from "./api.js";

function showAlert(message, type = "success") {
  const alertContainer = document.querySelector("#error-container");
  alertContainer.innerHTML = "";

  const div = document.createElement("div");
  div.className = `alert alert-${type} mt-2`;
  div.role = "alert";
  div.textContent = message;
  alertContainer.appendChild(div);
}

document.addEventListener("DOMContentLoaded", () => {
  const wait = document.querySelector(".wait");
  const exportBtn = document.getElementById("export-button");
  const scheduleBtn = document.getElementById("schedule-button");

  exportBtn.addEventListener("click", async () => {
    exportBtn.disabled = true;
    wait.style.visibility = "visible";

    const result = await API.exportNow();
    showAlert(result.message, result.success ? "success" : "danger");

    exportBtn.disabled = false;
    wait.style.visibility = "hidden";
  });

  scheduleBtn.addEventListener("click", async () => {
    const hour = document.getElementById("hour-input").value;
    const minute = document.getElementById("minute-input").value;

    const result = await API.scheduleExport(hour, minute);
    showAlert(result.message, result.success ? "success" : "danger");
  });
});
