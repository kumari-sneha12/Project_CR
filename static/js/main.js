// DriveEase Core JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // 1. Remove Loading Spinner
    const loader = document.getElementById('loading-overlay');
    if (loader) {
        setTimeout(function() {
            loader.style.opacity = '0';
            loader.style.visibility = 'hidden';
        }, 300); // Small delay for visual satisfaction
    }

    // 2. Sticky Navbar Shrink Effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-shrink');
            } else {
                navbar.classList.remove('navbar-shrink');
            }
        });
    }

    // 3. Scroll to Top Button
    const mybutton = document.getElementById("btn-back-to-top");
    if (mybutton) {
        window.addEventListener('scroll', function() {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                mybutton.style.display = "flex";
            } else {
                mybutton.style.display = "none";
            }
        });

        mybutton.addEventListener("click", function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 4. Dark Mode / Light Mode Toggle
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme');

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark' && toggleSwitch) {
            toggleSwitch.checked = true;
        }
    } else {
        // Default to dark mode for premium look
        document.documentElement.setAttribute('data-theme', 'dark');
        localStorage.setItem('theme', 'dark');
        if (toggleSwitch) {
            toggleSwitch.checked = true;
        }
    }

    if (toggleSwitch) {
        toggleSwitch.addEventListener('change', function(e) {
            if (e.target.checked) {
                document.documentElement.setAttribute('data-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-theme', 'light');
                localStorage.setItem('theme', 'light');
            }
        });
    }

    // 5. Auto Close Toast Alerts
    const toastAlerts = document.querySelectorAll('.toast');
    if (toastAlerts.length > 0) {
        toastAlerts.forEach(function(toastEl) {
            const toast = new bootstrap.Toast(toastEl, { delay: 5000 });
            toast.show();
        });
    }

    // 6. Real-time Rental Calculator on Car Detail / Checkout
    const pickupInput = document.getElementById('id_pickup_date');
    const returnInput = document.getElementById('id_return_date');
    const priceElement = document.getElementById('car_price_per_day');
    
    if (pickupInput && returnInput && priceElement) {
        const pricePerDay = parseFloat(priceElement.dataset.price);
        
        function calculateEstimates() {
            const pickupDate = new Date(pickupInput.value);
            const returnDate = new Date(returnInput.value);
            
            if (!isNaN(pickupDate.getTime()) && !isNaN(returnDate.getTime())) {
                const diffTime = Math.abs(returnDate - pickupDate);
                let diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
                
                if (pickupDate >= returnDate) {
                    diffDays = 1;
                }
                
                const baseCost = pricePerDay * diffDays;
                const tax = baseCost * 0.15;
                const grandTotal = baseCost + tax;
                
                // Update HTML elements if they exist
                const daysEl = document.getElementById('calc_days');
                const rentEl = document.getElementById('calc_rent');
                const taxEl = document.getElementById('calc_tax');
                const totalEl = document.getElementById('calc_total');
                
                if (daysEl) daysEl.innerText = diffDays + ' Days';
                if (rentEl) rentEl.innerText = '$' + baseCost.toFixed(2);
                if (taxEl) taxEl.innerText = '$' + tax.toFixed(2);
                if (totalEl) totalEl.innerText = '$' + grandTotal.toFixed(2);
            }
        }
        
        pickupInput.addEventListener('change', calculateEstimates);
        returnInput.addEventListener('change', calculateEstimates);
        
        // Run once on load if values are present
        if (pickupInput.value && returnInput.value) {
            calculateEstimates();
        }
    }
});
