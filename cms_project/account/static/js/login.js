function showLoginSection() {
    document.getElementById("loginSection").style.display = "block";
    document.getElementById("signupSection").style.display = "none";
}

function showSignupSection() {
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("signupSection").style.display = "block";
}

function selectRole(role) {
    let form = document.getElementById("dynamicLoginForm");
    let roleInput = document.getElementById("selected_role");
    let title = document.getElementById("loginRoleTitle");
    let submitBtn = document.getElementById("loginSubmitBtn");

    roleInput.value = role;

    if (role === "admin") {
        form.action = "/admin_login/";
        title.innerText = "Admin Sign In";
        submitBtn.innerText = "Admin Login";
    } 
    else if (role === "teacher") {
        form.action = "/teacher_login/";
        title.innerText = "Teacher Sign In";
        submitBtn.innerText = "Teacher Login";
    } 
    else if (role === "student") {
        form.action = "/student_login/";
        title.innerText = "Student Sign In";
        submitBtn.innerText = "Student Login";
    }

    document.querySelectorAll(".role-btn").forEach(btn => {
        btn.classList.remove("active-role");
    });

    document.querySelector("." + role).classList.add("active-role");
}

/* 🔥 IMPORTANT AUTO CONTROL */
window.onload = function () {

    showLoginSection();

    const heroSection = document.getElementById("heroSection");
    const loginPage = document.getElementById("loginPage");
    const showSignupFlag = document.getElementById("showSignupFlag");
    const successFlag = document.getElementById("successFlag");
    const errorFlag = document.getElementById("errorFlag");

    function openLoginPage() {
        if (heroSection) heroSection.style.display = "none";
        if (loginPage) loginPage.style.display = "block";
    }

    if (showSignupFlag && showSignupFlag.value === "true") {
        openLoginPage();
        showSignupSection();
    } else if (successFlag && successFlag.value === "true") {
        openLoginPage();
        showLoginSection();
    } else if (errorFlag && errorFlag.value === "true") {
        openLoginPage();
        showLoginSection();
    }
};

/* ================= PASSWORD TOGGLE ================= */

const toggle = document.getElementById("togglePassword");
const password = document.getElementById("password");

if (toggle && password) {
    toggle.addEventListener("click", function () {
        if (password.type === "password") {
            password.type = "text";
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
        } else {
            password.type = "password";
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
        }
    });
}

/* ================= SIGNUP PASSWORD ================= */

const toggleSignup = document.getElementById("toggleSignupPassword");
const signupPassword = document.getElementById("signupPassword");

if (toggleSignup && signupPassword) {
    toggleSignup.addEventListener("click", function () {
        if (signupPassword.type === "password") {
            signupPassword.type = "text";
            this.classList.remove("fa-eye-slash");
            this.classList.add("fa-eye");
        } else {
            signupPassword.type = "password";
            this.classList.remove("fa-eye");
            this.classList.add("fa-eye-slash");
        }
    });
}

function showForgetSection() {
    document.getElementById("loginSection").style.display = "none";
    document.getElementById("signupSection").style.display = "none";
    document.getElementById("forgetSection").style.display = "block";
}

function showLoginSection() {
    document.getElementById("loginSection").style.display = "block";
    document.getElementById("signupSection").style.display = "none";
    document.getElementById("forgetSection").style.display = "none";
}