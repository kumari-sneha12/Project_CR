// DriveEase AJAX Search Suggestions

document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('navbar-search-input') || document.getElementById('hero-search-input');
    const suggestionsContainer = document.getElementById('search-suggestions');

    if (searchInput && suggestionsContainer) {
        searchInput.addEventListener('input', function() {
            const query = searchInput.value.trim();
            
            if (query.length < 2) {
                suggestionsContainer.innerHTML = '';
                suggestionsContainer.style.display = 'none';
                return;
            }

            fetch(`/cars/suggestions/?q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    suggestionsContainer.innerHTML = '';
                    
                    if (data.results && data.results.length > 0) {
                        data.results.forEach(item => {
                            const suggestionDiv = document.createElement('div');
                            suggestionDiv.classList.add('search-suggestion-item');
                            
                            // Include car brand/model and a small icon
                            suggestionDiv.innerHTML = `
                                <i class="fas fa-car me-2 text-gold"></i>
                                <div>
                                    <strong>${item.brand}</strong> ${item.model_name}
                                    <span class="text-muted d-block" style="font-size: 0.75rem;">$${item.price_per_day}/day - ${item.fuel_type}</span>
                                </div>
                            `;
                            
                            suggestionDiv.addEventListener('click', function() {
                                searchInput.value = `${item.brand} ${item.model_name}`;
                                suggestionsContainer.innerHTML = '';
                                suggestionsContainer.style.display = 'none';
                                
                                // Auto redirect or submit form
                                const parentForm = searchInput.closest('form');
                                if (parentForm) {
                                    parentForm.submit();
                                } else {
                                    window.location.href = `/cars/detail/${item.id}/`;
                                }
                            });
                            
                            suggestionsContainer.appendChild(suggestionDiv);
                        });
                        suggestionsContainer.style.display = 'block';
                    } else {
                        suggestionsContainer.style.display = 'none';
                    }
                })
                .catch(error => {
                    console.error('Error fetching suggestions:', error);
                });
        });

        // Close suggestions container when clicking outside
        document.addEventListener('click', function(e) {
            if (e.target !== searchInput && e.target !== suggestionsContainer) {
                suggestionsContainer.innerHTML = '';
                suggestionsContainer.style.display = 'none';
            }
        });
    }
});
