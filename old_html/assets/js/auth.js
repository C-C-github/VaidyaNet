function login() {
  const role = document.getElementById("role").value;

  if (role === "patient") window.location = "patient/dashboard.html";
  if (role === "doctor") window.location = "doctor/dashboard.html";
  if (role === "admin") window.location = "admin/dashboard.html";
}
