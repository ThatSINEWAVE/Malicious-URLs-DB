// Main data object
let accountsData = {};
let filteredData = [];
let currentPage = 1;
const rowsPerPage = 10;

// Dark mode toggle
const darkModeToggle = document.getElementById('darkModeToggle');
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('bg-gray-900');
    document.body.classList.toggle('text-white');
    const cards = document.querySelectorAll('.bg-white');
    cards.forEach(card => {
        card.classList.toggle('bg-gray-800');
        card.classList.toggle('text-white');
    });
});

// Fetch data from JSON file
async function fetchData() {
    try {
        document.getElementById('loading').classList.remove('hidden');
        document.getElementById('dashboard').classList.add('hidden');

        const response = await fetch('../data/Compromised-Discord-Accounts.json');
        if (!response.ok) {
            throw new Error('Failed to fetch data');
        }

        accountsData = await response.json();
        processData();

        document.getElementById('loading').classList.add('hidden');
        document.getElementById('dashboard').classList.remove('hidden');
    } catch (error) {
        console.error('Error fetching data:', error);
        alert('Failed to load data. Please check that the data file exists and is accessible.');
    }
}

// Process data and initialize charts
function processData() {
    // Populate filter dropdowns
    populateFilters();

    // Initialize with all data
    filterData();

    // Update stats
    updateStats();

    // Create charts
    createCharts();
}

// Populate filter dropdowns
function populateFilters() {
    const attackMethods = new Set();

    Object.values(accountsData).forEach(account => {
        attackMethods.add(account.ATTACK_METHOD);
    });

    const attackMethodFilter = document.getElementById('attackMethodFilter');
    attackMethods.forEach(method => {
        const option = document.createElement('option');
        option.value = method;
        option.textContent = method;
        attackMethodFilter.appendChild(option);
    });

    // Initialize date filters
    const dates = Object.values(accountsData).map(account => new Date(account.FOUND_ON));
    if (dates.length > 0) {
        const minDate = new Date(Math.min(...dates));
        const maxDate = new Date(Math.max(...dates));

        document.getElementById('dateFrom').value = minDate.toISOString().split('T')[0];
        document.getElementById('dateTo').value = maxDate.toISOString().split('T')[0];
    }
}

// Filter data based on current filters
function filterData() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const attackMethod = document.getElementById('attackMethodFilter').value;
    const dateFrom = new Date(document.getElementById('dateFrom').value);
    const dateTo = new Date(document.getElementById('dateTo').value);
    dateTo.setHours(23, 59, 59); // Include the entire day

    filteredData = Object.values(accountsData).filter(account => {
        const foundDate = new Date(account.FOUND_ON);
        const matchesSearch =
            (account.USERNAME && account.USERNAME.toLowerCase().includes(searchTerm)) ||
            (account.BEHAVIOUR && account.BEHAVIOUR.toLowerCase().includes(searchTerm)) ||
            (account.ATTACK_METHOD && account.ATTACK_METHOD.toLowerCase().includes(searchTerm)) ||
            (account.ATTACK_VECTOR && account.ATTACK_VECTOR.toLowerCase().includes(searchTerm)) ||
            (account.DISCORD_ID && account.DISCORD_ID.includes(searchTerm));

        const matchesAttackMethod = !attackMethod || account.ATTACK_METHOD === attackMethod;
        const matchesDate = (!dateFrom || foundDate >= dateFrom) && (!dateTo || foundDate <= dateTo);

        return matchesSearch && matchesAttackMethod && matchesDate;
    });

    // Reset to first page
    currentPage = 1;

    // Update table and stats
    updateStats();
    updateTable();
    createCharts();
}

