// Initialize Toast Library
const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 2000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
        }
    });

// Check if dark mode is enabled
const html_element = document.getElementsByTagName('html')[0];
if (html_element.getAttribute('data-bs-theme') == 'auto') {
    const windows_theme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    html_element.setAttribute('data-bs-theme', windows_theme);
}

function compareDates(d1, d2) {
    // Return -1 if d1 is before d2, 1 if d1 is after d2, and 0 if they are the same
    // Convert to UTC to avoid local timezone differences
    const yearDiff = d1.getUTCFullYear() - d2.getUTCFullYear();
    if (yearDiff < 0) {
        return -1
    } else if (yearDiff > 0) {
        return 1
    } else {
        const monthDiff = d1.getUTCMonth() - d2.getUTCMonth();
        if (monthDiff < 0) {
            return -1
        } else if (monthDiff > 0) {
            return 1
        } else {
            const dayDiff = d1.getUTCDate() - d2.getUTCDate();
            if (dayDiff < 0) {
                return -1
            } else if (dayDiff > 0) {
                return 1
            } else {
                return 0
            }
        }
    }
}