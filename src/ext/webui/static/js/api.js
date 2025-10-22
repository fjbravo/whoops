export const API = {
  async exportNow() {
    try {
      const response = await fetch("/export", { method: "POST" });
      if (!response.ok) throw new Error(`Failed to export (status: ${response.status})`);
      return { success: true, message: "Export completed successfully" };
    } catch (err) {
      return { success: false, message: err.message };
    }
  },

  async scheduleExport(hour, minute) {
    try {
      const response = await fetch("/schedule", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ hour, minute }),
      });
      if (!response.ok) throw new Error(`Failed to schedule (status: ${response.status})`);
      const data = await response.json();
      return { success: true, message: data.message };
    } catch (err) {
      return { success: false, message: err.message };
    }
  },
};
