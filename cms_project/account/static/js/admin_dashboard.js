function toggleAdminDropdown() {
    document.getElementById("adminDropdownMenu").classList.toggle("show-dropdown");
}

window.onclick = function(event) {
    if (!event.target.closest('.admin-dropdown')) {
        let dropdown = document.getElementById("adminDropdownMenu");
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
let courseChartInstance = null;
let resultChartInstance = null;
let feeChartInstance = null;
let examChartInstance = null;
let departmentChartInstance = null;

function loadAdminCharts() {
    const attendanceCtx = document.getElementById('attendanceChart');
    const courseCtx = document.getElementById('courseChart');
    const resultCtx = document.getElementById('resultChart');
    const feeCtx = document.getElementById('feeChart');
    const examCtx = document.getElementById('examChart');
    const departmentCtx = document.getElementById('departmentChart');

    if (!attendanceCtx || !courseCtx || !resultCtx || !feeCtx || !examCtx || !departmentCtx) {
        return;
    }

    const attendancePresentElement = document.getElementById('attendance-present-data');
    const attendanceAbsentElement = document.getElementById('attendance-absent-data');

    const attendancePresentCount = attendancePresentElement ? JSON.parse(attendancePresentElement.textContent) : 0;
    const attendanceAbsentCount = attendanceAbsentElement ? JSON.parse(attendanceAbsentElement.textContent) : 0;

    const courseLabelsElement = document.getElementById('course-labels-data');
    const courseCountsElement = document.getElementById('course-student-counts-data');

    const resultLabelsElement = document.getElementById('result-labels-data');
    const resultMarksElement = document.getElementById('result-marks-data');

    const feeStatusLabelsElement = document.getElementById('fee-status-labels-data');
    const feeStatusCountsElement = document.getElementById('fee-status-counts-data');

    const examLabelsElement = document.getElementById('exam-labels-data');
    const examCountsElement = document.getElementById('exam-counts-data');

    const departmentLabelsElement = document.getElementById('department-labels-data');
    const departmentTeacherCountsElement = document.getElementById('department-teacher-counts-data');

    const courseLabels = courseLabelsElement ? JSON.parse(courseLabelsElement.textContent) : [];
    const courseStudentCounts = courseCountsElement ? JSON.parse(courseCountsElement.textContent) : [];

    const resultLabels = resultLabelsElement ? JSON.parse(resultLabelsElement.textContent) : [];
    const resultMarksData = resultMarksElement ? JSON.parse(resultMarksElement.textContent) : [];

    const feeStatusLabels = feeStatusLabelsElement ? JSON.parse(feeStatusLabelsElement.textContent) : [];
    const feeStatusCounts = feeStatusCountsElement ? JSON.parse(feeStatusCountsElement.textContent) : [];

    const examLabels = examLabelsElement ? JSON.parse(examLabelsElement.textContent) : [];
    const examCounts = examCountsElement ? JSON.parse(examCountsElement.textContent) : [];

    const departmentLabels = departmentLabelsElement ? JSON.parse(departmentLabelsElement.textContent) : [];
    const departmentTeacherCounts = departmentTeacherCountsElement ? JSON.parse(departmentTeacherCountsElement.textContent) : [];

    if (attendanceChartInstance) attendanceChartInstance.destroy();
    if (courseChartInstance) courseChartInstance.destroy();
    if (resultChartInstance) resultChartInstance.destroy();
    if (feeChartInstance) feeChartInstance.destroy();
    if (examChartInstance) examChartInstance.destroy();
    if (departmentChartInstance) departmentChartInstance.destroy();

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

    courseChartInstance = new Chart(courseCtx, {
        type: 'bar',
        data: {
            labels: courseLabels,
            datasets: [{
                label: 'Students',
                data: courseStudentCounts,
                backgroundColor: '#36A2EB',
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

    resultChartInstance = new Chart(resultCtx, {
        type: 'bar',
        data: {
            labels: resultLabels,
            datasets: [{
                label: 'Marks',
                data: resultMarksData,
                backgroundColor: '#8BC34A',
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

    feeChartInstance = new Chart(feeCtx, {
        type: 'pie',
        data: {
            labels: feeStatusLabels,
            datasets: [{
                data: feeStatusCounts,
                backgroundColor: ['#00C853', '#FF9800'],
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

    examChartInstance = new Chart(examCtx, {
        type: 'bar',
        data: {
            labels: examLabels,
            datasets: [{
                label: 'Exams',
                data: examCounts,
                backgroundColor: '#9966FF',
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

    departmentChartInstance = new Chart(departmentCtx, {
        type: 'bar',
        data: {
            labels: departmentLabels,
            datasets: [{
                label: 'Teachers',
                data: departmentTeacherCounts,
                backgroundColor: '#FF6384',
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
}

window.onload = function() {
    const sections = document.querySelectorAll('.content-section');
    sections.forEach(section => {
        section.style.display = 'none';
    });

    let activeSectionId = 'dashboardSection';
    const params = new URLSearchParams(window.location.search);
    activeSectionId = params.get('section') || 'dashboardSection';

    const activeSection = document.getElementById(activeSectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
        activeSection.classList.add('active-section');
    } else {
        document.getElementById('dashboardSection').style.display = 'block';
        document.getElementById('dashboardSection').classList.add('active-section');
    }

    loadAdminCharts();
};