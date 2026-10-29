"use strict";

(() => {
  const shell = document.getElementById("startup");
  const status = document.getElementById("startup-status");
  const retry = document.getElementById("startup-retry");
  const name = shell.dataset.startupName || "workspace";
  let slow, deadline;
  const finish = () => {
    clearTimeout(slow);
    clearTimeout(deadline);
    shell.remove();
  };
  slow = setTimeout(() => {
    status.textContent = `Still starting the ${name}. The service may have been idle. You can wait or try again.`;
    retry.hidden = false;
  }, 4000);
  deadline = setTimeout(() => {
    status.textContent = `The ${name} is taking longer than expected. Try again. If this continues, contact application support.`;
    retry.hidden = false;
  }, 15000);
  retry.addEventListener("click", () => location.reload());
  document.addEventListener("workspace-ready", finish, { once: true });
})();