// Update main stats
function updateStats() {
    document.getElementById('totalAccounts').textContent = filteredData.length;

    const activeUrls = filteredData.filter(account =>
        account.FINAL_URL_STATUS === 'ACTIVE' ||
        account.SURFACE_URL_STATUS === 'ACTIVE'
    ).length;
    document.getElementById('activeUrls').textContent = activeUrls;

    // Most common attack method
    const attackCounts = {};
    filteredData.forEach(account => {
        attackCounts[account.ATTACK_METHOD] = (attackCounts[account.ATTACK_METHOD] || 0) + 1;
    });

    let commonAttack = '';
    let maxCount = 0;
    for (const [attack, count] of Object.entries(attackCounts)) {
        if (count > maxCount) {
            maxCount = count;
            commonAttack = attack;
        }
    }
    document.getElementById('commonAttack').textContent = commonAttack || 'N/A';

    // Most targeted platform
    const platformCounts = {};
    filteredData.forEach(account => {
        platformCounts[account.ATTACK_SURFACE] = (platformCounts[account.ATTACK_SURFACE] || 0) + 1;
    });

    let targetedPlatform = '';
    maxCount = 0;
    for (const [platform, count] of Object.entries(platformCounts)) {
        if (count > maxCount) {
            maxCount = count;
            targetedPlatform = platform;
        }
    }
    document.getElementById('targetedPlatform').textContent = targetedPlatform || 'N/A';
}

// Update the data table
function updateTable() {
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = '';

    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    const pageData = filteredData.slice(startIndex, endIndex);

    pageData.forEach(account => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td class="px-6 py-4 whitespace-nowrap">${account.CASE_NUMBER}</td>
            <td class="px-6 py-4 whitespace-nowrap">${formatDate(account.FOUND_ON)}</td>
            <td class="px-6 py-4 whitespace-nowrap">${account.USERNAME}</td>
            <td class="px-6 py-4 whitespace-nowrap">${account.ATTACK_METHOD}</td>
            <td class="px-6 py-4 whitespace-nowrap">${account.ATTACK_GOAL}</td>
            <td class="px-6 py-4 whitespace-nowrap">
                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                    account.FINAL_URL_STATUS === 'ACTIVE' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                }">
                    ${account.FINAL_URL_STATUS}
                </span>
            </td>
            <td class="px-6 py-4 whitespace-nowrap">
                <button class="text-indigo-600 hover:text-indigo-900 view-details" data-case="${account.CASE_NUMBER}">
                    View Details
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });

    // Update pagination info
    document.getElementById('tableInfo').textContent =
        `Showing ${startIndex + 1}-${Math.min(endIndex, filteredData.length)} of ${filteredData.length} entries`;

    // Update pagination buttons
    document.getElementById('prevPage').disabled = currentPage === 1;
    document.getElementById('nextPage').disabled = endIndex >= filteredData.length;

    // Add event listeners to view details buttons
    document.querySelectorAll('.view-details').forEach(button => {
        button.addEventListener('click', () => {
            const caseNumber = button.getAttribute('data-case');
            showAccountDetails(caseNumber);
        });
    });
}

