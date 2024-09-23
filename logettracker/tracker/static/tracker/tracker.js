document.addEventListener("DOMContentLoaded", function () {
  const greenCheckButtons = document.querySelectorAll(".greenCheck");
  const redXButtons = document.querySelectorAll(".redX");

  greenCheckButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const divId = this.getAttribute("data-id");
      const container = document.getElementById(divId);
      if (!container.classList.contains("collected")) {
        container.classList.add("collected");
      }
      sendCardActionToBackend(divId, "add");
    });
  });

  redXButtons.forEach((button) => {
    button.addEventListener("click", function () {
      const divId = this.getAttribute("data-id");
      const container = document.getElementById(divId);
      if (container.classList.contains("collected")) {
        container.classList.remove("collected");
      }
      sendCardActionToBackend(divId, "remove");
    });
  });

  // Send action to Django backend
  function sendCardActionToBackend(divId, action) {
    fetch(`processcardaction/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"), // CSRF token for security
      },
      body: JSON.stringify({ div_id: divId, action: action }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }

  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
