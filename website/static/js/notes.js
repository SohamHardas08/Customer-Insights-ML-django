// calendar view
function disablePrevious() {
    const today = new Date();
    const day = String(today.getDate()).padStart(2,'0');
    const month = String(today.getMonth()+1).padStart(2,'0');
    const year = today.getFullYear();
    const minDate = `${year}-${month}-${day}`;

    document.getElementById('add-deadline').setAttribute('min', minDate);
    document.getElementById('edit-deadline').setAttribute('min', minDate);
}

//tab-animations

document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.nav-pills .nav-link');
    const navPills = document.querySelector('.nav-pills');

    function updateUnderline() {
        const activeTab = document.querySelector('.nav-pills .nav-link.active');
        const leftOffset = activeTab.offsetLeft;
        const tabWidth = activeTab.offsetWidth;


        navPills.style.setProperty('--nav-left', `${leftOffset}px`);
        navPills.style.setProperty('--nav-width', `${tabWidth}px`);
        }

    updateUnderline();


    tabs.forEach(tab => {
        tab.addEventListener('click', updateUnderline);
    });


    window.addEventListener('resize', updateUnderline);
});