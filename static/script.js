let searchController = new AbortController(); // Initialize an AbortController.

function doSearch(e) {
    // Get the search term from the search bar.
    let search_term = document.getElementById("search_bar").value;

    if (search_term === "") {
        // If the search term is empty, do nothing.
        return;
    }

    // Abort the previous search request, if it's still ongoing.
    searchController.abort();
    searchController = new AbortController();

    // Construct the URL for the search request.
    let searchUrl = `/search/${encodeURIComponent(search_term)}`;

    // Make a new search request using the Fetch API.
    fetch(searchUrl, {
        method: 'GET',
        signal: searchController.signal, // Associate the AbortController's signal with the request.
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle the search results here.
        let searchResults = document.getElementById("search_results");
        searchResults.innerHTML = "";
        // {id: {name: "name", link: "link"}}
        for (let id in data) {
            let name = id + ": " + data[id]["name"];
            let url = data[id]["link"];
            let result = document.createElement("a");
            result.href = url;
            result.innerHTML = name;
            searchResults.appendChild(result);
            searchResults.appendChild(document.createElement("br"));
        }
    })
    .catch(error => {
        if (error.name === 'AbortError') {
            // The request was aborted, which is expected.
            console.log('Search request aborted');
        } else {
            // Handle other errors.
            console.error('Error:', error);
        }
    });
}
