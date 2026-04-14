function toggleTeacherDropdown() {
    document.getElementById("teacherDropdownMenu").classList.toggle("show-dropdown");
}

window.onclick = function(event) {
    if (!event.target.closest('.teacher-dropdown')) {
        let dropdown = document.getElementById("teacherDropdownMenu");
        if (dropdown.classList.contains("show-dropdown")) {
            dropdown.classList.remove("show-dropdown");
        }
    }
}

function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (dropdown.style.display === "block") {
        dropdown.style.display = "none";
    } else {
        dropdown.style.display = "block";
    }
}

function showSection(sectionId) {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.classList.remove('active-section');
        section.style.display = 'none';
    });

    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
        activeSection.classList.add('active-section');
    }

    if (history.replaceState) {
        const url = new URL(window.location);
        url.searchParams.set('section', sectionId);
        history.replaceState(null, '', url.toString());
    }
}

let attendanceChartInstance = null;
let resultChartInstance = null;
let courseChartInstance = null;
let examChartInstance = null;

function loadDashboardCharts() {
    const attendanceCtx = document.getElementById('attendanceChart');
    const resultCtx = document.getElementById('resultChart');
    const courseCtx = document.getElementById('courseChart');
    const examCtx = document.getElementById('examChart');

    if (!attendanceCtx || !resultCtx || !courseCtx || !examCtx) {
        return;
    }

    // ✅ FIXED PART (IMPORTANT)
    const presentElement = document.getElementById('attendance-present-data');
    const absentElement = document.getElementById('attendance-absent-data');

    const attendancePresentCount = presentElement ? JSON.parse(presentElement.textContent) : 0;
    const attendanceAbsentCount = absentElement ? JSON.parse(absentElement.textContent) : 0;

    // Other graph data
    const resultLabelsElement = document.getElementById('result-labels-data');
    const resultMarksElement = document.getElementById('result-marks-data');
    const courseLabelsElement = document.getElementById('course-labels-data');
    const courseCountsElement = document.getElementById('course-student-counts-data');
    const examLabelsElement = document.getElementById('exam-labels-data');
    const examCountsElement = document.getElementById('exam-counts-data');

    const resultLabels = resultLabelsElement ? JSON.parse(resultLabelsElement.textContent) : [];
    const resultMarksData = resultMarksElement ? JSON.parse(resultMarksElement.textContent) : [];
    const courseLabels = courseLabelsElement ? JSON.parse(courseLabelsElement.textContent) : [];
    const courseStudentCounts = courseCountsElement ? JSON.parse(courseCountsElement.textContent) : [];
    const examLabels = examLabelsElement ? JSON.parse(examLabelsElement.textContent) : [];
    const examCounts = examCountsElement ? JSON.parse(examCountsElement.textContent) : [];

    // Destroy old charts
    if (attendanceChartInstance) attendanceChartInstance.destroy();
    if (resultChartInstance) resultChartInstance.destroy();
    if (courseChartInstance) courseChartInstance.destroy();
    if (examChartInstance) examChartInstance.destroy();

    // Attendance Chart
    attendanceChartInstance = new Chart(attendanceCtx, {
        type: 'doughnut',
        data: {
            labels: ['Present', 'Absent'],
            datasets: [{
                data: [attendancePresentCount, attendanceAbsentCount],
                backgroundColor: ['#4CAF50', '#F44336'],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });

    // Result Chart
    resultChartInstance = new Chart(resultCtx, {
        type: 'bar',
        data: {
            labels: resultLabels,
            datasets: [{
                label: 'Marks',
                data: resultMarksData,
                backgroundColor: '#36A2EB',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    // Course Chart
    courseChartInstance = new Chart(courseCtx, {
        type: 'bar',
        data: {
            labels: courseLabels,
            datasets: [{
                label: 'Students',
                data: courseStudentCounts,
                backgroundColor: '#8BC34A',
                borderRadius: 6
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Exam Chart
    examChartInstance = new Chart(examCtx, {
        type: 'pie',
        data: {
            labels: examLabels,
            datasets: [{
                label: 'Exam Count',
                data: examCounts,
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ],
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                }
            }
        }
    });
}

// Page load
window.onload = function() {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    let activeSectionId = "{{ active_section|default:'dashboardSection' }}";

    if (!activeSectionId || activeSectionId === "None") {
        const params = new URLSearchParams(window.location.search);
        activeSectionId = params.get('section') || 'dashboardSection';
    }

    const dashboard = document.getElementById(activeSectionId);
    if (dashboard) {
        dashboard.style.display = 'block';
        dashboard.classList.add('active-section');
    } else {
        document.getElementById('dashboardSection').style.display = 'block';
        document.getElementById('dashboardSection').classList.add('active-section');
    }

    loadDashboardCharts();
};