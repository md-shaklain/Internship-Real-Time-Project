    
        function toggleStudentDropdown() {
            document.getElementById("studentDropdownMenu").classList.toggle("show-dropdown");
        }

        window.onclick = function(event) {
            if (!event.target.closest('.student-dropdown')) {
                let dropdown = document.getElementById("studentDropdownMenu");
                if (dropdown.classList.contains("show-dropdown")) {
                    dropdown.classList.remove("show-dropdown");
                }
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
        }

        let attendanceChartInstance = null;
        let resultChartInstance = null;
        let feeChartInstance = null;
        let subjectChartInstance = null;

        function loadStudentCharts() {
            const attendanceCtx = document.getElementById('attendanceChart');
            const resultCtx = document.getElementById('resultChart');
            const feeCtx = document.getElementById('feeChart');
            const subjectCtx = document.getElementById('subjectChart');

            if (!attendanceCtx || !resultCtx || !feeCtx || !subjectCtx) {
                return;
            }

            const attendanceChartLabels = JSON.parse(document.getElementById('attendance-chart-labels-data').textContent);
            const attendanceChartData = JSON.parse(document.getElementById('attendance-chart-data').textContent);

            const resultLabels = JSON.parse(document.getElementById('result-labels-data').textContent);
            const resultMarksData = JSON.parse(document.getElementById('result-marks-data').textContent);

            const feeStatusLabels = JSON.parse(document.getElementById('fee-status-labels-data').textContent);
            const feeStatusData = JSON.parse(document.getElementById('fee-status-data').textContent);

            const subjectLabels = JSON.parse(document.getElementById('subject-labels-data').textContent);
            const subjectMarksData = JSON.parse(document.getElementById('subject-marks-data').textContent);

            if (attendanceChartInstance) attendanceChartInstance.destroy();
            if (resultChartInstance) resultChartInstance.destroy();
            if (feeChartInstance) feeChartInstance.destroy();
            if (subjectChartInstance) subjectChartInstance.destroy();

            attendanceChartInstance = new Chart(attendanceCtx, {
                type: 'doughnut',
                data: {
                    labels: attendanceChartLabels,
                    datasets: [{
                        data: attendanceChartData,
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

            feeChartInstance = new Chart(feeCtx, {
                type: 'pie',
                data: {
                    labels: feeStatusLabels,
                    datasets: [{
                        data: feeStatusData,
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

            subjectChartInstance = new Chart(subjectCtx, {
                type: 'bar',
                data: {
                    labels: subjectLabels,
                    datasets: [{
                        label: 'Subject Marks',
                        data: subjectMarksData,
                        backgroundColor: '#9966FF',
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
        }

        window.onload = function() {
            const sections = document.querySelectorAll('.content-section');
            sections.forEach(section => {
                section.style.display = 'none';
            });

            document.getElementById('dashboardSection').style.display = 'block';
            document.getElementById('dashboardSection').classList.add('active-section');

            loadStudentCharts();
        }
    
