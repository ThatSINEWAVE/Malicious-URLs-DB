// Load the JSON data
fetch('Compromised-Discord-Accounts.json')
  .then(response => response.json())
  .then(data => {
    const tableBody = document.querySelector('#data-table tbody');
    const navbar = document.getElementById('navbar');
    const thElements = document.querySelectorAll('#data-table th');
    let prevScrollPos = window.pageYOffset;
    let sortOrder = 'asc';
    let sortColumn = 'FOUND_ON';

    // Function to render the data in the table
    function renderData() {
      // Clear the table body
      tableBody.innerHTML = '';

      // Convert the data object to an array and sort it based on the selected column and order
      const dataArray = Object.values(data).sort((a, b) => {
        const valueA = a[sortColumn];
        const valueB = b[sortColumn];
        if (sortColumn === 'CASE_NUMBER') {
          // Special sorting logic for case numbers
          const caseNumA = parseInt(valueA.replace('CASE_NUMBER_', ''), 10);
          const caseNumB = parseInt(valueB.replace('CASE_NUMBER_', ''), 10);
          return sortOrder === 'asc' ? caseNumA - caseNumB : caseNumB - caseNumA;
        } else if (typeof valueA === 'string' && typeof valueB === 'string') {
          return sortOrder === 'asc' ? valueA.localeCompare(valueB) : valueB.localeCompare(valueA);
        } else {
          return sortOrder === 'asc' ? valueA - valueB : valueB - valueA;
        }
      });

      // Loop through the sorted data and create table rows
      dataArray.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${item.CASE_NUMBER}</td>
          <td>${item.FOUND_ON}</td>
          <td>${item.DISCORD_ID}</td>
          <td>${item.USERNAME}</td>
          <td>${item.BEHAVIOUR}</td>
          <td>${item.ATTACK_METHOD}</td>
          <td>${item.ATTACK_VECTOR}</td>
          <td>${item.ATTACK_GOAL}</td>
          <td>${item.ATTACK_SURFACE}</td>
          <td>${item.SUSPECTED_REGION_OF_ORIGIN}</td>
          <td>${item.SURFACE_URL}</td>
          <td>${item.SURFACE_URL_DOMAIN}</td>
          <td>${item.SURFACE_URL_STATUS}</td>
          <td>${item.FINAL_URL}</td>
          <td>${item.FINAL_URL_DOMAIN}</td>
          <td>${item.FINAL_URL_STATUS}</td>
        `;
        tableBody.appendChild(row);
      });
    }

    // Initial render with default sort order
    renderData();
    navbar.classList.add('show'); // Add the 'show' class to the navigation bar

    // Event listener for column header clicks
    thElements.forEach(th => {
      th.addEventListener('click', () => {
        const column = th.getAttribute('data-sort');
        if (column === sortColumn) {
          // Toggle sort order if the same column is clicked
          sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
        } else {
          // Set the new sort column and reset to ascending order
          sortColumn = column;
          sortOrder = 'asc';
        }
        renderData();
      });
    });

    // Sticky navbar logic
    window.addEventListener('scroll', () => {
      const currentScrollPos = window.pageYOffset;
      if (currentScrollPos > prevScrollPos) {
        // Scrolling down, hide the navbar
        navbar.classList.remove('show');
      } else {
        // Scrolling up, show the navbar
        navbar.classList.add('show');
      }
      prevScrollPos = currentScrollPos;
    });
  })
  .catch(error => console.error('Error loading data:', error));