// Show detailed information for a specific account
function showAccountDetails(caseNumber) {
    const account = Object.values(accountsData).find(acc => acc.CASE_NUMBER === caseNumber);
    if (!account) return;

    const modal = document.getElementById('detailModal');
    const modalContent = document.getElementById('modalContent');

    modalContent.innerHTML = `
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
                <h3 class="font-medium text-lg mb-2">Account Information</h3>
                <p><span class="font-medium">Case Number:</span> ${account.CASE_NUMBER}</p>
                <p><span class="font-medium">Found On:</span> ${formatDate(account.FOUND_ON)}</p>
                <p><span class="font-medium">Discord ID:</span> ${account.DISCORD_ID}</p>
                <p><span class="font-medium">Username:</span> ${account.USERNAME}</p>
                <p><span class="font-medium">Behaviour:</span> ${account.BEHAVIOUR}</p>
            </div>
            <div>
                <h3 class="font-medium text-lg mb-2">Attack Details</h3>
                <p><span class="font-medium">Attack Method:</span> ${account.ATTACK_METHOD}</p>
                <p><span class="font-medium">Attack Vector:</span> ${account.ATTACK_VECTOR}</p>
                <p><span class="font-medium">Attack Goal:</span> ${account.ATTACK_GOAL}</p>
                <p><span class="font-medium">Attack Surface:</span> ${account.ATTACK_SURFACE}</p>
                <p><span class="font-medium">Suspected Origin:</span> ${account.SUSPECTED_REGION_OF_ORIGIN}</p>
            </div>
        </div>
        <div class="mt-4">
            <h3 class="font-medium text-lg mb-2">URLs</h3>
            <div class="overflow-x-auto">
                <table class="min-w-full divide-y divide-gray-200">
                    <thead class="bg-gray-50">
                        <tr>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">URL Type</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">URL</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Domain</th>
                            <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">Surface URL</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <a href="#" class="text-indigo-600 hover:text-indigo-900">${account.SURFACE_URL}</a>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">${account.SURFACE_URL_DOMAIN}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                    account.SURFACE_URL_STATUS === 'ACTIVE' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                                }">
                                    ${account.SURFACE_URL_STATUS}
                                </span>
                            </td>
                        </tr>
                        <tr>
                            <td class="px-6 py-4 whitespace-nowrap">Final URL</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <a href="#" class="text-indigo-600 hover:text-indigo-900">${account.FINAL_URL}</a>
                            </td>
                            <td class="px-6 py-4 whitespace-nowrap">${account.FINAL_URL_DOMAIN}</td>
                            <td class="px-6 py-4 whitespace-nowrap">
                                <span class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                                    account.FINAL_URL_STATUS === 'ACTIVE' ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
                                }">
                                    ${account.FINAL_URL_STATUS}
                                </span>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    `;

    modal.classList.remove('hidden');
}

// Create all charts
function createCharts() {
    createTimelineChart();
    createMethodsChart();
    createSurfacesChart();
    createRegionsChart();
}

// Create timeline chart
function createTimelineChart() {
    const canvas = document.getElementById('timelineChart');

    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }

    // Group data by date
    const dateGroups = {};
    filteredData.forEach(account => {
        const date = account.FOUND_ON;
        dateGroups[date] = (dateGroups[date] || 0) + 1;
    });

    // Sort dates
    const sortedDates = Object.keys(dateGroups).sort();

    // Create chart
    canvas.chart = new Chart(canvas, {
        type: 'line',
        data: {
            labels: sortedDates.map(date => formatDate(date)),
            datasets: [{
                label: 'Compromised Accounts',
                data: sortedDates.map(date => dateGroups[date]),
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: 'rgba(99, 102, 241, 1)',
                borderWidth: 2,
                tension: 0.3,
                fill: true
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top',
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

// Create attack methods chart
function createMethodsChart() {
    const canvas = document.getElementById('methodsChart');

    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }

    // Count attack methods
    const methodCounts = {};
    filteredData.forEach(account => {
        const method = account.ATTACK_METHOD;
        methodCounts[method] = (methodCounts[method] || 0) + 1;
    });

    // Get labels and data
    const labels = Object.keys(methodCounts);
    const data = Object.values(methodCounts);

    // Generate colors
    const backgroundColors = labels.map((_, i) =>
        `hsl(${(i * 137) % 360}, 70%, 60%)`
    );

    // Create chart
    canvas.chart = new Chart(canvas, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Create attack surfaces chart
function createSurfacesChart() {
    const canvas = document.getElementById('surfacesChart');

    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }

    // Count attack surfaces
    const surfaceCounts = {};
    filteredData.forEach(account => {
        const surface = account.ATTACK_SURFACE;
        surfaceCounts[surface] = (surfaceCounts[surface] || 0) + 1;
    });

    // Get labels and data
    const labels = Object.keys(surfaceCounts);
    const data = Object.values(surfaceCounts);

    // Create chart
    canvas.chart = new Chart(canvas, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: 'Target Count',
                data: data,
                backgroundColor: 'rgba(6, 182, 212, 0.8)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        precision: 0
                    }
                }
            }
        }
    });
}

