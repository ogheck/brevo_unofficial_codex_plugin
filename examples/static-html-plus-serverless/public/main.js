const form = document.querySelector("#lead-form");
const status = document.querySelector("#form-status");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const formData = new FormData(form);
  const payload = Object.fromEntries(formData.entries());

  status.textContent = "Submitting...";

  try {
    const response = await fetch("/api/brevo-lead", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const result = await response.json();
    if (!response.ok || !result.ok) {
      throw new Error(result.message || "Submission failed.");
    }

    form.reset();
    status.textContent = "Thanks. Your request was received.";
  } catch (error) {
    status.textContent = error instanceof Error ? error.message : "Submission failed.";
  }
});
