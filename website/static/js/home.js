// eye-toggler
function togglePassword(type) {
    let passwordField, toggleIcon;
    
    if (type === 'register1') {
        passwordField = document.getElementById('id_password1');
        toggleIcon = document.getElementById('toggle-icon-register1');
    } else if (type === 'register2') {
        passwordField = document.getElementById('id_password2');
        toggleIcon = document.getElementById('toggle-icon-register2');
    } else {
        passwordField = document.getElementById('password-field');
        toggleIcon = document.getElementById('toggle-icon');
    }

    if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggleIcon.classList.remove('bi-eye-fill');
        toggleIcon.classList.add('bi-eye-slash-fill');
    } else {
        passwordField.type = 'password';
        toggleIcon.classList.remove('bi-eye-slash-fill');
        toggleIcon.classList.add('bi-eye-fill');
    }
}


// view records
document.addEventListener('DOMContentLoaded', () => {
    fetch('/records/')
    .then(response => response.json())
    .then(data => {
        const recordsContainer = document.getElementById('records-container');
        recordsContainer.innerHTML = ''; 
        data.forEach(record => {
            const recordItem = document.createElement('tr');
            recordItem.innerHTML = `
                <td>
                    <a href="/details/${record.ID}/" data-bs-toggle="popover" class="popover-link"
                    data-bs-content="Click to view more details of ${record.first_name} ${record.last_name}">
                    <span class="badge bg-primary" >${record.ID}</span>
                </td>
                <td>${record.first_name} ${record.last_name}</td>
                <td>${record.contract}</td>
                <td>${record.tenure}</td>
                <td>${record.payment_method}</td>
                <td>${record.internet_service}</td>
                <td>${record.online_security}</td>
                <td>${record.tech_support}</td>
                <td>${record.monthly_charges}</td>
                <td>${record.total_charges}</td>
                <td><a href="/notes/${record.ID}/" class="btn btn-primary mx-2 back-btn" ><i class="bi bi-check2-circle"></i></a></td>
                
            `;
            recordsContainer.appendChild(recordItem); 
        });

        const popoverLinks = document.querySelectorAll('.popover-link');
        popoverLinks.forEach(link => {
            new bootstrap.Popover(link, {
                trigger: 'hover'
            });
        });
    })
    .catch(error => {
        console.error('Error fetching records', error);
    });
});

   

// Search function

function filterRecords() {
    const input = document.getElementById('inputText');
    const filter = input.value.toLowerCase();
    let found = false;


    const table = document.getElementById('records-container');
    const rows = table.getElementsByTagName('tr');

    for (let i =0; i<rows.length; i++ ) {
        const cells = rows[i].getElementsByTagName('td');
        if (cells.length > 0) {
          const cellName = cells[1];
          if (cellName) {
            const textValue = cellName.innerText;
            if(textValue.toLowerCase().indexOf(filter) > -1) {
                rows[i].style.display = "";
            found = true; 
            }
            else {
              rows[i].style.display = "none";
            }
            } // "" means show the element in style.display
            
          }
        }
    const noRecords = document.getElementById('no-records')
    if(found) {
        noRecords.style.display = "none"; //hide the message
    }
    else {
        noRecords.style.display ="block"
    }
    }