// Create regions chart
function createRegionsChart() {
    const canvas = document.getElementById('regionsChart');

    // Destroy existing chart if it exists
    if (canvas.chart) {
        canvas.chart.destroy();
    }

    // Count regions
    const regionCounts = {};
    filteredData.forEach(account => {
        const region = account.SUSPECTED_REGION_OF_ORIGIN || 'UNKNOWN';
        regionCounts[region] = (regionCounts[region] || 0) + 1;
    });

    // Get labels and data
    const labels = Object.keys(regionCounts);
    const data = Object.values(regionCounts);

    // Generate colors
    const backgroundColors = labels.map((_, i) =>
        `hsl(${(i * 137 + 60) % 360}, 70%, 60%)`
    );

    // Create chart
    canvas.chart = new Chart(canvas, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: backgroundColors,
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right',
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ${value} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Format date to a more readable format
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

// Export data to CSV
function exportToCSV() {
    const headers = [
        'Case Number',
        'Found On',
        'Discord ID',
        'Username',
        'Behaviour',
        'Attack Method',
        'Attack Vector',
        'Attack Goal',
        'Attack Surface',
        'Suspected Region',
        'Surface URL',
        'Surface URL Domain',
        'Surface URL Status',
        'Final URL',
        'Final URL Domain',
        'Final URL Status'
    ];

    let csvContent = headers.join(',') + '\n';

    filteredData.forEach(account => {
        const row = [
            account.CASE_NUMBER,
            account.FOUND_ON,
            account.DISCORD_ID,
            `"${(account.USERNAME || '').replace(/"/g, '""')}"`,
            `"${(account.BEHAVIOUR || '').replace(/"/g, '""')}"`,
            `"${(account.ATTACK_METHOD || '').replace(/"/g, '""')}"`,
            `"${(account.ATTACK_VECTOR || '').replace(/"/g, '""')}"`,
            `"${(account.ATTACK_GOAL || '').replace(/"/g, '""')}"`,
            `"${(account.ATTACK_SURFACE || '').replace(/"/g, '""')}"`,
            account.SUSPECTED_REGION_OF_ORIGIN,
            `"${(account.SURFACE_URL || '').replace(/"/g, '""')}"`,
            account.SURFACE_URL_DOMAIN,
            account.SURFACE_URL_STATUS,
            `"${(account.FINAL_URL || '').replace(/"/g, '""')}"`,
            account.FINAL_URL_DOMAIN,
            account.FINAL_URL_STATUS
        ];
        csvContent += row.join(',') + '\n';
    });

    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.setAttribute('href', url);
    link.setAttribute('download', 'malicious_accounts_export.csv');
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Event listeners
document.addEventListener('DOMContentLoaded', () => {
    // Fetch data when page loads
    fetchData();

    // Search and filter events
    document.getElementById('searchInput').addEventListener('input', filterData);
    document.getElementById('attackMethodFilter').addEventListener('change', filterData);
    document.getElementById('dateFrom').addEventListener('change', filterData);
    document.getElementById('dateTo').addEventListener('change', filterData);

    // Pagination events
    document.getElementById('prevPage').addEventListener('click', () => {
        if (currentPage > 1) {
            currentPage--;
            updateTable();
        }
    });

    document.getElementById('nextPage').addEventListener('click', () => {
        const maxPage = Math.ceil(filteredData.length / rowsPerPage);
        if (currentPage < maxPage) {
            currentPage++;
            updateTable();
        }
    });

    // Modal events
    document.getElementById('closeModal').addEventListener('click', () => {
        document.getElementById('detailModal').classList.add('hidden');
    });

    // Close modal when clicking outside
    document.getElementById('detailModal').addEventListener('click', (e) => {
        if (e.target === document.getElementById('detailModal')) {
            document.getElementById('detailModal').classList.add('hidden');
        }
    });

    // Export CSV
    document.getElementById('exportCSV').addEventListener('click', exportToCSV);

    // Refresh data
    document.getElementById('refreshData').addEventListener('click', fetchData);
});